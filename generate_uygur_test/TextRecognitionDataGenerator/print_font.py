# -*- coding:utf-8 -*-
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from tqdm import tqdm
import os
import random
from bidi.algorithm import get_display
import arabic_reshaper

font_dir = r'./fonts/uygur'
out_dir = r'fonts_test'

# 常用字
char1 = "خ ج چ ك ڭ گ ي ل ا ە و ۈ ۇ ۆ ى ې ؟ ! ، . > < _ - |"
char2 = "ئا ئە ئو ئۈ ئۇ ئۆ ئى ئې د ر ز ۋ ژ ن ت پ م غ س ش ف ق"
#char_list2 = "ئا ئە ئو ئۈ ئۇ ئۆ ئى ئې د ر ز ۋ ژ ن ت پ م غ س ش ف ق خ ج چ ك ڭ گ ي ل ا ە و ۈ ۇ ۆ ى ې"


def make_farsi_text(x):
    # 针对维语的特殊性，确保维语显示顺序正确
    # arabic_reshaper包是根据不同位置时的编码来切割维文
    reshaped_text = arabic_reshaper.reshape(x)
    farsi_text = get_display(reshaped_text)
    return farsi_text

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

font_files = os.listdir(font_dir)

for font_file in tqdm(font_files):
    space_width = 1
    f_path = os.path.join(font_dir, font_file)
    # 设置字体，字间，颜色，尺寸
    image_font = ImageFont.truetype(font=f_path, size=40)
    words = make_farsi_text(char2)
    print(words)
    space_width = image_font.getsize(' ')[0] * space_width

    words_width = [image_font.getsize(w)[0] for w in words]
    text_width = sum(words_width) + int(space_width) * (len(words) - 1)
    text_height = max([image_font.getsize(w)[1] for w in words])

    txt_img = Image.new('RGB', (text_width, text_height), (0, 0, 0))

    txt_draw = ImageDraw.Draw(txt_img)

    color_def = "#282828"

    colors = [ImageColor.getrgb(c) for c in color_def.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (random.randint(c1[0], c2[0]),
            random.randint(c1[1], c2[1]),
            random.randint(c1[2], c2[2]))

    for i, w in enumerate(words):
        txt_draw.text((sum(words_width[0:i]) + i * int(space_width), 0), w, fill=fill, font=image_font)

    #background = Image.new("L", (2000, 400), 255).convert('RGB')
    #background.paste(txt_draw, (5, 5), txt_draw)
    txt_img.save(out_dir + '/' + font_file + '.jpg')
