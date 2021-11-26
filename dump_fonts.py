#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import pathlib
from ja2 import Sti
from PIL import Image, ImageDraw


def get_font_image(sti, size=(256, 256)):
    image = Image.new('P', size)
    image.putpalette(sti.palette)
    x = y = 0
    max_h = 0
    for f in sti:
        img = f['image']
        w, h = img.size
        max_h = max(max_h, h)
        if x + w + 1 > size[0]:
            x = 0
            y += max_h + 2
        image.paste(img, (x, y))
        x += w + 1
    return image


def get_font_palette(sti, size=(1024, 1024)):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    w, h = size
    _w, _h = w // 16, h // 16
    palette = sti.palette.tobytes()
    for i in range(len(palette) // 3):
        r, g, b = palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]
        bg = (r, g, b)
        fg = (256 - r, 256 - g, 256 - b)
        x = i % 16 * _w
        y = i // 16 * _h
        if y > h:
            break
        draw.rectangle((x, y, x + _w, y + _h), fill=bg)
        draw.text((x, y), f'{i}\n#{r:02x}{g:02x}{b:02x}', fill=fg)

    return img


if __name__ == '__main__':
    import sys
    for f in Path(sys.argv[1]).glob('*.sti'):
        print(f)
        sti = Sti(open(f, 'rb'))
        print(set(sti[0]['image'].tobytes()))
        im = get_font_image(sti).save(f.stem + '.png')
        get_font_palette(sti).save(f.stem + '.pal.png')
