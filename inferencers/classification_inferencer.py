import torch
from torch import Tensor
from torchvision.transforms import InterpolationMode, transforms

from inferencers.inferencer import Inferencer


class ClassificationPresetEval:
    """ 分类预处理器 """

    def __init__(
            self,
            *,
            resize_size,
            crop_size=None,
            mean=None,  # (0.723, 0.485, 0.608)
            std=None,  # (0.293, 0.377, 0.333)
            interpolation=InterpolationMode.BILINEAR,
    ):
        # 缩放
        trans = [transforms.Resize(resize_size, interpolation=interpolation)]
        # 剪裁 可选
        if crop_size is not None:
            trans.append(transforms.CenterCrop(crop_size))
        # 转图
        trans.append(transforms.PILToTensor())
        trans.append(transforms.ConvertImageDtype(torch.float))
        # 归一 可选
        if mean is not None and std is not None:
            trans.append(transforms.Normalize(mean=mean, std=std))

        self.transforms = transforms.Compose(trans)

    def __call__(self, img):
        return self.transforms(img)


class ClassificationInferencer(Inferencer):
    """ 分类推理器 """

    def __init__(
            self,
            model,
            weight,
            classes,
            transform=None,
            required_size=None,
            batch_size=8,
            device=None
    ):
        """
        初始化推理器
        :param model: 模型
        :param weight: 模型权重路径，字符串
        :param classes: 模型类别信息，列表
        :param transform: 模型预处理器
        :param inference_size: 模型推理时使用的尺寸 **[height, width]**
        :param required_size: 模型输出时使用的尺寸 **[height, width]**
        :param batch_size: 推理时的批次
        :param device: 推理时使用的设备，默认情况下，cuda可用时使用cuda，否则使用cpu
        """
        super(ClassificationInferencer, self).__init__(
            model,
            weight,
            classes,
            transform,
            required_size,
            batch_size,
            device
        )

    def post_process(self, inputs: Tensor, outputs: Tensor) -> list:
        """
        根据输入输出构造结果
        :param inputs: 输入
        :param outputs: 输出
        :return:
        """
        _, predictions = torch.max(outputs, 1)
        prediction_indices = predictions.to(torch.int8).cpu().numpy().tolist()
        prediction_classes = [{'class': idx} for idx in prediction_indices]
        return prediction_classes


if __name__ == '__main__':
    # 模型
    from model import get_cla_model
    classes = ['出血', '坏死', '实质', '淋巴', '空泡', '空白', '间质']
    model = get_cla_model(classes)
    weight = '../weights/cla_model.pth'
    # inferencer = ClassificationInferencer(model, weight, classes, batch_size=32)
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\cla_slices')
    # print(predictions)
    # inferencer = ClassificationInferencer(model, weight, classes, batch_size=16, inference_size=(255, 250), required_size=[512, 200])
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\cla_slices')
    # inferencer = ClassificationInferencer(model, weight, classes, batch_size=64, inference_size=(255, 250), required_size=[512, 200], device='cpu')
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\cla_slices')
    # print(predictions)
    print('unit test is done!')
