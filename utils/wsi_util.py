from classification.model import get_model_finetuning_the_convnet
from inferencers import ClassificationInferencer, SegmentationInferencer
from inferencers.ClassificationInferencer import ClassificationPresetEval
from inferencers.SegmentationInferencer import SegmentationPresetEval
from segmentation.model import DeepLabV3Plus
from slicers import VipsSlicer


def get_seg_slicer(slice_size=(2048, 2048), drop_last=True, down_sample=16, prefix='', suffix='.jpg'):
    """
    获取分割所用的切片器
    :param slice_size: 切片大小 [width, height]
    :param drop_last: 舍弃图片边缘
    :param down_sample: 降采样倍数
    :param prefix: 文件前缀
    :param suffix: 文件后缀
    :return:
    """
    return VipsSlicer(slice_size, down_sample=down_sample, drop_last=drop_last, prefix=prefix, suffix=suffix)


def get_cla_slicer(slice_size=(1024, 1024), drop_last=True, down_sample=1, prefix='', suffix='.jpg'):
    """
    获取分类所用的切片器
    :param slice_size: 切片大小 [width, height]
    :param drop_last: 舍弃图片边缘
    :param down_sample: 降采样倍数
    :param prefix: 文件前缀
    :param suffix: 文件后缀
    :return:
    """
    return VipsSlicer(slice_size, down_sample=down_sample, drop_last=drop_last, prefix=prefix, suffix=suffix)


def get_seg_inferencer(
        weights=None,
        transform_size=(1024, 1024),
        required_size=(2048, 2048),
        batch_size=2,
        device=None
):
    """
    获取分割的分类器，提供model、class、transform_cls等信息
    :return:
    """
    classes = ['_background_', 'Normal', 'Tumor']
    model = DeepLabV3Plus(len(classes), pretrained=False)
    weights = weights or '../segmentation/data/model.pth'
    return SegmentationInferencer(model, weights, classes, transform_cls=SegmentationPresetEval, inference_size=transform_size,
                                  required_size=required_size, batch_size=batch_size, device=device)


def get_cla_inferencer(
        weights=None,
        transform_cls=ClassificationPresetEval,
        transform_size=(256, 256),
        required_size=(1024, 1024),
        batch_size=16,
        device=None
):
    """
    获取分类的分类器，提供model、class、transform_cls信息
    :return:
    """
    classes = ['出血', '坏死', '实质', '淋巴', '空泡', '空白', '间质']
    model = get_model_finetuning_the_convnet(len(classes), pretrained=False)
    weights = weights or '../classification/data/model.pth'
    return ClassificationInferencer(model, weights, classes, transform_cls=transform_cls, inference_size=transform_size,
                                    required_size=required_size, batch_size=batch_size, device=device)
