# -*- coding: utf-8 -*-
class ArabicText(object):
    # first, last, middle, alone
    __arabic_Positions = [[0xfe80, 0xfe80, 0xfe80, 0xfe80],  # 0x621
                          [0xfe82, 0xfe81, 0xfe82, 0xfe81],
                          [0xfe84, 0xfe83, 0xfe84, 0xfe83],
                          [0xfe86, 0xfe85, 0xfe86, 0xfe85],
                          [0xfe88, 0xfe87, 0xfe88, 0xfe87],
                          [0xfe8a, 0xfe8b, 0xfe8c, 0xfe89],
                          [0xfe8e, 0xfe8d, 0xfe8e, 0xfe8d],
                          [0xfe90, 0xfe91, 0xfe92, 0xfe8f],  # 0x628
                          [0xfe94, 0xfe93, 0xfe94, 0xfe93],
                          [0xfe96, 0xfe97, 0xfe98, 0xfe95],  # 0x62A
                          [0xfe9a, 0xfe9b, 0xfe9c, 0xfe99],
                          [0xfe9e, 0xfe9f, 0xfea0, 0xfe9d],
                          [0xfea2, 0xfea3, 0xfea4, 0xfea1],
                          [0xfea6, 0xfea7, 0xfea8, 0xfea5],
                          [0xfeaa, 0xfea9, 0xfeaa, 0xfea9],
                          [0xfeac, 0xfeab, 0xfeac, 0xfeab],  # 0x630
                          [0xfeae, 0xfead, 0xfeae, 0xfead],
                          [0xfeb0, 0xfeaf, 0xfeb0, 0xfeaf],
                          [0xfeb2, 0xfeb3, 0xfeb4, 0xfeb1],
                          [0xfeb6, 0xfeb7, 0xfeb8, 0xfeb5],
                          [0xfeba, 0xfebb, 0xfebc, 0xfeb9],
                          [0xfebe, 0xfebf, 0xfec0, 0xfebd],
                          [0xfec2, 0xfec3, 0xfec4, 0xfec1],
                          [0xfec6, 0xfec7, 0xfec8, 0xfec5],  # 0x638
                          [0xfeca, 0xfecb, 0xfecc, 0xfec9],
                          [0xfece, 0xfecf, 0xfed0, 0xfecd],  # 0x63A
                          [0x63b, 0x63b, 0x63b, 0x63b],
                          [0x63c, 0x63c, 0x63c, 0x63c],
                          [0x63d, 0x63d, 0x63d, 0x63d],
                          [0x63e, 0x63e, 0x63e, 0x63e],
                          [0x63f, 0x63f, 0x63f, 0x63f],
                          [0x640, 0x640, 0x640, 0x640],  # 0x640
                          [0xfed2, 0xfed3, 0xfed4, 0xfed1],
                          [0xfed6, 0xfed7, 0xfed8, 0xfed5],
                          [0xfeda, 0xfedb, 0xfedc, 0xfed9],
                          [0xfede, 0xfedf, 0xfee0, 0xfedd],
                          [0xfee2, 0xfee3, 0xfee4, 0xfee1],
                          [0xfee6, 0xfee7, 0xfee8, 0xfee5],
                          [0xfeea, 0xfeeb, 0xfeec, 0xfee9],
                          [0xfeee, 0xfeed, 0xfeee, 0xfeed],  # 0x648
                          [0xfef0, 0xfef3, 0xfef4, 0xfeef],
                          [0xfef2, 0xfef3, 0xfef4, 0xfef1]]  # 0x64A

    __preSet = [0x62c, 0x62d, 0x62e, 0x647, 0x639, 0x63a, 0x641, 0x642,
                0x62b, 0x635, 0x636, 0x637, 0x643, 0x645, 0x646, 0x62a,
                0x644, 0x628, 0x64a, 0x633, 0x634, 0x638, 0x626, 0x640]

    __nextSet = [0x62c, 0x62d, 0x62e, 0x647, 0x639, 0x63a, 0x641, 0x642,
                 0x62b, 0x635, 0x636, 0x637, 0x643, 0x645, 0x646, 0x62a,
                 0x644, 0x628, 0x64a, 0x633, 0x634, 0x638, 0x626,
                 0x627, 0x623, 0x625, 0x622, 0x62f, 0x630, 0x631, 0x632,
                 0x648, 0x624, 0x629, 0x649, 0x640]
    __replaceSet = [[0xFEF5, 0xFEF6], [0xFEF7, 0xFEF8], [0xFEF9, 0xFEFA], [0xFEFB, 0xFEFC]]

    # 将传入的字符串转换为显示时的数组，显示时用FreeType直接取数组中的每一个值进行排版显示
    # 字符串倒置返回
    @staticmethod
    def translate(text):
        retArr = []
        textLen = len(text)
        lastIdx = -3  # 上一个非维文字符下标
        begIdxs = []  # 非维文字符串下标集合
        endIdxs = []

        for i in range(0, textLen):
            charCode = ord(text[i])
            # print(i,charCode)
            # 非维文时，直接添加
            if charCode not in range(0x621, 0x6ff):
                retArr.append(charCode)
                arrLen = len(retArr)
                # 不连续
                if arrLen - 1 != lastIdx + 1:
                    begIdxs.append(arrLen - 1)
                    # 最后一个字符非维文
                if i == textLen - 1:
                    endIdxs.append(arrLen - 1)
                lastIdx = arrLen - 1
                continue
            else:
                arrLen = len(retArr)
                # 当前维文字符的前一个字符非维文时
                if lastIdx == arrLen - 2:
                    endIdxs.append(lastIdx)

            # ----rule 1----
            # 前一个字符的Unicode码
            pre_Ch = (0 if (i == 0) else ord(text[i - 1]))
            # 当前字符的Unicode码
            Ch = charCode
            # 后一个字符的Unicode码
            next_Ch = (0 if (i == (textLen - 1)) else ord(text[i + 1]))
            val = ArabicText.__GetTransform(pre_Ch, Ch, next_Ch)
            retArr.append(val)
            # ----rule 2----
            replace = ArabicText.__GetContinuousWriting(pre_Ch, Ch, next_Ch)
            if replace > 0:
                retArr.append(replace)
                i = i + 2
        # 结果反过来从右往左显示
        retArr.reverse()
        ArabicText.__NonArabicReverse(retArr, begIdxs, endIdxs)
        return retArr

    # 非维文字符不用反转，再反回来
    @classmethod
    def __NonArabicReverse(cls, charArr=[], begIdxs=[], endIdxs=[]):
        lastIdx = len(charArr) - 1  # 最后一个下标
        loopCnt = len(begIdxs)
        for i in range(0, loopCnt):
            beg = (lastIdx - endIdxs[i])
            end = (lastIdx - begIdxs[i])
            switchTimes = int((end + 1 - beg) / 2)
            for j in range(0, switchTimes):
                temp = charArr[beg + j]
                charArr[beg + j] = charArr[end - j]
                charArr[end - j] = temp

    # 处理连写字符 某些情况下需要将后续两个字符替换成其他字符
    @classmethod
    def __GetContinuousWriting(cls, preCh=0, ch=0, nextCh=0):
        retVal = 0
        nextChArr = [0x622, 0x623, 0x625, 0x627]
        positionIdx = -1
        charIdx = 0
        if (ch == 0x644) and (nextCh in nextChArr):
            charIdx = nextChArr.index(nextCh)
            if preCh in cls.__preSet:
                positionIdx = 1
            else:
                positionIdx = 0
            retVal = cls.__replaceSet[charIdx][positionIdx]
        return retVal

    # 处理字符因前连写后连写的变形
    @classmethod
    def __GetTransform(cls, pre_Ch=0, Ch=0, next_Ch=0):
        preConnect = False
        nextConnect = False
        positionIdx = -1
        charIdx = 0
        # 是前连字符
        if pre_Ch in cls.__preSet:
            preConnect = True
            positionIdx = 0
        # 是后连字符
        if next_Ch in cls.__nextSet:
            nextConnect = True
            positionIdx = 1
        # 既是前连又是后连，双连式
        if preConnect and nextConnect:
            positionIdx = 2
        # 不是前连又不是后连，独立式
        elif (preConnect == False) and (nextConnect == False):
            positionIdx = 3
        charIdx = Ch - 0x621
        retVal = cls.__arabic_Positions[charIdx][positionIdx]
        return retVal
