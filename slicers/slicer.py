import logging
import os
from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np
from PIL import Image

from binders import get_progress_binder
from utils import make_directory, get_boxed_size


class Slicer(ABC):
    def __init__(self, slice_size, down_sample=1, drop_last=True, prefix='', suffix='.jpg'):
        """
        初始化图片切割器
        :param slice_size: 切片大小 [width, height]
        :param drop_last: 舍弃图片边缘
        :param down_sample: 降采样倍数
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        """
        self.slice_size = slice_size
        self.drop_last = drop_last
        self.down_sample = down_sample
        self.prefix = prefix
        self.suffix = suffix
        self.logger = logging.getLogger('file-logger')
        self.progress_binder = get_progress_binder()

        self.slice_width, self.slice_height = self.slice_size

    def file_to_slices(self, file, image_dir=None, result_folder=None):
        """
        将给定文件生成切片
        方式1，指定image_dir，图片将存放至image_dir下
        方式2，未指定image_dir、指定result_folder，图片将存放至{result_folder}/{filename}下
        方式3，未指定image_dir、未指定result_folder，图片将存放至{filepath}/{filename}下，即result_folder为file所在的file_path
        :param file: 图片文件
        :param image_dir: 图片文件夹
        :param result_folder: 目标文件夹，默认为当前图片文件夹
        """
        # 读取图片
        image = self.read_file(file)
        # 降采样
        down_sampled_image = self.down_sample_image(image, self.down_sample)
        # 裁切
        cols, rows = get_boxed_size(down_sampled_image, self.slice_size, self.drop_last, type='image')
        idx_len = max(len(str(rows)), len(str(cols)))
        # 创建文件夹，若未指定image_dir则存放至{result_folder}/{filename}下
        image_dir = self._prepare_image_dir(file, image_dir, result_folder)
        # 转换图片为数组
        self.logger.info('开始读取图片...')
        stage, _ = self.progress_binder.get_stage()
        self.progress_binder.set_stage(0, stage)
        image_arr = self.get_image_array(down_sampled_image)
        self.progress_binder.set_stage(100, stage)
        # 遍历图片
        self.logger.info('开始写入...')
        stage, _ = self.progress_binder.get_stage()
        self.progress_binder.set_stage(0, stage)
        for r in reversed(range(rows)):
            for c in reversed(range(cols)):
                # 获取图片边界
                left = c * self.slice_width
                top = r * self.slice_height
                right = left + self.slice_width
                bottom = top + self.slice_height
                # 裁切图片
                cropped_image = image_arr[top: bottom, left: right, ...]
                # 保留符合预期图片
                if self.filter_image(cropped_image):
                    image = Image.fromarray(cropped_image).convert('RGB')
                    image_name = self.get_slice_name(
                        prefix=self.prefix,
                        suffix=self.suffix,
                        d=self.down_sample,
                        r=str(r).zfill(idx_len),
                        c=str(c).zfill(idx_len)
                    )
                    image_path = os.path.join(image_dir, image_name)
                    self.write_image(image, image_path)
            if r % 4 == 0:
                self.logger.info(f'写入完成度{(1 - r / rows) * 100:.2f}%')
                self.progress_binder.set_stage((1 - r / rows) * 100, stage)
        self.progress_binder.set_stage(100, stage)
        self.logger.info(f'写入完成！')

    def _prepare_image_dir(self, file, image_dir=None, result_folder=None):
        """
        准备图片文件夹
        方式1，指定image_dir，图片将存放至image_dir下
        方式2，未指定image_dir、指定result_folder，图片将存放至{result_folder}/{filename}下
        方式3，未指定image_dir、未指定result_folder，图片将存放至{filepath}/{filename}下
        :param file: 图片文件
        :param image_dir: 图片文件夹
        :param result_folder: 目标文件夹，默认为当前图片文件夹
        :return: 切片文件存放文件夹
        """
        # 尝试方式2/3
        if image_dir is None:
            # 获取文件存放路径以及文件名
            filepath, filename = os.path.split(file)
            # 获取存放图片输出目录目录名
            image_folder_name = '.'.join(filename.split('.')[:-1])
            # 获取输出切片的切片文件夹
            if result_folder is None:
                image_dir = os.path.join(filepath, image_folder_name)
            else:
                image_dir = os.path.join(result_folder, image_folder_name)
        image_dir = make_directory(image_dir)
        return image_dir

    @abstractmethod
    def get_image_array(self, image) -> np.ndarray:
        """
        获取图片数组
        :param image:
        :return:
        """
        pass

    def get_slice_name(self, *, delimiter='_', prefix='', suffix='', **kwargs):
        """
        获取文件名
        :param delimiter: 分割符
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        :param kwargs: 参数列表
        :return: 图片切片名称
        """
        args = [f'{str(k)}{str(v)}' for k, v in kwargs.items()]
        image_name = f'{prefix}{delimiter.join(args)}{suffix}'
        return image_name

    def files_to_slices(self, files: Iterable, target_dir=''):
        """
        将给定文件列表内生成切片
        :param files: 可迭代图片文件列表
        :param target_dir: 目标文件夹，默认为当前图片文件夹
        """
        for file in files:
            self.file_to_slices(file, result_folder=target_dir)

    def before_generate(self):
        """
        生成图片前钩子函数
        :return:
        """
        pass

    @abstractmethod
    def read_file(self, file) -> object:
        """
        读取图片
        :param file: 图片文件
        :return: 图片对象
        """
        pass

    @abstractmethod
    def write_image(self, image, image_path):
        """
        写入图片
        :param image: 图片
        :param image_path: 图片存放路径
        """
        pass

    @abstractmethod
    def down_sample_image(self, image, down_sample_factor) -> object:
        """
        将指定图片进行降采样
        :param image: 图片
        :param down_sample_factor: 降采样倍数
        :return: 降采样后的图片
        """
        pass

    @abstractmethod
    def filter_image(self, image) -> bool:
        """
        判断指定切片是否需要保留
        :param image: 图片
        :return: 是否需要保留
        """
        pass
