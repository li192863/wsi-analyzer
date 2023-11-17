import os

# 配置环境变量
import numpy as np

vipshome = os.path.join(os.getcwd(), '../vips-dev-8.14', 'bin')
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  # 导入pyvips包

from pyvips import Image

from slicers.Slicer import Slicer

class VipsSlicer(Slicer):
    """ 基于pyvips实现的切片器 """
    def __init__(self, slice_size, down_sample=1, drop_last=True, prefix='', suffix='.jpg', memory=True):
        """
        初始化图片切割器
        :param slice_size: 切片大小 [width, height]
        :param drop_last: 舍弃图片边缘
        :param down_sample: 降采样倍数
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        :param memory: 是否采用内存加载
        """
        super(VipsSlicer, self).__init__(slice_size, down_sample, drop_last, prefix, suffix)
        self.memory = memory

    def read_file(self, file) -> Image:
        """
        读取图片
        :param file: 图片文件
        :return: 图片对象
        """
        self.image_arr = None
        return pyvips.Image.new_from_file(file, access='sequential', memory=self.memory)

    def write_image(self, image, image_path):
        """
        写入图片
        :param image: 图片
        :param image_path: 图片存放路径
        """
        image.save(image_path)

    def down_sample_image(self, image, down_sample_factor) -> Image:
        """
        将指定图片进行降采样
        :param image: 图片
        :param down_sample_factor: 降采样倍数
        :return: 降采样后的图片
        """
        return image.resize(1 / down_sample_factor)

    def filter_image(self, image) -> bool:
        """
        判断指定切片是否需要保留
        :param image: 图片
        :return: 是否需要保留
        """
        return True

    def get_image_array(self, image) -> np.ndarray:
        """
        获取图片数组
        :param image:
        :return:
        """
        return image.numpy()


if __name__ == '__main__':
    file = r"E:\Projects\Carcinoma\#Temp\test\TCGA-2Y-A9GW-01Z-00-DX1.71805205-933D-4D72-A4A2-586DC5490D78.svs"
    slicer = VipsSlicer([892, 892], down_sample=1, drop_last=True)
    slicer.file_to_slices(file)
