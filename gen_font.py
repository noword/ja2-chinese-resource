from PIL import Image, ImageFont, ImageDraw
from ja2 import Slf
from ja2 import Sti
import os

'''
free fonts:
https://github.com/andot/zfull-for-yosemite
https://github.com/adobe-fonts/source-han-mono
'''

SMALL_FONT = 'Zfull-GB.ttf'
BIG_FONT = 'Zfull-GB.ttf'

JOBS = (
    ('blockfont.sti', SMALL_FONT, 8),
    ('BLOCKFONT2.sti', SMALL_FONT, 8),
    ('BLOCKFONTNARROW.sti', SMALL_FONT, 8),
    ('CLOCKFONT.sti', BIG_FONT, 15),
    ('COMPFONT.sti', SMALL_FONT, 8),
    ('FONT10ARIAL.sti', BIG_FONT, 9),
    ('FONT10ARIALBOLD.sti', BIG_FONT, 9),
    ('FONT10ROMAN.sti', SMALL_FONT, 8),
    ('FONT12ARIAL.sti', BIG_FONT, 11),
    ('FONT12ARIALFIXEDWIDTH.sti', BIG_FONT, 11),
    ('FONT12POINT1.sti', BIG_FONT, 11),
    ('FONT12ROMAN.sti', BIG_FONT, 9),
    ('FONT14ARIAL.sti', BIG_FONT, 13),
    ('FONT14HUMANIST.sti', BIG_FONT, 15),
    ('FONT14SANSERIF.sti', BIG_FONT, 11),
    ('FONT14SANSSERIF.sti', BIG_FONT, 11),
    ('FONT16ARIAL.sti', BIG_FONT, 15),
    ('HUGEFONT.sti', BIG_FONT, 17),
    ('LARGEFONT1.sti', BIG_FONT, 13),
    ('MERCFONT.sti', BIG_FONT, 14),
    ('SMALLCOMPFONT.sti', SMALL_FONT, 8),
    ('SMALLFONT1.sti', BIG_FONT, 10),
    ('TINYFONT1.sti', BIG_FONT, 9),
)


def load_text(name, encoding='utf-8'):
    text = []
    for line in open(name, encoding=encoding):
        line = line.strip('\n')
        assert len(line) == 1
        text.append(line)
    return text


class FontCache(dict):
    def get(self, ttf, size, char):
        key = ttf + str(size) + char
        return super().get(key)

    def set(self, ttf, size, char, image):
        key = ttf + str(size) + char
        self[key] = image


def gen_m_table(texts, name='m_table.cc'):
    with open(name, 'w', encoding='utf-8') as fp:
        for i, t in enumerate(texts):
            if ord(t) < 0x7f:
                fp.write(f"\t\tm_table[L'{t}'] = {i};\n")
            else:
                fp.write(f"\t\tm_table[{ord(t)}] = {i}; // {t}\n")


ADJUST = 1

if __name__ == '__main__':
    texts = load_text('ENGLISH.txt') + load_text('GB2312_Level1.txt') + load_text('OTHERS.txt')
    assert len(texts) == len(set(texts))
    gen_m_table(texts)
    image = Image.new('L', (128, 128))
    draw = ImageDraw.Draw(image)
    slf = Slf(name='FONTS.SLF', path='fonts\\')
    cache = FontCache()
    for name, ttf, size in JOBS:
        print(name, ttf, size)
        sti = Sti()
        font = ImageFont.FreeTypeFont(ttf, size=size + ADJUST)
        for t in texts:
            img = cache.get(ttf, size, t)
            if img is None:
                left, top, right, bottom = font.getbbox(t)
                draw.rectangle((0, 0, right, bottom), fill=0)
                draw.text((0, 0), t, font=font, fill=255)
                img = image.crop((0, 0, right, bottom))
                img = img.point(lambda x: 0 if x < 10 else x)
                cache.set(ttf, size, t, img)
            sti.append({'image': img})
        # sti.save(open(name, 'wb'))
        slf.append_file(name, sti.getvalue())
    try:
        os.makedirs('out/Data')
    except BaseException:
        pass
    slf.save(open('out/Data/Fonts.slf', 'wb'))
