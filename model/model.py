from torch import nn

from model.classification import *
from model.segmentation import *


def get_seg_model(classes) -> nn.Module:
    """
    获取分类模型，请手动修改该函数以适配自己的模型
    :param classes: 种类列表
    :return:
    """
    model = MyNet(bilinear=False, num_classes=len(classes))
    model.eval()
    return model


def get_cla_model(classes) -> nn.Module:
    """
    获取分类模型，请手动修改该函数以适配自己的模型
    :param classes: 种类列表
    :return:
    """
    model = get_model_finetuning_the_convnet(len(classes))
    model.eval()
    return model
