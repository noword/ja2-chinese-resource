#! /usr/bin/env python3
# coding=utf-8
from struct import unpack, pack
from io import BytesIO
import os
from PIL import Image, ImagePalette
from .base import Base

''''
IMPORTANT: This script only support 8bits sti file.
'''


STCI_ETRLE_COMPRESSED = 0x0020
STCI_ZLIB_COMPRESSED = 0x0010
STCI_INDEXED = 0x0008
STCI_RGB = 0x0004
STCI_ALPHA = 0x0002
STCI_TRANSPARENT = 0x0001

ALPHA_VALUE = 0
IS_COMPRESSED_BYTE_MASK = 0x80
NUMBER_OF_BYTES_MASK = 0x7F


def etrle_decompress(data):
    number_of_compressed_bytes = len(data)
    compressed_bytes = unpack('<{}B'.format(number_of_compressed_bytes), data)
    extracted_buffer = BytesIO()
    bytes_til_next_control_byte = 0

    for current_byte in compressed_bytes:
        if bytes_til_next_control_byte == 0:
            is_compressed_alpha_byte = ((current_byte & IS_COMPRESSED_BYTE_MASK) >> 7) == 1
            length_of_subsequence = current_byte & NUMBER_OF_BYTES_MASK
            if is_compressed_alpha_byte:
                for s in range(length_of_subsequence):
                    extracted_buffer.write(pack('<B', ALPHA_VALUE))
            else:
                bytes_til_next_control_byte = length_of_subsequence
        else:
            extracted_buffer.write(pack('<B', current_byte))
            bytes_til_next_control_byte -= 1

    if bytes_til_next_control_byte != 0:
        raise Exception('Not enough data to decompress')

    return extracted_buffer.getvalue()


def etrle_compress(data):
    current = 0
    source_length = len(data)
    compressed_buffer = BytesIO()

    while current < source_length:
        runtime_length = 0

        if data[current] == 0:
            while current + runtime_length < source_length \
                    and data[current + runtime_length] == 0 \
                    and runtime_length < NUMBER_OF_BYTES_MASK:
                runtime_length += 1
            compressed_buffer.write(pack('<B', runtime_length | IS_COMPRESSED_BYTE_MASK))
        else:
            while current + runtime_length < source_length \
                    and data[current + runtime_length] != 0 \
                    and runtime_length < NUMBER_OF_BYTES_MASK:
                runtime_length += 1
            compressed_buffer.write(pack('<B', runtime_length))
            compressed_buffer.write(pack('<{}B'.format(runtime_length), * data[current:current + runtime_length]))

        current += runtime_length

    return compressed_buffer.getvalue()


def compress_image(image):
    w, h = image.size
    buf = image.tobytes()
    data = []
    for i in range(h):
        data.append(etrle_compress(buf[w * i:w * (i + 1)]))
        data.append(b'\x00')
    return b''.join(data)


class Sti(Base, list):
    STCI_ID_STRING = b'STCI'

    def __init__(self, io=None):
        self.uiOriginalSize = 640 * 480
        self.uiTransparentValue = 0
        self.fFlags = 0x28
        self.usWidth = 640
        self.usHeight = 480
        self.uiNumberOfColours = 256
        self.ubRedDepth = 8
        self.ubGreenDepth = 8
        self.ubBlueDepth = 8
        self.ubDepth = 8
        self.uiAppDataSize = 0
        super().__init__(io)

    def load(self, io):
        if io.read(len(self.STCI_ID_STRING)) != self.STCI_ID_STRING:
            raise TypeError

        (self.uiOriginalSize,
         _,
         self.uiTransparentValue,
         self.fFlags,
         self.usHeight,
         self.usWidth) = unpack('<4I2H', io.read(0x14))

        assert self.fFlags & STCI_INDEXED
        assert self.fFlags & STCI_ETRLE_COMPRESSED

        (self.uiNumberOfColours,
         num,
         self.ubRedDepth,
         self.ubGreenDepth,
         self.ubBlueDepth,
         dummy) = unpack('<IHBBB11s', io.read(0x14))
        assert dummy == b'\x00' * 11
        assert self.uiNumberOfColours == 256

        (self.ubDepth, self.uiAppDataSize, dummy) = unpack('<BI15s', io.read(0x14))
        assert dummy == b'\x00' * 15

        colors = io.read(256 * 3)
        self.palette = ImagePalette.ImagePalette('RGB', colors, 256 * 3)

        for _ in range(num):
            self.append(dict(zip(('offset', 'size', 'x', 'y', 'h', 'w'), unpack('<2I4H', io.read(0x10)))))

        data_offset = io.tell()
        for f in self:
            io.seek(data_offset + f['offset'], os.SEEK_SET)
            buf = etrle_decompress(io.read(f['size']))
            assert len(buf) == f['w'] * f['h']
            f['image'] = Image.frombytes('P', (f['w'], f['h']), buf, 'raw')
            f['image'].putpalette(self.palette)

    def save(self, io):
        io.write(self.STCI_ID_STRING)
        io.write(pack('<4I2H',
                      self.uiOriginalSize,
                      0,
                      self.uiTransparentValue,
                      self.fFlags,
                      self.usHeight,
                      self.usWidth))

        io.write(pack('<IHBBB11s',
                      self.uiNumberOfColours,
                      len(self),
                      self.ubRedDepth,
                      self.ubGreenDepth,
                      self.ubBlueDepth,
                      b''))

        io.write(pack('<BI15s', self.ubDepth, self.uiAppDataSize, b''))

        last_palette = Image.new('P', (10, 10))
        last_palette.putpalette(ImagePalette.ImagePalette('RGB', [0, 0, 0], size=3))
        for i, f in enumerate(self):
            if f['image'].mode != 'P':
                last_palette = f['image'] = f['image'].quantize(palette=last_palette)
        palette = self[-1]['image'].getpalette()
        io.write(pack(f'{len(palette)}B', *palette))

        data_io = BytesIO()
        for f in self:
            img = f['image']
            assert img.mode == 'P'
            f['offset'] = data_io.tell()
            f['x'] = f['y'] = 0
            f['w'], f['h'] = img.size
            zbuf = compress_image(img)
            f['size'] = len(zbuf)
            io.write(pack('II4H', f['offset'], f['size'], f['x'], f['y'], f['h'], f['w']))
            data_io.write(zbuf)
        io.write(data_io.getvalue())
        io.seek(8, os.SEEK_SET)
        io.write(pack('I', data_io.tell()))

    def __str__(self):
        s = []
        for i, f in enumerate(self):
            s.append(f"{i:3d} {f['offset']:08x} {f['size']:08x} {f['x']}, {f['y']}, {f['w']}, {f['h']}")

        return '\n'.join(s)
