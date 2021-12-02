#! /usr/bin/env python3
# coding=utf-8
from PIL import Image, ImageFont, ImageDraw, ImagePalette
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

PALLETTE = bytes.fromhex('000000003600000000000000000000d6c99cad9473000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c9ac857b5b47000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000735a4a11b2d811b2d811b2d811b2d811b2d811b2d8634d2c11b2d811b2d811b2d811b2d8060202989898a9b892ffce1ef0742dd4692daf5e359a4c16a46013b76d15c06927c47b1ed39210cc9127a5a750888b42869f5f9c8769828e7c758466727554606a634f5c6630464c192433102c0439140126070010100a1e1c162e2a1a2f3d3045462b4e391b522f04633b077b3f0b74412160562d5a422a51473c45594759564b6a6440785c32805b1e906b238b6a399d744ba67e35b38e31be9047cfa957be9d67b2a876d2a97fd7bd6dc2bd70c9c58fe6b3a9f3f3f3d9d9d9bebebea4a4a48989896f6f6f5454543a3a3a1f1f1f050505fff4bcffe87fffd73fffc902dfb001bf9701a07e02806502604c03f0ffc8daff85c5ff43afff008cd50069ab00468200235800002e00ffc1c1ff8181ff4040ff0000cd00009b0000680000360000fffffff3e5abe7cc56dbb2027100005800003f0000372b0d2a2106231c031c17007a7a7a5c5c5c3e3e3e20202000ff0000ce0000790000480000230073634c64564256493840362a1b1611718a9363798155696f4050551d26284f5a2d444d273941212e341b13150b0000ff0000bc00009a000079000046ffffffdededea8a8a86262623e3e3eccb611b09d0f6b5f0b4f4609332d07b20f0f9a0d0d5e0a0a4508082d0606ffa382e78c68bf7b5c885237c28a77ad745ea16a528c5b4586573f6f49345b3b2a4c3123694a3a573d304430262f2019c4963bb68a338b661c7777775b5b5b3e3e3e8b3d036c34094d2b0f6a47004f3501332302282725201f1e080807ffffffff00ff')
CLOCK_PALLETTE = bytes.fromhex('000000210000420000630505840808a40d0dc61010e61414fd1717110101310101530202730808940b0bb40f0fd61313f215150900003900002902024a02025b03036b07077b07078b0b0b9c0c0cac0e0ebc1010ce11111700003e03034404044f05055506065c07077f0a0a850c0cdd1313ec1414f717171c00002600002c00004700004e01013502023903034a05056607076f09097709098f0a0a960e0ea00e0eb90e0eaf1010c11010b71111c91212d21212e114140400000c00001400003400003c00003f00001a02021e02024102024502023003034d03035603034704045204045805056005055907076207076e07075f08088008086c09097a0909890909820a0a860a0a900c0c970c0ca70d0db00e0ecc1313cf1313d91313e91414ef1515fa16160f00002900002f00003701012102023b02025002022b03034104045d04045b05055206065e0606770707690808710a0a880b0b8d0c0c8b0d0d940d0d990d0d9e0d0da90e0eb70f0fac1010b91010be1111c31111cb1111db1414e41515ed1616f41616ff18182c2417302817211e18271f182c20183425192d281a29211b24221b37281b2e1f1c32271c2b241d312d1e39331e3b2d1f322320332820352d203c31202624212e2522413522362b243a3324433824474025403526473c26392d273c36284a3a284c45284d412941352a53472b43382c4a3b2c4d472c4e422d56482e3d332f52492f483a30584c303e37314d42325548325b4c33474034564b354d46366053364943375547375c4d376556395d4d3c51463d6b5c3d0f0700060e000b12001212001613001e16001418001119002219002b1e001a20001d2000272b00452e002c2f004e35003436000c07020704040a05041009040f0c05160f050b0a060b0707100e071b0f070c0c08161209201409110c0a0e0d0a140d0a20150c140e0d23180d16120e19130e15150e1d160f1815102319101d1a10261e111c15121e1812251b12171613221813201d13272013261d141e1b15211f152622151a1916281c16251d172f2217000000585858989898d0d0d0ff0000')

# font name, ttf name, size, bold, pallette, color index0, color index 1
JOBS = (
    ('blockfont.sti', SMALL_FONT, 8, False, PALLETTE, 133, 1),
    ('BLOCKFONT2.sti', SMALL_FONT, 8, False, PALLETTE, 133, 1),
    ('BLOCKFONTNARROW.sti', SMALL_FONT, 8, False, PALLETTE, 133, 1),
    ('CLOCKFONT.sti', BIG_FONT, 15, False, CLOCK_PALLETTE, 7, 2),
    ('COMPFONT.sti', SMALL_FONT, 8, False, PALLETTE, 183, 1),
    ('FONT10ARIAL.sti', BIG_FONT, 9, False, PALLETTE, 254, 1),
    ('FONT10ARIALBOLD.sti', BIG_FONT, 9, True, PALLETTE, 254, 1),
    ('FONT10ROMAN.sti', SMALL_FONT, 8, False, PALLETTE, 183, 1),
    ('FONT12ARIAL.sti', BIG_FONT, 11, False, PALLETTE, 254, 1),
    ('FONT12ARIALFIXEDWIDTH.sti', BIG_FONT, 11, False, PALLETTE, 168, 1),
    ('FONT12POINT1.sti', BIG_FONT, 11, False, PALLETTE, 209, 1),
    ('FONT12ROMAN.sti', BIG_FONT, 9, False, PALLETTE, 183, 1),
    ('FONT14ARIAL.sti', BIG_FONT, 13, False, PALLETTE, 168, 1),
    ('FONT14HUMANIST.sti', BIG_FONT, 15, True, PALLETTE, 163, 1),
    ('FONT14SANSERIF.sti', BIG_FONT, 11, False, PALLETTE, 183, 1),
    ('FONT14SANSSERIF.sti', BIG_FONT, 11, False, PALLETTE, 183, 1),
    ('FONT16ARIAL.sti', BIG_FONT, 15, False, PALLETTE, 209, 1),
    ('HUGEFONT.sti', BIG_FONT, 17, True, PALLETTE, 183, 1),
    ('LARGEFONT1.sti', BIG_FONT, 13, False, PALLETTE, 211, 100),
    ('MERCFONT.sti', BIG_FONT, 14, False, PALLETTE, 168, 1),
    ('SMALLCOMPFONT.sti', SMALL_FONT, 8, False, PALLETTE, 168, 1),
    ('SMALLFONT1.sti', BIG_FONT, 10, False, PALLETTE, 211, 91),
    ('TINYFONT1.sti', BIG_FONT, 9, False, PALLETTE, 91, 1),
)


def load_text(name, encoding='utf-8'):
    text = []
    for line in open(name, encoding=encoding):
        line = line.strip('\n')
        assert len(line) == 1
        text.append(line)
    return text


def gen_m_table(texts, name='m_table.cc'):
    with open(name, 'w', encoding='utf-8') as fp:
        for i, t in enumerate(texts):
            if ord(t) < 0x7f:
                fp.write(f"\t\tm_table[L'{t}'] = {i};\n")
            else:
                fp.write(f"\t\tm_table[{ord(t)}] = {i}; // {t}\n")


ADJUST = 1
OUT_PATH = 'out/Data/Fonts'
if __name__ == '__main__':
    texts = load_text('ENGLISH.txt') + load_text('GB2312_Level1.txt') + load_text('OTHERS.txt')
    assert len(texts) == len(set(texts))
    gen_m_table(texts)
    image = Image.new('P', (128, 128))
    draw = ImageDraw.Draw(image)

    try:
        os.makedirs(OUT_PATH)
    except BaseException:
        pass

    for name, ttf, size, bold, palette, color0, color1 in JOBS:
        print(name, ttf, size)
        image.putpalette(ImagePalette.ImagePalette('RGB', palette, 256 * 3))
        sti = Sti()
        font = ImageFont.FreeTypeFont(ttf, size=size + ADJUST)
        for t in texts:
            if bold:
                left, top, right, bottom = font.getbbox(t)
                draw.rectangle((0, 0, right + 2, bottom + 1), fill=0)
                draw.text((1, 1), t, font=font, fill=color1)
                draw.text((2, 1), t, font=font, fill=color1)
                draw.text((0, 0), t, font=font, fill=color0)
                draw.text((1, 0), t, font=font, fill=color0)
                img = image.crop((0, 0, right + 2, bottom + 1))
            else:
                left, top, right, bottom = font.getbbox(t)
                draw.rectangle((0, 0, right + 1, bottom + 1), fill=0)
                draw.text((1, 1), t, font=font, fill=color1)
                draw.text((0, 0), t, font=font, fill=color0)
                img = image.crop((0, 0, right + 1, bottom + 1))
            if t == 'A':
                w, h = img.size
                img = img.crop((0, 1, w, h - 1))
                print(size, img.size[1])
            sti.append({'image': img})
        sti.save(open(os.path.join(OUT_PATH, name), 'wb'))
