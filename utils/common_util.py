import os
import pickle
import shutil

import matplotlib.pyplot as plt
import torch

from matplotlib import cm

plt.style.use('_mpl-gallery-nogrid')

def make_directory(directory):
    """
    创建文件夹，若文件夹不存在则创建
    :param directory: 文件夹
    :return: 文件夹名称
    """
    # # 若文件夹已存在则删除
    # if os.path.exists(directory):
    #     shutil.rmtree(directory)
    # os.makedirs(directory)
    # 若文件夹不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def read_object(file):
    """
    读取对象
    :param file: 存储对象的文件
    :return: 对象
    """
    with open(file, 'rb') as f:
        return pickle.load(f)


def write_object(obj, file):
    """
    写入对象
    :param obj: 要写入的对象
    :param file: 文件路径
    :return: 无
    """
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


def show_image(tensor, *, cmap=cm.coolwarm, save_path=None, show_image=True):
    """
    可视化一个二维矩阵
    :param tensor: 输入的二维矩阵
    :param cmap: 颜色映射
    :return: 图片
    """
    fig, ax = plt.subplots()
    ax.imshow(tensor, cmap=cmap)
    ax.axis('off')  # 关闭坐标轴
    # fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    if save_path is not None:
        plt.savefig(save_path)
    if show_image:
        plt.show()

def show_contour(tensor, *, cmap=cm.coolwarm, save_path=None, show_image=True):
    """
    可视化一个二维矩阵
    :param tensor: 输入的二维矩阵
    :param cmap: 颜色映射
    :return: 图片
    """
    fig, ax = plt.subplots()
    ax.contour(tensor, cmap=cmap)
    ax.axis('off')  # 关闭坐标轴
    if save_path is not None:
        plt.savefig(save_path)
    if show_image:
        plt.show()

if __name__ == '__main__':
    random_tensor = torch.rand(5, 5)
    # show_image(random_tensor, save_path='./test.png')
    show_contour(random_tensor, save_path='./test.png')

