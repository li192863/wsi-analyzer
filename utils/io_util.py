import os
import pickle
import shutil

import matplotlib.pyplot as plt
import yaml
from addict import Dict


plt.style.use('_mpl-gallery-nogrid')

def make_directory(directory, delete_old=False):
    """
    创建文件夹，若文件夹不存在则创建
    :param directory: 文件夹
    :return: 文件夹名称
    """
    # 若文件夹已存在、且要求删除时则删除
    if delete_old and os.path.exists(directory):
        shutil.rmtree(directory)
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


def read_text(file, encoding='utf-8'):
    """
    读取文件
    :param file: 要读取的文件
    :param encoding: 文件编码方式
    :return:
    """
    with open(file, 'r', encoding=encoding) as f:
        text = f.read()
    return text


def write_text(text, file, encoding='utf-8'):
    """
    读取文件
    :param text: 要读取的文件
    :param file: 要读取的文件
    :param encoding: 文件编码方式
    :return:
    """
    with open(file, 'w', encoding=encoding) as f:
        f.write(text)
    return text


def read_config(config_file, encoding='utf-8'):
    """
    读取配置
    :param config_file: 配置文件
    :param encoding: 配置文件编码方式
    :return: 配置字典
    """
    with open(config_file, 'r', encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)  # Loader为了更加安全
    return Dict(config)
