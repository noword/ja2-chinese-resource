#! /usr/bin/env python3
# coding=utf-8
from ja2 import Slf
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
