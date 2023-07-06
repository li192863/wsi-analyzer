import math
import os
import os.path as osp

import PIL.Image
from PIL import Image
import numpy as np

# 配置环境变量
vipshome = os.path.join(os.getcwd(), 'vips-dev-8.14', 'bin')
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  # 导入pyvips包


class ImageSlicer(object):
    def __init__(self, slice_size, drop_last=True, enable_filter=True, threshold=230,  down_sample=2, target_dir='', prefix='', suffix='.jpg'):
        """
        初始化图片切割器
        :param slice_size: 切片大小 [height, width]
        :param drop_last: 舍弃图片边缘
        :param threshold: 方差阈值
        :param target_dir: 目标文件夹 ''代表默认指定切片当前文件夹
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        """
        self.slice_size = slice_size
        self.drop_last = drop_last
        self.enable_filter = enable_filter
        self.threshold = threshold
        self.down_sample = down_sample
        self.target_dir = target_dir
        self.prefix = prefix
        self.suffix = suffix

        self.file_name = ''
        self.image = None
        self.white_ratio = 1
        self._thumbnail_width = 100

    def set_file(self, file_name):
        """
        设置文件
        :param file_name:
        :return:
        """
        if file_name == None or not osp.isfile(file_name):
            self.file_name = ''
            self.image = None
            self.white_ratio = 1
            return
        self.file_name = file_name
        self.white_ratio = self.compute_while_ratio(pyvips.Image.thumbnail(self.file_name, self._thumbnail_width))
        self.image = pyvips.Image.new_from_file(self.file_name, access='sequential').resize(1 / self.down_sample)
        self.width, self.height, self.depth = self.image.width, self.image.height, self.image.bands

    def get_info(self, down_sample: float = 2):
        """
        由当前降采样值得到降采样后图片尺寸
        :param down_sample:
        :return:
        """
        img = pyvips.Image.thumbnail(self.file_name, int(self.image.width / down_sample))
        stride_h, stride_w = self.slice_size
        h, w = img.height, img.width
        num_h, num_w = h // stride_h, w // stride_w
        count = int(num_h * num_w * (1.0 - self.white_ratio))
        info = f'空白占比={self.white_ratio * 100:.1f}%，分片数量≈{num_h}x{num_w}x{(1 - self.white_ratio) * 100:.1f}%={count}'
        return info

    def compute_while_ratio(self, image, num_points=1000):
        """
        计算白色占比
        :param picture:
        :return:
        """
        if type(image) == pyvips.Image:
            img = image.numpy()
        elif type(image) == PIL.Image.Image:
            img = np.array(image)
        else:
            img = image
        height, width, depth = img.shape
        # 读取图片
        num_points = min(width * height, num_points)
        indices0 = np.random.randint(0, height, (num_points,))
        indices1 = np.random.randint(0, width, (num_points,))

        white_ratio = np.count_nonzero(np.mean(img[indices0, indices1], axis=1) > self.threshold) / num_points
        return white_ratio

    def generate_slices(self):
        """
        分割图片为列表
        :param file:
        :return:
        """
        # 保存路径
        filepath, filename = os.path.split(self.file_name)
        image_folder_name = ''.join(filename.split('.')[:-1])
        if self.target_dir == '':
            image_dir = os.path.join(filepath, image_folder_name)
        else:
            image_dir = os.path.join(self.target_dir, image_folder_name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        # 缩小图片
        img = pyvips.Image.thumbnail(self.file_name, int(self.image.width / self.down_sample))
        # 计算尺寸
        stride_h, stride_w = self.slice_size
        # 抛弃边缘
        if self.drop_last:
            num_h, num_w = img.height // stride_h, img.width // stride_w
            img = img.crop(0, 0, num_w * stride_w, num_h * stride_h)
        else:
            num_h, num_w = math.ceil(img.height / stride_h), math.ceil(img.width // stride_w)
        width = len(str(max(num_h, num_w)))
        # 裁切图片
        img = img.numpy()
        for i in range(0, num_h):
            top = i * stride_h
            for j in range(0, num_w):
                left = j * stride_w
                img_slice = img[top: top + stride_h, left: left + stride_w]
                if self.enable_filter and self.compute_while_ratio(img_slice) > 0.5:
                    continue
                slice_name = f'{self.prefix}_{filename}_{str(i).zfill(width)}_{str(j).zfill(width)}{self.suffix}'
                image = Image.fromarray(img_slice).convert('RGB')
                image.save(osp.join(image_dir, slice_name))

if __name__ == '__main__':
    # options = {
    #     'slice_size': [512, 512],
    #     'filter_image': True,
    #     'threshold': 50,
    #     'prefix': '',
    #     'suffix': '.jpg'
    # }
    # files = ['../test.svs', '../test2.svs']
    file = r"E:\Projects\Carcinoma\素材\TCGA-2Y-A9GW-01Z-00-DX1.71805205-933D-4D72-A4A2-586DC5490D78.svs"
    slicer = ImageSlicer(slice_size=[892, 892], drop_last=False, enable_filter=False, threshold=235, down_sample=1, suffix='.jpg', prefix='xxx')
    slicer.set_file(file)
    slicer.generate_slices()
