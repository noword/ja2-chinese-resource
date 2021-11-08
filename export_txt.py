#! /usr/bin/env python3
# coding=utf-8
from ja2 import EdtFactory
from translation import Translation
import pathlib


def get_pure_name(name):
    return ('/'.join(str(name).replace('\\', '/').split('/')[1:])).upper()


if __name__ == '__main__':
    trans = {}
    for name in pathlib.Path('chs').rglob('*.edt'):
        edt = EdtFactory(name)
        pure_name = get_pure_name(name)
        for i, f in enumerate(edt):
            for j, ff in enumerate(f):
                ff = ff.replace('\x1f', ' ')
                trans[f'{pure_name}{i}{j}'] = ff

    data = []
    for name in pathlib.Path('eng').rglob('*.edt'):
        edt = EdtFactory(name)
        pure_name = get_pure_name(name)
        print(pure_name)
        for i, f in enumerate(edt):
            for j, ff in enumerate(f):
                if len(ff):
                    data.append({'Name': pure_name, 'English': ff, 'Chinese': trans.get(f'{pure_name}{i}{j}', '')})

    translation = Translation()
    translation.set_data(data, ('Name', 'English', 'Chinese'))
    translation.save('ja2_export.xlsx')
