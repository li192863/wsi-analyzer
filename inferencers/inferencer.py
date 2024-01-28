import logging
import os
from abc import ABC, abstractmethod

import torch
import torchvision.transforms.functional as F
from PIL import Image
from torch import Tensor
from torch.utils.data import DataLoader

from binders import ProgressbarBinder


class FileListDataset(torch.utils.data.Dataset):
    """ 文件列表数据集 """
    def __init__(self, images, required_size=None, transform=None):
        self.images = sorted(images)
        self.required_size = required_size
        self.transform = transform
        # 要求长宽
        self.required_height, self.required_width = self.required_size

    def __getitem__(self, idx):
        image = Image.open(self.images[idx]).convert('RGB')
        width, height = image.size
        image = F.pad(image, [0, 0, self.required_width - width, self.required_height - height], fill=255)
        if self.transform:
            image = self.transform(image)
        return image

    def __len__(self):
        return len(self.images)


class FolderDataset(torch.utils.data.Dataset):
    """ 文件夹数据集 """
    def __init__(self, root, required_size, transform=None):
        self.root = root
        self.required_size = required_size
        self.transform = transform
        # 要求长宽
        self.required_height, self.required_width = self.required_size
        # 读取图片
        self.images = sorted(os.listdir(root))

    def __getitem__(self, idx):
        image = Image.open(self.images[idx]).convert('RGB')
        width, height = image.size
        image = F.pad(image, [0, 0, self.required_width - width, self.required_height - height], fill=255)
        # if self.transform:
        #     image = self.transform(image)
        return image

    def __len__(self):
        return len(self.images)


class Inferencer(ABC):
    """ 推理器 """
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
        :param required_size: 模型输出时使用的尺寸 **[height, width]**
        :param batch_size: 推理时的批次
        :param device: 推理时使用的设备，默认情况下，cuda可用时使用cuda，否则使用cpu
        """
        self.model = model
        self.weight = weight
        self.classes = classes
        self.transform = transform
        self.required_size = required_size  # 图片的高宽(h, w)，默认以图片列表第一张图片为输出尺寸
        self.batch_size = batch_size
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.logger = logging.getLogger(name='file-logger')
        self.progress_binder = ProgressbarBinder()
        # 构建映射
        self.class_to_idx = {clazz: idx for idx, clazz in enumerate(self.classes)}
        self.idx_to_class = {idx: clazz for idx, clazz in enumerate(self.classes)}
        # 模型加载
        self.model = self.model.to(self.device)
        # 加载权重
        self.model.load_state_dict(torch.load(weight, map_location=torch.device(self.device)))

    @abstractmethod
    def post_process(self, inputs: Tensor, outputs: Tensor) -> list:
        """
        根据输入输出构造结果
        :param inputs: 输入
        :param outputs: 输出
        :return: 游标当前位置
        """
        pass

    def build_dataloader(self, files: list) -> DataLoader:
        """
        构造数据加载器
        :param files: 图片文件列表
        :return: dataloader
        """
        if self.required_size is None:
            image = Image.open(files[0])
            width, height = image.size
            required_size = (height, width)
        else:
            required_size = self.required_size
        self.logger.debug(f'推理变形尺寸为{required_size}')
        dataset = FileListDataset(files, required_size, transform=self.transform)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
        return dataloader

    def inference_batch(self, files: list) -> dict:
        """
        对一个文件列表里所有图片进行推理
        :param files: 图片文件列表
        :return: 推理结果
        """
        dataloader = self.build_dataloader(files)
        # 逐批次预测
        results = []
        self.logger.info('开始推理...')
        self.model.eval()  # Sets the module in evaluation mode
        with torch.no_grad():  # Disabling gradient calculation
            # with tqdm(dataloader, desc='inference', total=len(dataloader)) as pbar:  # 进度条
            stage, _ = self.progress_binder.get_stage()
            self.progress_binder.set_stage(0, stage)
            for i, inputs in enumerate(dataloader):
                inputs = inputs.to(self.device)  # [b, c, h, w]
                outputs = self.model(inputs)  # [b, num_classes]
                results.extend(self.post_process(inputs, outputs))
                if i % 4 == 0:
                    self.logger.info(f'推理完成度{(i + 1) * 100 / len(dataloader):.2f}%')
                    self.progress_binder.set_stage((i + 1) * 100 / len(dataloader), stage)
        self.logger.info('推理完成！')
        self.progress_binder.set_stage(100, stage)
        return dict(sorted({file: result for file, result in zip(files, results)}.items()))

    def inference_folder(self, folder: str) -> dict:
        """
        对一个文件夹里所有图片进行推理
        :param folder: 图片文件夹
        :param transform: 预测前对图片的变换
        :return: 推理结果
        """
        files = [os.path.join(folder, file_path) for file_path in os.listdir(folder)]
        return self.inference_batch(files)

    def inference_one(self, file: str) -> dict:
        """
        对一个文件图片进行推理
        :param file: 图片文件
        :return: 推理结果
        """
        return self.inference_batch([file])
