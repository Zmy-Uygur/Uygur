# -*- coding: utf-8 -*-
import freetype
import numpy
import matplotlib.pyplot as plt
import ArabicTextHelper as Arabic
import time


def FreeTypeDisplay(textArr=[], R=255, G=255, B=255):
    RGB = [('R', numpy.uint8), ('G', numpy.uint8), ('B', numpy.uint8)]
    face = freetype.Face('D:/FH/Uygur/Font/ARIALUNI.TTF')
    face.set_char_size(48 * 64)
    slot = face.glyph

    # 计算边框
    width, height, = 0, 0
    previous = 0
    # 计算总宽高
    for c in textArr:
        face.load_char(c)
        height = max(height, (face.size._FT_Size_Metrics.height >> 6))
        kerning = face.get_kerning(previous, c)
        width += (slot.advance.x >> 6) + (kerning.x >> 6)
        previous = c

    imgBuf = numpy.zeros((height, width), dtype=numpy.ubyte)
    colorBuf = numpy.zeros((height, width), dtype=RGB)

    # 渲染
    xBeg, yBeg = 0, 0
    previous = 0
    # 把每个字添加到imgBuf里
    for c in textArr:
        face.load_char(c)
        # 校正值
        descender = (-face.size._FT_Size_Metrics.descender) >> 6
        bitmap = slot.bitmap
        # 基线到字模顶部的距离
        top = slot.bitmap_top
        w = bitmap.width
        h = bitmap.rows
        yBeg = height - top - descender
        # 间隔
        kerning = face.get_kerning(previous, c)
        xBeg += (kerning.x >> 6)
        newChar = numpy.array(bitmap.buffer, dtype='ubyte').reshape(h, w)
        yEnd = yBeg + h
        xEnd = xBeg + w
        # 添加到imgBuf中
        imgBuf[yBeg:yEnd, xBeg:xEnd] += newChar
        xBeg += (slot.advance.x >> 6)
        previous = c

    FillColor(imgBuf, colorBuf, R, G, B)

    # 显示imgBuf
    plt.figure(figsize=(10, 10 * imgBuf.shape[0] / float(imgBuf.shape[1])))
    showing = colorBuf.view(dtype=numpy.uint8).reshape(colorBuf.shape[0], colorBuf.shape[1], 3)
    plt.imshow(showing, interpolation='nearest', origin='upper')
    plt.xticks([]), plt.yticks([])
    plt.imsave('output1.png', showing)
    plt.show()


def FillColor(srcBuf, colorBuf, R, G, B):
    rows = srcBuf.shape[0]
    columns = srcBuf.shape[1]
    for y in range(0, rows):
        for x in range(0, columns):
            if srcBuf[y][x] > 0:
                colorBuf[y][x] = (R, G, B)


def main():
    text = u'القارة الأورشبح ، شبح الشيوعية ، وبية يتجول في جميع أنحاء'
    # 处理原始字符串，生成转换后的数组
    textArr = Arabic.ArabicText.translate(text=text)
    # 显示转换后的数组
    FreeTypeDisplay(textArr, 0x33, 0xe4, 0xff)


if __name__ == '__main__':
    main()
