#! /usr/bin/env python3
# coding=utf-8
from abc import ABC, abstractmethod
from io import BytesIO
from struct import unpack, pack
import os
import re
from .base import Base

DECODE_TAB = {
    '\xb1': '[NEWLINE]',
    '\xb2': '[BOLD]',
    '\xb3': '[CENTER]',
    '\xb4': 'NEWCOLOR',
    '\xb5': 'DEFCOLOR'
}

ENCODE_TAB = {v: k for k, v in DECODE_TAB.items()}


class Edt(Base, list):
    def __init__(self, content_size, io=None):
        self.content_size = content_size
        super().__init__(io)

    def encode(self, s: str, size):
        for k, v in ENCODE_TAB.items():
            s = s.replace(k, v)
        bs = []
        for c in s:
            c = ord(c)
            if 0x410 <= c <= 0x415:
                c += 0x3d
            elif c == 0x401:
                c = 0x453
            elif 0x417 <= c <= 0x42a:
                c += 0x3e
            elif 0x42b <= c <= 0x42f:
                c += 0x3d
            if c > 32:
                c += 1
            bs.append(c)
        return pack(f'{len(bs)}H', *bs) + b'\x00\x00' * (size - len(bs))

    def decode(self, bs: bytes):
        s = []
        for c in unpack(f'{len(bs)//2}H', bs):
            if c > 33:
                c -= 1
            if 0x44d <= c <= 0x452:
                c -= 0x3d
            elif c == 0x453:
                c = 0x401
            elif 0x454 <= c <= 0x467:
                c -= 0x3e
            elif 0x468 <= c <= 0x46c:
                c -= 0x3d
            s.append(chr(c))

        s = ''.join(s).split('\x00')[0]
        for k, v in DECODE_TAB.items():
            s = s.replace(k, v)
        return s

    def load(self, io):
        size = sum(self.content_size)
        end = False
        while not end:
            f = []
            for size in self.content_size:
                buf = io.read(size * 2)
                if len(buf) < size * 2:
                    end = True
                    break
                f.append(self.decode(buf))
            if not end:
                self.append(f)

    def save(self, io):
        for f in self:
            for i, size in enumerate(self.content_size):
                io.write(self.encode(f[i], size))

    def __str__(self):
        s = []
        for i, f in enumerate(self):
            for j, ff in enumerate(f):
                s.append(f'{i:2d} {j:d} {ff}')
        return '\n'.join(s)


EDT_NAME_SIZE = {
    'AIMBIOS': [400, 160],
    'AIMHIST': [400],
    'AIMPOL': [400],
    'ALUMNI': [80, 560],
    'ALUMNAME': [80],
    'BRAYDESC': [80, 320],
    'CREDITS': [80],
    'EMAIL': [320],
    'FILES': [400],
    'FLOWERCARD': [400],
    'FLOWERDESC': [80, 80, 320],
    'FLWRDESC': [80, 80, 320],
    'HELP': [640],
    'IMPASS': [320],
    'IMPTEXT': [400],
    'INSURANCEMULTI': [400],
    'INSURANCESINGLE': [80],
    'ITEMDESC': [80, 80, 240],
    'MERCBIOS': [400, 160],
    'QUESTS': [80],
    'RIS': [400],
    'CCREDITS': [80, ]
}

EDT_PATTERN_SIZE = {
    r'\d{2,3}': [240],
    r'CIV\d{2}': [160],
    r'D_\d{3}': [240],
    r'[A-Z]\d{1,2}': [160],
}


def EdtFactory(name: str):
    key = os.path.splitext(os.path.split(name)[1])[0].upper()
    size = EDT_NAME_SIZE.get(key)
    if size:
        return Edt(size, open(name, 'rb'))
    else:
        for pn, size in EDT_PATTERN_SIZE.items():
            if re.match(pn, key):
                return Edt(size, open(name, 'rb'))
    return TypeError('unknown type')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name", action="store", nargs=1)
    args = parser.parse_args()
    edt = EdtFactory(args.name[0])
    print(edt)
