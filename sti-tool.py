#! /usr/bin/env python3
# coding=utf-8
from ja2 import Sti
import os
import argparse


def dump(sti, index, name):
    img = sti[index]['image']
    img.save(f'{name}_{index}.png')


def dump_all(sti, name):
    for i in range(len(sti)):
        dump(sti, i, name)


parser = argparse.ArgumentParser()
parser.add_argument("name", action="store", nargs=1)
parser.add_argument("index", action="store", nargs="?")
parser.add_argument("--dump_all", action="store_true", default=False)
args = parser.parse_args()

sti = Sti(open(args.name[0], 'rb'))
if args.index:
    dump(sti, int(args.index), os.path.splitext(args.name[0])[0])
elif args.dump_all:
    dump_all(sti, os.path.splitext(args.name[0])[0])
else:
    print(sti)
