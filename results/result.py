import logging
import os
import re
from abc import ABC, abstractmethod

from PIL import Image

from binders import get_progress_binder


class Result(ABC):
    """ 分割结果 """
    default_value = -1
    def __init__(self, dict_results, slice_size, down_sample, naming_regex=r'd(\d+)_r(\d+)_c(\d+)\..*'):
        """
        初始化结果对象
        :param dict_results: 结果字典
        :param slice_size: 切片大小 [width, height]
        :param down_sample: 降采样倍数
        :param naming_regex: 文件命名的正则表达式
        """
        self.dict_results = dict_results
        self.slice_size = slice_size
        self.naming_regex = naming_regex
        self.logger = logging.getLogger('file-logger')
        self.progress_binder = get_progress_binder()
        # 获取信息
        self.down_sample = down_sample
        self.slice_width, self.slice_height = self.slice_size
        # 构建结果集
        self.results, self.slice_paths = None, None
        self.scan_dict_results()

    def __getitem__(self, item):
        try:
            return self.results[item]
        except:
            return self.default_value

    @abstractmethod
    def scan_dict_results(self):
        """
        扫描dict_results
        :return: 无
        """
        pass

    def parse_path(self, path: str):
        """
        获取当前切片对应的方格信息
        :param path: 路径字符串
        :return: d降采样倍数，r行数，c列数
        """
        filepath, filename =  os.path.split(path)
        pattern = re.compile(self.naming_regex)
        match = pattern.match(filename)
        if match:
            d, r, c = int(match.group(1)), int(match.group(2)), int(match.group(3))
        else:
            self.logger.error('解析结果文件字符串出错，请检查文件字符串是否正确或重新生成切片!')
            raise ValueError('解析结果文件字符串出错，请检查文件字符串是否正确或重新生成切片!')
        return d, r, c

    def get_slice_image(self, r, c):
        """
        获取图片
        :param r: 横坐标
        :param c: 纵坐标
        :return:
        """
        return Image.open(self.slice_paths[r, c])

    def scaled_to_box(self, x1, y1):
        """
        返回指定缩放后点的box坐标
        :param x1: 经过缩放后横坐标
        :param y1: 经过缩放后纵坐标
        :return: (r, c)
        """
        return y1 // self.slice_height, x1 // self.slice_width

    def box_to_scaled(self, r, c):
        """
        返回指定box的缩放后左上点坐标
        :param r: box横坐标
        :param c: box纵坐标
        :return: (x1, y1)
        """
        return c * self.slice_width, r * self.slice_height

    def origin_to_box(self, x1, y1):
        """
        返回指定原始点的box坐标
        :param x1: 原始横坐标
        :param y1: 原始纵坐标
        :return: (r, c)
        """
        return y1 // self.down_sample // self.slice_height, x1 // self.down_sample // self.slice_width

    def box_to_origin(self, r, c):
        """
        返回指定box的原始左上点坐标
        :param r: box横坐标
        :param c: box纵坐标
        :return: (x1, y1)
        """
        return c * self.down_sample * self.slice_width, r * self.down_sample * self.slice_height
