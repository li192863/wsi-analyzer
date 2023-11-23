from torch import nn

from model.classification import *
from model.segmentation import *


def get_seg_model(classes):
    """
    获取分类模型
    :param classes: 种类列表
    :return:
    """
    model = DeepLabV3Plus(len(classes), pretrained=False)
    return model


def get_cla_model(classes):
    """
    获取分类模型
    :param classes: 种类列表
    :return:
    """
    model = MobileNetV3_Large()
    in_channels = model.linear4.in_features  # 获得最后fc层的in_features参数
    model.linear4 = nn.Linear(in_channels, len(classes))  # 改变原网络最后一层参数
    return model
