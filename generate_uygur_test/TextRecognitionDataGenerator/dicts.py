# -*- coding: utf-8 -*-

# with open('dicts/' + 'sahardike nikah.txt', 'r', encoding="utf-8-sig") as f:
#     #print(f.readlines())
#     lines = []
#     for l in f.readlines():
#         print(l.strip()[0:100])
#         lines.append(l.strip()[0:100])
#     #lines = [l.strip()[0:200] for l in f.readlines()]
#     if len(lines) == 0:
#         raise Exception("No lines could be read in file")
#     print(lines)
#     while '' in lines:
#         lines.remove('')
#     print(lines)



import random
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


# text_color = '#282828'
text_color = randomcolor()
colors = []
for c in text_color.split(','):
    colors.append(ImageColor.getrgb(c))
# colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
c1, c2 = colors[0], colors[-1]

fill = (random.randint(c1[0], c2[0]),
        random.randint(c1[1], c2[1]),
        random.randint(c1[2], c2[2]))
print(fill)
