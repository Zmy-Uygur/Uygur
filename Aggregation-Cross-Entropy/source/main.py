# -*- coding: utf-8 -*-
from __future__ import print_function, division
import torch
import argparse
import numpy as np
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from models.seq_module import ACE
from torch.autograd import Variable
from models.solver import seq_solver
from utils.basic import timeSince
from torch.utils.data import DataLoader
from utils.data_loader import ImageDataset

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, default='../log/snapshot/model-{:0>2d}.pkl')
parser.add_argument('--total_epoch', type=int, default=50, help='total epoch number')
parser.add_argument('--train_path', type=str, default='../data/train.txt')
parser.add_argument('--test_path', type=str, default='../data/test.txt')
parser.add_argument('--train_batch_size', type=int, default=50, help='training batch size')
parser.add_argument('--test_batch_size', type=int, default=50, help='testing batch size')
parser.add_argument('--last_epoch', type=int, default=0, help='last epoch')
parser.add_argument('--class_num', type=int, default=26, help='class number')
parser.add_argument('--dict', type=str, default='_abcdefghijklmnopqrstuvwxyz')
opt = parser.parse_args()
print(opt)

# PyTorch定义了几个常用模型（包含预训练版本）
import torchvision.models as models


class ResnetEncoderDecoder(nn.Module):
    def __init__(self, loss_layer):
        super(ResnetEncoderDecoder, self).__init__()
        self.bn = nn.BatchNorm2d(64)  # 数据归一化
        resnet = models.resnet18(pretrained=True)
        self.conv = nn.Conv2d(1, 64, kernel_size=(3, 3), padding=(1, 1), stride=(1, 1))  # 卷积
        # 取掉model的前四层后两层
        self.cnn = nn.Sequential(*list(resnet.children())[4:-2])
        self.out = nn.Linear(512, opt.class_num + 1)
        self.loss_layer = loss_layer(opt.dict)

    def forward(self, input, labels):
        input = F.relu(self.bn(self.conv(input)), True)  # 激活
        input = F.max_pool2d(input, kernel_size=(2, 2), stride=(2, 2))  # 池化
        input = self.cnn(input)

        # 维度换位
        input = input.permute(0, 2, 3, 1)
        input = F.softmax(self.out(input), dim=-1)

        labels = labels.cuda()

        return self.loss_layer(input, labels)


if __name__ == "__main__":
    # 构建网络, resnet18残差模块
    model = ResnetEncoderDecoder(ACE).cuda()
    print(model)

    # 优化器
    optimizer = optim.Adadelta(model.parameters())

    if opt.last_epoch != 0:
        check_point = torch.load(opt.model_path.format(opt.last_epoch))
        model.load_state_dict(check_point['state_dict'])
        optimizer.load_state_dict(check_point['optimizer'])
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[opt.total_epoch], gamma=0.1,
                                                   last_epoch=opt.last_epoch)
    else:
        # 学习率更新
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[opt.total_epoch], gamma=0.1)

    # 加载训练样本
    train_set = ImageDataset(file_name=opt.train_path, length=5000, class_num=opt.class_num)
    # DataLoader将数据根据batch大小、是否shuffle等封装成一个Batch大小的Tensor，用于后面的训练
    lmdb_train = DataLoader(train_set,  # 数据加载
                            batch_size=opt.train_batch_size,  # 批处理大小
                            shuffle=True,  # 是否进行洗牌操作
                            num_workers=0)  # 是否多进程加载数据设置

    # 测试样本
    test_set = ImageDataset(file_name=opt.test_path, length=1000, class_num=opt.class_num)
    lmdb_test = DataLoader(test_set, batch_size=opt.test_batch_size, shuffle=False, num_workers=0)

    # 训练
    the_solver = seq_solver(model=model,
                            lmdb=[lmdb_train, lmdb_test],
                            optimizer=optimizer,
                            scheduler=scheduler,
                            total_epoch=opt.total_epoch,
                            model_path=opt.model_path,
                            last_epoch=opt.last_epoch)

    the_solver.forward()
