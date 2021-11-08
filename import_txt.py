#! /usr/bin/env python3
# coding=utf-8
from ja2 import EdtFactory
from translation import Translation
from pathlib import Path
import os

OUT_PATH = 'out/Data'
if __name__ == '__main__':
    tanslation = Translation('ja2.xlsx')
    for t in tanslation.check_variables(r'\[[A-Z]+?\]', 'English', 'Chinese'):
        print(t)

    trans = tanslation.get_translation(index='English')
    for name in Path('eng').rglob('*.edt'):
        print(name)
        edt = EdtFactory(name)
        for f in edt:
            for i, ff in enumerate(f):
                if ff in trans:
                    f[i] = trans[ff]['Chinese']

        new_name = str(name).replace('eng', OUT_PATH, 1)
        try:
            os.makedirs(os.path.split(new_name)[0])
        except BaseException:
            pass
        edt.save(open(new_name, 'wb'))
