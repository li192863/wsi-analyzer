import logging

from binders import get_status_binder, get_progress_binder
from builders import SlicerBuilder, InferencerBuilder, ResultBuilder
from engine.file_processor import FileProcessor
from utils import read_config


class Processor(object):
    """ WSI处理器 """
    def __init__(self, config_file):
        """
        初始化处理器，可对某一张病理切片进行处理
        :param config_file: 配置文件
        """
        self.config_file = config_file
        self.config = read_config(self.config_file)
        self.logger = logging.getLogger(name='file-logger')
        self.status_binder = get_status_binder()  # 已创建无需传参
        self.progress_binder = get_progress_binder()  # 已创建无需传参
        # 读取基本配置
        self.filelist = self.config.basic.filelist
        self.auto_resume = self.config.basic.auto_resume
        self.force_inference = self.config.basic.force_inference
        self.result_folder = self.config.basic.result_folder
        # 检查文件信息
        self._prepare_config()
        self._check_config()
        self._build_components()

    def _prepare_config(self):
        """
        准备配置信息
        :return: 无
        """
        self.logger.info('准备配置信息...')
        self.seg_slice_size = self.config.slicer.segmentation.slice_size
        self.cla_slice_size = self.config.slicer.classification.slice_size
        self.seg_down_sample = self.config.slicer.segmentation.down_sample
        self.cla_down_sample = self.config.slicer.classification.down_sample
        self.seg_slice_width, self.seg_slice_height = self.seg_slice_size
        self.cla_slice_width, self.cla_slice_height = self.cla_slice_size

    def _check_config(self):
        """
        检查配置信息
        :return: 无
        """
        self.logger.info('检查配置信息...')
        # 检查文件列表
        if len(self.filelist) <= 0:
            self.logger.error('文件列表不能为空！')
            raise ValueError('文件列表不能为空！')
        # 检查尺寸信息
        if self.seg_slice_width * self.seg_down_sample % (self.cla_slice_width * self.cla_down_sample) != 0:
            self.logger.error('请确保 分割切片宽×分割降采样 mod (分类切片宽×分类降采样) == 0！')
            raise ValueError('请确保 分割切片宽×分割降采样 mod (分类切片宽×分类降采样) == 0！')
        if self.seg_slice_height * self.seg_down_sample % (self.cla_slice_height * self.cla_down_sample) != 0:
            self.logger.error('请确保 分割切片高×分割降采样 mod (分类切片高×分类降采样) == 0！')
            raise ValueError('请确保 分割切片高×分割降采样 mod (分类切片高×分类降采样) == 0！')

    def _build_components(self):
        """
        构建基本组件
        :return:
        """
        self.logger.info('构建基本组件...')
        # 构建切片器，共享使用
        self.slicer_builder = SlicerBuilder(self.config_file)
        self.seg_slicer = self.slicer_builder.build_seg_slicer()
        self.cla_slicer = self.slicer_builder.build_cla_slicer()
        # 构建推理器，共享使用
        self.inferencer_builder = InferencerBuilder(self.config_file)
        self.seg_inferencer = self.inferencer_builder.build_seg_inferencer()
        self.cla_inferencer = self.inferencer_builder.build_cla_inferencer()
        # 构建结果器
        self.result_builder = ResultBuilder(self.config_file)

    def process(self):
        """
        依次对文件列表的文件进行处理
        :return:
        """
        self.logger.info('开始处理...')
        for i, file in enumerate(self.filelist):
            self.status_binder.info(f'正在处理第{i + 1}个文件，共{len(self.filelist)}个')
            image_processor = FileProcessor(file, self)
            image_processor.process()
            self.logger.info(f'处理完成度{(i + 1) * 100 / len(self.filelist):.2f}%')
        self.logger.info('处理完成！')


if __name__ == '__main__':
    processor = Processor('../conf/settings.yml')
    processor.process()