import torch
import torch.nn.functional as F
from torch import Tensor
from torchvision.transforms import InterpolationMode, transforms

from inferencers.Inferencer import Inferencer


class SegmentationPresetEval:
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


class SegmentationInferencer(Inferencer):
    def __init__(
            self,
            model,
            weight,
            classes,
            transform_cls=SegmentationPresetEval,
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
        super(SegmentationInferencer, self).__init__(model, weight, classes, transform_cls, inference_size,
                                                     required_size, batch_size, device)

    def post_process(self, inputs: Tensor, outputs: Tensor) -> list:
        """
        根据输入输出构造结果
        :param inputs: 输入
        :param outputs: 输出
        :return: 游标当前位置
        """
        _, predictions = torch.max(outputs, 1)
        if self.required_size is not None:
            predictions = F.interpolate(predictions.unsqueeze(1).to(torch.float32), size=self.required_size,
                                        mode='nearest').squeeze(1)
        prediction_indices = predictions.to(torch.int8).cpu().numpy()  # 图片的高宽(h, w)，默认以图片列表第一张图片为输出尺寸
        prediction_classes = [{'tensor': indices} for indices in prediction_indices]
        return prediction_classes


if __name__ == '__main__':
    from model import get_seg_model
    classes = ['_background_', 'Normal', 'Tumor']
    model = get_seg_model(classes)
    weight = '../weights/seg_model.pth'
    # inferencer = SegmentationInferencer(model, weight, classes, inference_size=(1024, 512), required_size=(3000, 4000), batch_size=2)
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\seg_slices')
    # print(predictions)
    # inferencer = SegmentationInferencer(model, weight, classes, inference_size=(1024, 1024), required_size=(2048, 2048), batch_size=2, device='cpu')
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\seg_slices')
    # print(predictions)
    # inferencer = SegmentationInferencer(model, weight, classes, inference_size=(1024, 1024), required_size=(2048, 2048), batch_size=4, device='cpu')
    # predictions = inferencer.inference_folder(r'E:\test_folder\TCGA-2Y-A9H5-01Z-00-DX108348C3C-A16F-45F6-8AE9-D0613268D703\seg_slices')
    # print(predictions)
    print('unit test is done!')
