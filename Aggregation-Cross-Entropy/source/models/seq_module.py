# -*- coding: utf-8 -*-
import math
import torch
import random
import itertools
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class Sequence(nn.Module):
    def __init__(self):
        super(Sequence, self).__init__()

    def result_analysis(self, iteration):
        pass


class ACE(Sequence):

    def __init__(self, dictionary):
        super(ACE, self).__init__()
        self.softmax = None
        self.label = None
        self.dict = dictionary

    def forward(self, input, label):

        self.bs, self.h, self.w, _ = input.size()
        T_ = self.h * self.w

        # tensor维度展开
        input = input.view(self.bs, T_, -1)
        input = input + 1e-10

        self.softmax = input
        label[:, 0] = T_ - label[:, 0]
        self.label = label

        # ACE的实现：四个基本公式
        input = torch.sum(input, 1)  # 概率求和
        input = input / T_  # 累计概率标准化
        label = label / T_  # 将标签标注为所有类的概率分布
        loss = (-torch.sum(torch.log(input) * label)) / self.bs  # 交叉熵比较以上两步概率分布

        return loss

    def decode_batch(self):
        # 取最大值，张量转numpy
        out_best = torch.max(self.softmax, 2)[1].data.cpu().numpy()
        pre_result = [0] * self.bs
        for j in range(self.bs):
            pre_result[j] = out_best[j][out_best[j] != 0]
        return pre_result

    def vis(self, iteration):
        sn = random.randint(0, self.bs - 1)
        print('Test image %4d:' % (iteration * 50 + sn))

        pred = torch.max(self.softmax, 2)[1].data.cpu().numpy()
        pred = pred[sn].tolist()  # sample #0
        pred_string = ''.join(['%2s' % self.dict[pn] for pn in pred])
        pred_string_set = [pred_string[i:i + self.w * 2] for i in range(0, len(pred_string), self.w * 2)]
        print('Prediction: ')
        for pre_str in pred_string_set:
            print(pre_str)
        label = ''.join(
            ['%2s:%2d' % (self.dict[idx], pn) for idx, pn in enumerate(self.label[sn]) if idx != 0 and pn != 0])
        label = 'Label: ' + label
        print(label)

    def result_analysis(self, iteration):
        prediction = self.decode_batch()
        correct_count = 0
        pre_total = 0
        len_total = self.label[:, 1:].sum()
        label_data = self.label.data.cpu().numpy()
        # 从每张图片的预测结果中获取每个字符
        for idx, pre_list in enumerate(prediction):
            for pw in pre_list:
                if label_data[idx][pw] > 0:
                    correct_count = correct_count + 1
                    label_data[idx][pw] -= 1

            pre_total += len(pre_list)

        if not self.training and random.random() < 0.05:
            self.vis(iteration)

        return correct_count, len_total, pre_total
