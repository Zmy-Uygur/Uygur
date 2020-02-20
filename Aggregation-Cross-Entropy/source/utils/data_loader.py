import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader


class ImageDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, file_name, length, class_num, transform=None):
        """
        Args:
            file_name (string): Path to the files with images and their annotations.
            length (string): image number.
            class_num (int): class number.
        """
        with open(file_name) as fh:
            self.img_and_label = fh.readlines()
        self.length = length
        self.transform = transform
        self.class_num = class_num

    def __len__(self):
        return self.length

    def __getitem__(self, idx):

        img_and_label = self.img_and_label[idx].strip() # 去除首尾空格
        pth, word = img_and_label.split(' ') # 分离图片路径与标签


        image = cv2.imread(pth,0)
        # 从一个高分辨率大尺寸的图像向上构建一个金字塔（滤波下采样）
        image = cv2.pyrDown(image).astype('float32') # 100*100

        # 从0开始返回ASCII码
        word = [ord(var)-97 for var in word] # a->0

        label = np.zeros((self.class_num+1)).astype('float32')

        for ln in word:
            label[int(ln+1)] += 1 # 构造ACE的标签

        label[0] = len(word)

        # sample = {'image': image, 'label': label}

        # numpy中的数组转化成pytorch中的tensor
        # unsqueeze(0)第一维度处增加一维
        sample = {'image': torch.from_numpy(image).unsqueeze(0), 'label': torch.from_numpy(label)}

        if self.transform:
            sample = self.transform(sample)

        return sample    


