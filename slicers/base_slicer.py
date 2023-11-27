import numpy as np
from PIL import Image

from slicers.slicer import Slicer


class BaseSlicer(Slicer):
    """ 基于Pillow实现的切片器 """
    def __init__(self, slice_size, down_sample=1, drop_last=True, prefix='', suffix='.jpg'):
        """
        初始化图片切割器
        :param slice_size: 切片大小 [width, height]
        :param drop_last: 舍弃图片边缘
        :param down_sample: 降采样倍数
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        """
        super(BaseSlicer, self).__init__(slice_size, down_sample, drop_last, prefix, suffix)

    def read_file(self, file) -> Image:
        """
        读取图片
        :param file: 图片文件
        :return: 图片对象
        """
        return Image.open(file)

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
        width, height = image.size
        down_sample_size = (width // down_sample_factor, height // down_sample_factor)
        return image.resize(down_sample_size)

    def get_image_array(self, image) -> np.ndarray:
        """
        获取图片数组
        :param image:
        :return:
        """
        return np.array(image)

    def filter_image(self, image) -> bool:
        """
        判断指定切片是否需要保留
        :param image: 图片
        :return: 是否需要保留
        """
        return True


if __name__ == '__main__':
    file = r"E:\test_folder\iphone14.png"
    # slicer = BaseSlicer([10, 20], down_sample=1, drop_last=False, prefix='test_prefix', suffix='.png')
    # slicer.file_to_slices(file)
    # slicer = BaseSlicer([10, 20], down_sample=2, drop_last=False, prefix='test_prefix_', suffix='.jpg')
    # slicer.file_to_slices(file, image_dir=r"E:\test_folder\iphone14\test_slices_d2")
    # slicer = BaseSlicer([24, 24], down_sample=3, drop_last=False, prefix='', suffix='.jpg')
    # slicer.file_to_slices(file, image_dir=r"E:\test_folder\iphone14\test_slices_d3")
    # slicer = BaseSlicer([24, 24], down_sample=16, drop_last=False, prefix='', suffix='.jpg')
    # slicer.file_to_slices(file, result_folder=r"E:\test_folder\iphone14\test_slices_d3_target")
    # slicer = BaseSlicer([24, 24], down_sample=16, drop_last=True, prefix='', suffix='.jpg')
    # slicer.file_to_slices(file, result_folder=r"E:\test_folder\iphone14\test_slices_d16_target_drop_last")
    print('unit test is done!')
