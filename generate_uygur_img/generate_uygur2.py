# -*- coding:utf-8 -*-
import pygame
import os
from PIL import Image, ImageFont, ImageDraw

# path = 'D:/FH/Uygur/Code/Uygur.txt'
# with open(path, 'r', encoding="utf-8-sig") as f:
#     lines = f.readlines()
#     f.close()
#     char_list = [line[:-1] for line in lines]  # 维语40个基础字符
#     print(len(char_list), char_list)

char = u'القارة الأورشبح ، شبح الشيوعية ، وبية يتجول في جميع أنحاء'

im = Image.new("RGB", (800, 50), (255, 255, 255))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype(os.path.join("D:/FH/Uygur/Font", "ARIALUNI.TTF"), 20)
char_list = [i for i in char]
new_char = str()
for i in range(len(char_list)-1, -1, -1):
    new_char += char_list[i]
dr.text((40, 8), new_char, font=font, fill="#000000")
im.show()
im.save('output2.png')

# pygame.init()  # 初始化
#
# # 引用变量使用字符串格式化
# text = u"{0}".format(char)
#
# # 字体
# font = pygame.font.Font(os.path.join("D:/FH/Uygur/Font/", "ARIALUNI.TTF"), 26)
#
# # 位置,颜色
# rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
#
# # 存储
# pygame.image.save(rtext, "D:/FH/Uygur/Code/output2.png")
