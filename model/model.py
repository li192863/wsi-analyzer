from model.classification import *
from model.segmentation import *


def get_seg_model(classes):
    """
    获取分类模型
    :param classes: 种类列表
    :return:
    """
    model = DeepLabV3Plus(len(classes), pretrained=False)
    model.eval()
    return model


def get_cla_model(classes):
    """
    获取分类模型
    :param classes: 种类列表
    :return:
    """
    model = get_model_finetuning_the_convnet(len(classes))
    model.eval()
    return model
