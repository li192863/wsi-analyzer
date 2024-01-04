import math
import os

import matplotlib.pyplot as plt

# 配置环境变量
from PIL import Image

vipshome = os.path.join(os.getcwd(), './vips-dev-8.14', 'bin')
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  # 导入pyvips包

plt.style.use('_mpl-gallery-nogrid')


def get_image_size(source, type='file'):
    """
    获取图片真实大小
    :param source: 图片文件，图片对象，图片尺寸
    :param type: source的类型，可以为 'file', 'image', 'size'
    :return: [origin_width, origin_height]
    """
    if type == 'file':
        # try with vips
        try:
            image = pyvips.Image.new_from_file(source)
            return image.width, image.height
        except:
            pass
        # try with pillow
        try:
            image = Image.open(source)
            return image.width, image.height
        except:
            pass
        raise ValueError(f'文件尺寸获取失败！')
    elif type == 'image':
        assert hasattr(source, 'width') and hasattr(source, 'height')
        return source.width, source.height
    elif type == 'size':
        return source[0], source[1]
    else:
        raise ValueError(f'{repr(type)}类型暂不支持！')


def get_scaled_size(source, down_sample, type='file'):
    """
    获取降采样后图片大小
    :param source: 图片文件，图片对象，图片尺寸
    :param down_sample: 降采样倍数
    :param type: source的类型，可以为 'file', 'image', 'size'
    :return: [scaled_width, scaled_height]
    """
    origin_width, origin_height = get_image_size(source, type)
    scaled_width, scaled_height = round(origin_width / down_sample), round(origin_height / down_sample)
    return scaled_width, scaled_height


def get_boxed_size(source, slice_size, drop_last=False, type='file'):
    """
    获取图片切片后的行数和列数
    :param source: 图片文件，图片对象，图片尺寸
    :param slice_size: [slice_width, slice_height]
    :param drop_last: 是否舍弃边缘
    :param type: source的类型，可以为 'file', 'image', 'size'
    :return: [cols, rows]
    """
    # 获取切片前宽高
    width, height = get_image_size(
        source,
        type
    )
    # 获取单个切片宽高
    slice_width, slice_height = slice_size
    # 获取切片后行列
    cols = width // slice_width if drop_last else math.ceil(width / slice_width)
    rows = height // slice_height if drop_last else math.ceil(height / slice_height)
    return cols, rows


def get_slicer_size(source, down_sample, slice_size, drop_last, type='file'):
    """
    获取经过slicer模块后的尺寸信息（降采样 -> 裁切）
    :param source: 图片文件，图片对象，图片尺寸
    :param down_sample: 降采样倍数
    :param slice_size: 是否舍弃边缘
    :param drop_last: 是否舍弃边缘
    :param type: source的类型，可以为 'file', 'image', 'size'
    :return: [scaled_width, scaled_height, cols, rows]
    """
    # 获取原始图片宽高
    origin_width, origin_height = get_image_size(
        source,
        type
    )
    # 获取降采样后宽高
    scaled_width, scaled_height = get_scaled_size(
        (origin_width, origin_height),
        down_sample,
        type='size'
    )
    # 获取经切片后宽高
    cols, rows = get_boxed_size(
        (scaled_width, scaled_height),
        slice_size,
        drop_last,
        type='size'
    )
    return scaled_width, scaled_height, cols, rows


def get_inferencer_size(source, down_sample, slice_size, drop_last, type='file'):
    """
    获取经过inferencer模块后的尺寸信息（降采样 -> 裁切 -> 填充）
    :param source: 图片文件，图片对象，图片尺寸
    :param down_sample: 降采样倍数
    :param slice_size: 是否舍弃边缘
    :param drop_last: 是否舍弃边缘
    :param type: source的类型，可以为 'file', 'image', 'size'
    :return: [scaled_width, scaled_height, cols, rows]
    """
    # 获取经切片后宽高
    scaled_width, scaled_height, cols, rows = get_slicer_size(
        source,
        down_sample,
        slice_size,
        drop_last,
        type
    )
    # 获取单个切片宽高
    slice_width, slice_height = slice_size
    # 获取经填充后宽高
    scaled_width, scaled_height = cols * slice_width, rows * slice_height
    return scaled_width, scaled_height, cols, rows
