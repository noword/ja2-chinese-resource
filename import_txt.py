#! /usr/bin/env python3
# coding=utf-8
from ja2 import EdtFactory
from translation import Translation
from pathlib import Path
import os
import sys


def load_text(name, encoding='utf-8'):
    text = []
    for line in open(name, encoding=encoding):
        line = line.strip('\n')
        assert len(line) == 1
        text.append(line)
    return text


OUT_PATH = 'out/Data'
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    tanslation = Translation('ja2.xlsx')
    for t in tanslation.check_variables(r'\[[A-Z]+?\](?=\s|$)', 'English', 'Chinese'):
        print('\n'.join([str(x) for x in t]), '\n')
    for t in tanslation.check_variables(r'\$[A-Z]+?\$', 'English', 'Chinese'):
        print('\n'.join([str(x) for x in t]), '\n')

    trans = tanslation.get_translation(index='English')
    texts = set()
    for t in trans.values():
        texts |= set(t['Chinese'])

    font_texts = load_text('ENGLISH.txt') + load_text('OTHERS.txt') + load_text('GB2312_Level1.txt')
    for t in texts:
        if t not in font_texts:
            print('not in font:', t)

    for name in Path('eng').rglob('*.edt'):
        print(name)
        edt = EdtFactory(name)
        for f in edt:
            for i, ff in enumerate(f):
                if len(ff) > 0:
                    if ff in trans:
                        f[i] = trans[ff]['Chinese']
                    else:
                        print(f'missing translation: {ff}')

        new_name = str(name).replace('eng', OUT_PATH, 1)
        try:
            os.makedirs(os.path.split(new_name)[0])
        except BaseException:
            pass
        edt.save(open(new_name, 'wb'))
