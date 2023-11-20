import torch
from torch import Tensor
from torchvision.transforms import InterpolationMode, transforms

from inferencers.Inferencer import Inferencer


class ClassificationPresetEval:
    """ 分类预处理器 """

    def __init__(
            self,
            *,
            resize_size,
            mean=(0.485, 0.456, 0.406),
            std=(0.229, 0.224, 0.225),
            interpolation=InterpolationMode.BILINEAR,
    ):
        self.transforms = transforms.Compose(
            [
                transforms.Resize(resize_size, interpolation=interpolation),
                transforms.PILToTensor(),
                transforms.ConvertImageDtype(torch.float),
                transforms.Normalize(mean=mean, std=std),
            ]
        )

    def __call__(self, img):
        return self.transforms(img)


class ClassificationInferencer(Inferencer):
    """ 分类推理器 """

    def __init__(
            self,
            model,
            weight,
            classes,
            transform_cls=ClassificationPresetEval,
            inference_size=None,
            required_size=None,
            batch_size=8,
            device=None
    ):
        """
        初始化推理器
        :param model: 模型
        :param weight: 模型权重路径，字符串
        :param classes: 模型类别信息，列表
        :param transform_cls: 模型预处理器
        :param inference_size: 模型推理时使用的尺寸 **[height, width]**
        :param required_size: 模型输出时使用的尺寸 **[height, width]**
        :param batch_size: 推理时的批次
        :param device: 推理时使用的设备，默认情况下，cuda可用时使用cuda，否则使用cpu
        """
        super(ClassificationInferencer, self).__init__(model, weight, classes, transform_cls, inference_size,
                                                       required_size, batch_size, device)

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
    transform = ClassificationPresetEval(resize_size=256)
    inferencer = ClassificationInferencer(model, weight, classes, batch_size=32, inference_size=(256, 256))
    predictions = inferencer.inference_folder(r'E:\Projects\Carcinoma\#Temp\素材\cla_slices')
    print(predictions)
