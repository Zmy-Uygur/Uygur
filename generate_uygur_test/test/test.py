# -*- coding: utf-8 -*-
import random
from PIL import ImageFont, Image, ImageDraw
import os
import cv2
import numpy as np
from random import choice
import pygame

chars = ["ئا", "ئە", "ئو", "ئۈ", "ئۇ", "ئۆ", "ئى", "ئې", "د", "ر",
         "ز", "ۋ", "ژ", "ن", "ت", "ب", "پ", "م", "ھ", "غ",
         "س", "ش", "ف", "ق", "خ", "ج", "چ", "ك", "ڭ", "گ",
         "ي", "ل", "ا", "ە", "و", "ۈ", "ۇ", "ۆ", "ى", "ې", " "]

def genUygur(fontPath, outputPath, num):
    outimgpath = os.path.join(outputPath, 'img')
    outtxtpath = os.path.join(outputPath, 'TXT')
    if (not os.path.exists(outputPath)):
        os.mkdir(outputPath)
    if (not os.path.exists(outimgpath)):
        os.mkdir(outimgpath)
    if (not os.path.exists(outtxtpath)):
        os.mkdir(outtxtpath)

    seed = random.randint(2, 25)
    genChar = str()
    char_list = []
    for i in range(seed - 1):
        char = choice(chars)
        genChar += char
        char_list.append(char)
    #print(seed, len(genChar), genChar)

    newChar = str()
    for i in range(len(char_list)-1, -1, -1):
        newChar += char_list[i]
    #print(seed, len(newChar), newChar)
    font = ImageFont.truetype(fontPath, 18)
    w, h = font.getsize(newChar)
    im = Image.new("RGB", (w+10, h+5), (255,255,255))
    draw = ImageDraw.Draw(im)
    draw.text((5,2), newChar, font=font, fill="#000000")
    imgpath = os.path.join(outimgpath, str(num)) + '.jpg'
    im.save(imgpath)

    # pygame.init()
    # text = u"{0}".format(newChar)
    # font = pygame.font.Font(fontPath, random.randint(10, 30))
    # rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    # imgpath = os.path.join(outimgpath, str(num)) + '.png'
    # pygame.image.save(rtext, imgpath)


if __name__ == '__main__':
    bgDir = "./bg/"
    fontsDir = "./fonts/"
    outputDir = "./generated-data/"
    print('Loading Font and Data......\n')
    fontFiles = os.walk(fontsDir)
    numFonts = 0
    for root, dirs, files in fontFiles:
        fonts = files

    bgFiles = os.walk(bgDir)
    numBgs = 0
    for root, dirs, files in bgFiles:
        bgs = files

    print('There will be ', len(fonts), 'bg images, ', len(bgs), ' Fonts in this run.\n')

    for i in range(10):
        fontPath = os.path.join(fontsDir, choice(fonts))
        bgPath = os.path.join(bgDir, choice(bgs))
        outputPath = os.path.join(outputDir, '20200212')
        print(fontPath, bgPath, outputPath, '\n')
        genUygur(fontPath, outputPath, i)
