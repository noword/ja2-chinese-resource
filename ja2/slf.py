#! /usr/bin/env python3
# coding=utf-8
from struct import unpack, pack
import os
from datetime import datetime, timedelta
import time
from .base import Base


class Slf(Base, list):
    def __init__(self, io=None, name=None, path=None):
        self.sort = 0xffff
        self.version = 0x200
        self.contains_subdirectories = 1

        if name:
            self.name = name
        if path:
            self.path = path

        super().__init__(io)

    def __read_str(self, io, size=0x100):
        return io.read(size).strip(b'\x00').decode('ascii')

    def __write_str(self, io, s, size=0x100):
        s = s.encode('ascii')
        s += b'\x00' * (size - len(s))
        io.write(s)

    def load(self, io):
        self.name = self.__read_str(io)
        self.path = self.__read_str(io)
        num, num1, self.sort, self.version, self.contains_subdirectories, dummy = unpack('<IIHHII', io.read(0x14))
        assert dummy == 0

        io.seek(-num * 0x118, os.SEEK_END)
        for i in range(num):
            f = {}
            f['name'] = self.__read_str(io)
            f['offset'], f['size'], f['state'], f['time'], f['dummy'] = unpack('<IIIQI', io.read(0x18))
            self.append(f)

        for f in self:
            io.seek(f['offset'], os.SEEK_SET)
            f['buf'] = io.read(f['size'])

    def save(self, io):
        self.__write_str(io, self.name)
        self.__write_str(io, self.path)
        io.write(pack('<IIHHII', len(self), len(self), self.sort, self.version, self.contains_subdirectories, 0))

        for f in self:
            f['offset'] = io.tell()
            f['size'] = len(f['buf'])
            io.write(f['buf'])

        for f in self:
            self.__write_str(io, f['name'])
            io.write(pack('<IIIQI', f['offset'], f['size'], f['state'], f['time'], f['dummy']))

    def __str__(self):
        s = [f'name: {self.name}',
             f'path: {self.path}',
             f'version: {self.version}',
             ]
        for i, f in enumerate(self):
            time_str = datetime(1601, 1, 1) + timedelta(microseconds=f['time'] / 10)
            s.append(f"{i:3d} {f['offset']:08x} {f['size']:08x} {f['name']:32s} {time_str}")
        return '\n'.join(s)

    def dump(self, index):
        f = self[index]
        name = os.path.join(self.path, f['name'])
        try:
            os.makedirs(os.path.split(name)[0])
        except BaseException:
            pass
        open(name, 'wb').write(f['buf'])

    def dump_all(self):
        for i in range(len(self)):
            self.dump(i)

    def append_file(self, name, buf):
        self.append({'name': name,
                     'buf': buf,
                     'state': 0,
                     'dummy': 0,
                     'time': int((11644473600 + time.time()) * 1e7)})


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", action="store", nargs=1)
    parser.add_argument("index", action="store", nargs="?")
    parser.add_argument("--dump_all", action="store_true", default=False)
    args = parser.parse_args()

    slf = Slf(open(args.name[0], 'rb'))
    if args.index:
        slf.dump(int(args.index))
    elif args.dump_all:
        slf.dump_all()
    else:
        print(slf)
