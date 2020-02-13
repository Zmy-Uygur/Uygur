# -*- coding: utf-8 -*-
from bidi.algorithm import get_display
import arabic_reshaper


def make_farsi_text(x):
    # 针对维语的特殊性，确保维语显示顺序正确
    # arabic_reshaper包是根据不同位置时的编码来切割维文
    reshaped_text = arabic_reshaper.reshape(x)
    farsi_text = get_display(reshaped_text)
    return farsi_text


def create_strings_from_file(filename, count, lang):
    """
        Create all strings by reading lines in specified files
    """
    strings = []

    with open('dicts/' + filename, 'r', encoding="utf8") as f:
        lines = [l.strip()[0:200] for l in f.readlines()]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            # 根据维文词列表相对于生成的图片数切片
            if len(lines) < count - len(strings):
                lines_fa = [make_farsi_text(l) for l in lines]
                strings.extend(lines_fa)
            else:
                lines_fa = [make_farsi_text(l) for l in lines[0:count - len(strings)]]
                strings.extend(lines_fa)

    return strings
