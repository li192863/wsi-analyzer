import math
import os
import os.path as osp
from threading import Thread

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
        self._white_threshold = 77

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
        self.image = pyvips.Image.new_from_file(self.file_name, access='sequential', memory=True)

    def analyze_slices(self):
        """
        由当前降采样值得到降采样后图片尺寸
        :param down_sample:
        :return:
        """
        # 空白占比
        white_ratio1 = self.compute_while_ratio(pyvips.Image.thumbnail(self.file_name, self._thumbnail_width), smooth_value=3, threshold=self.threshold)
        white_ratio2 = self.compute_while_ratio(pyvips.Image.thumbnail(self.file_name, self._thumbnail_width), smooth_value=3, threshold=255 - self.threshold)
        white_ratio, diff = (white_ratio1 + white_ratio2) / 2, abs(white_ratio2 - white_ratio1)
        # 分片数量
        image = self.image.resize(1 / self.down_sample)
        stride_h, stride_w = self.slice_size
        h, w = image.height, image.width
        if self.drop_last:
            num_h, num_w = h // stride_h, w // stride_w
        else:
            num_h, num_w = math.ceil(h / stride_h), math.ceil(w / stride_w)
        count = int(num_h * num_w)
        info = f'空白占比={white_ratio * 100:.1f}%(误差：{diff * 100:.0f}%)，分片数量={num_h}x{num_w}={count}'
        return info

    def compute_while_ratio(self, image, num_points=500, smooth_value=1, threshold=235, random_access=True):
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
        if random_access:
            num_points = num_points * smooth_value
            indices0 = np.random.randint(0, height, (num_points,))
            indices1 = np.random.randint(0, width, (num_points,))
            # 计算占比
            white_ratio = np.count_nonzero(np.mean(img[indices0, indices1], axis=1) > threshold) / num_points / smooth_value
        else:
            white_ratio = np.count_nonzero(np.mean(img, axis=-1) > threshold) / height / width
        return white_ratio

    def generate_slices(self):
        """
        分割图片为列表
        :param file:
        :return:
        """
        # 裁切图片
        self.image = self.image.resize(1 / self.down_sample)
        # 保存路径
        filepath, filename = os.path.split(self.file_name)
        image_folder_name = ''.join(filename.split('.')[:-1])
        if self.target_dir == '':
            image_dir = os.path.join(filepath, image_folder_name)
        else:
            image_dir = os.path.join(self.target_dir, image_folder_name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        # 计算尺寸
        stride_h, stride_w = self.slice_size
        # 抛弃边缘
        if self.drop_last:
            num_h, num_w = self.image.height // stride_h, self.image.width // stride_w
            self.image = self.image.crop(0, 0, num_w * stride_w, num_h * stride_h)
        else:
            num_h, num_w = math.ceil(self.image.height / stride_h), math.ceil(self.image.width / stride_w)
        width = len(str(max(num_h, num_w)))
        # 裁切图片
        img = self.image.numpy()
        for i in range(0, num_h):
            top = i * stride_h
            for j in range(0, num_w):
                left = j * stride_w
                img_slice = img[top: top + stride_h, left: left + stride_w]
                if self.enable_filter and self.compute_while_ratio(img_slice) > 0.5:
                    continue
                slice_name = f'{self.prefix}' \
                             f'i{str(i).zfill(width)}_' \
                             f'j{str(j).zfill(width)}_' \
                             f'd{str(self.down_sample).zfill(2)}_' \
                             f'{filename}' \
                             f'{self.suffix}'
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
    slicer = ImageSlicer(slice_size=[892, 1000], drop_last=False, enable_filter=False, threshold=235, down_sample=1, suffix='.jpg', prefix='xxx')
    slicer.set_file(file)
    slicer.analyze_slices()
    slicer.generate_slices()
