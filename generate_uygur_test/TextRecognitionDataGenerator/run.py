# -*- coding: utf-8 -*-
import argparse
import os, errno
import random

from tqdm import tqdm
from string_generator import create_strings_from_file, make_farsi_text
from data_generator import FakeTextDataGenerator
from multiprocessing import Pool


def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(description='Generate synthetic text data for text recognition.')
    parser.add_argument("--output_dir",
                        type=str,
                        nargs="?",
                        help="The output directory",
                        default="output/")
    parser.add_argument("-i",
                        "--input_file",
                        type=str,
                        nargs="?",
                        help="When set, this argument uses a specified text file as source for the text",
                        default="sahardike nikah.txt")

    parser.add_argument("-l",
                        "--language",
                        type=str,
                        nargs="?",
                        help="The language to use, should be fr (French), en (English), es (Spanish), de (German), or cn (Chinese).",
                        default="uygur")
    parser.add_argument("-c",
                        "--count",
                        type=int,
                        nargs="?",
                        help="The number of images to be created.",
                        default=1000)
    parser.add_argument("-w",
                        "--length",
                        type=int,
                        nargs="?",
                        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
                        default=5)
    parser.add_argument("-f",
                        "--format",
                        type=int,
                        nargs="?",
                        help="Define the height of the produced images if horizontal, else the width",
                        default=45)
    parser.add_argument("-t",
                        "--thread_count",
                        type=int,
                        nargs="?",
                        help="Define the number of thread to use for image generation",
                        default=1)
    parser.add_argument("-e",
                        "--extension",
                        type=str,
                        nargs="?",
                        help="Define the extension to save the image with",
                        default="jpg")
    # 生成文本的倾斜角度最大范围
    parser.add_argument("-k",
                        "--skew_angle",
                        type=int,
                        nargs="?",
                        help="Define skewing angle of the generated text. In positive degrees",
                        default=5)
    # 倾斜角度是否在+-skew_angle间随机变化
    parser.add_argument("-rk",
                        "--random_skew",
                        action="store_true",
                        help="When set, the skew angle will be randomized between the value set with -k and it's opposite",
                        default=True)
    parser.add_argument("-bl",
                        "--blur",
                        type=int,
                        nargs="?",
                        help="Apply gaussian blur to the resulting sample. Should be an integer defining the blur radius",
                        default=1)
    parser.add_argument("-rbl",
                        "--random_blur",
                        action="store_true",
                        help="When set, the blur radius will be randomized between 0 and -bl.",
                        default=True)
    # 背景图片类型，0：高斯，1：白色，2：凸晶体，3：图片
    parser.add_argument("-b",
                        "--background",
                        type=int,
                        nargs="?",
                        help="Define what kind of background to use. 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Pictures",
                        default=3)
    parser.add_argument("-hw",
                        "--handwritten",
                        action="store_true",
                        help="Define if the data will be \"handwritten\" by an RNN")
    # 生成文件格式
    parser.add_argument("-na",
                        "--name_format",
                        type=int,
                        help="Define how the produced files will be named. "
                             "0:[TEXT]_[ID].[EXT], 1:[ID]_[TEXT].[EXT] 2:[ID].[EXT] + one file labels.txt containing id-to-label mappings",
                        default=2)
    # 增强之形变，0：无，1：正弦，2：余弦，3：随机
    parser.add_argument("-d",
                        "--distorsion",
                        type=int,
                        nargs="?",
                        help="Define a distorsion applied to the resulting image. 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random",
                        default=3)
    # 变形方向，0：上下，1：左右，2：都变
    parser.add_argument("-do",
                        "--distorsion_orientation",
                        type=int,
                        nargs="?",
                        help="Define the distorsion's orientation. Only used if -d is specified. 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both",
                        default=2)
    # 结果图像宽度，未设置：为文本宽度+10，生成文本的宽度较大：使用该数字
    parser.add_argument("-wd",
                        "--width",
                        type=int,
                        nargs="?",
                        help="Define the width of the resulting image. If not set it will be the width of the text + 10. If the width of the generated text is bigger that number will be used",
                        default=0)
    # 图像中文本的对齐方式，0：左，1：中，2：右
    parser.add_argument("-al",
                        "--alignment",
                        type=int,
                        nargs="?",
                        help="Define the alignment of the text in the image. Only used if the width parameter is set. 0: left, 1: center, 2: right",
                        default=1)
    # 文本方向，0：水平，1：垂直
    parser.add_argument("-or",
                        "--orientation",
                        type=int,
                        nargs="?",
                        help="Define the orientation of the text. 0: Horizontal, 1: Vertical",
                        default=0)
    # 文本颜色
    parser.add_argument("-tc",
                        "--text_color",
                        type=str,
                        nargs="?",
                        help="Define the text's color, True:random, False:.",
                        default=True)
    # 单词之间空格的宽度
    parser.add_argument("-sw",
                        "--space_width",
                        type=float,
                        nargs="?",
                        help="Define the width of the spaces between words. 2.0 means twice the normal space width",
                        default=round(random.uniform(0.8, 1.2), 2))

    return parser.parse_args()


def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """
    return [os.path.join('fonts/' + lang, font) for font in os.listdir('fonts/' + lang)]


def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # 输出目录
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # 字体列表
    fonts = load_fonts(args.language)

    # 从txt中创建合成指定数量count个词句
    strings = []
    if args.input_file != '':
        strings = create_strings_from_file(args.input_file, args.count, args.language)
    string_count = len(strings)
    # 多线程，进度条提示信息
    p = Pool(args.thread_count)
    for _ in tqdm(p.imap_unordered(
            FakeTextDataGenerator.generate_from_tuple,  ## FakeTextDataGenerator样本生成主干部分
            zip(
                [i for i in range(0, string_count)],
                strings,
                [fonts[random.randrange(0, len(fonts))] for _ in range(0, string_count)],
                [args.output_dir] * string_count,
                [args.format] * string_count,
                [args.extension] * string_count,
                [args.skew_angle] * string_count,
                [args.random_skew] * string_count,
                [args.blur] * string_count,
                [args.random_blur] * string_count,
                [args.background] * string_count,
                [args.distorsion] * string_count,
                [args.distorsion_orientation] * string_count,
                [args.handwritten] * string_count,
                [args.name_format] * string_count,
                [args.width] * string_count,
                [args.alignment] * string_count,
                [args.text_color] * string_count,
                [args.orientation] * string_count,
                [args.space_width] * string_count
            )
    ), total=args.count):
        pass
    p.terminate()


    if args.name_format == 2:
        # 图片对应文本批量写入txt
        with open(os.path.join(args.output_dir, "labels.txt"), 'w', encoding="utf8") as f:
            for i in range(string_count):
                text = make_farsi_text(strings[i])
                file_name = str(i) + "." + args.extension
                f.write("{} {}\n".format(file_name.split('.')[0], text))


if __name__ == '__main__':
    main()
