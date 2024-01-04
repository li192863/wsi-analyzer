import logging
import os

from binders import get_status_binder, get_progress_binder
from builders import SlicerBuilder, InferencerBuilder, ResultBuilder
from engine import Resumer
from inferencers import ClassificationInferencer, SegmentationInferencer
from slicers import Slicer
from utils import make_directory, read_object, get_image_size, write_object, read_text, write_text


class FileProcessor(object):
    """ 单张图片处理器 """
    def __init__(self, file: str, processor):
        self.file: str = file
        self.processor = processor
        self.logger = logging.getLogger(name='file-logger')
        self.status_binder = get_status_binder()  # 已创建无需传参
        self.progress_binder = get_progress_binder()  # 已创建无需传参
        # 获取构建器
        self.slicer_builder: SlicerBuilder = self.processor.slicer_builder
        self.inferencer_builder: InferencerBuilder = self.processor.inferencer_builder
        self.result_builder: ResultBuilder = self.processor.result_builder
        # 获取切片器
        self.seg_slicer: Slicer = self.processor.seg_slicer
        self.cla_slicer: Slicer = self.processor.cla_slicer
        # 获取推理器
        self.seg_inferencer: ClassificationInferencer = self.processor.seg_inferencer
        self.cla_inferencer: SegmentationInferencer = self.processor.cla_inferencer
        self.get_file_info()

    def get_file_info(self):
        """
        获取文件相关信息
        :return:
        """
        # 基本信息
        self.config = self.processor.config  # 配置
        self.result_folder = self.processor.result_folder  # 结果文件夹
        # 文件信息
        self.filepath, self.filename = os.path.split(self.file)  # 文件路径 文件名称
        self.origin_size = get_image_size(self.file)  # 文件尺寸
        self.filesize = round(os.path.getsize(self.file) / 1024 / 1024, ndigits=2) # 文件大小， 以MB为单位
        # 结果信息
        self.seg_classes = self.config.inferencer.segmentation.classes  # 分割类别
        self.cla_classes = self.config.inferencer.classification.classes  # 分类类别
        self.result_root = os.path.join(self.result_folder or self.filepath, '.'.join(self.filename.split('.')[:-1]) + '_result')  # 结果路径
        # 配置信息
        self.yml_config = read_text(self.processor.config_file)  # 配置文件

    def process(self):
        """
        对文件进行处理
        :return: 无
        """
        # 初始化进度条
        self.progress_binder.set(0)
        # 准备结果文件夹
        self._prepare_results()
        # 准备状态恢复器
        self._prepare_resumer()
        # 生成分割切片
        self.progress_binder.set_stage(0, 'SEG_READ')
        self._seg_slice()
        self.progress_binder.set_stage(100, 'SEG_SLICE')
        # 生成分类切片
        self.progress_binder.set_stage(0, 'CLA_READ')
        self._cla_slice()
        self.progress_binder.set_stage(100, 'CLA_SLICE')
        # 分割切片推理
        self.progress_binder.set_stage(0, 'SEG_INFERENCE')
        self._seg_inference()
        self.progress_binder.set_stage(100, 'SEG_INFERENCE')
        # 分类切片推理
        self.progress_binder.set_stage(0, 'CLA_INFERENCE')
        self._cla_inference()
        self.progress_binder.set_stage(100, 'CLA_INFERENCE')
        # 生成分割结果
        self.progress_binder.set_stage(0, 'SEG_RESULT')
        self._seg_result()
        self.progress_binder.set_stage(100, 'SEG_RESULT')
        # 生成分类结果
        self.progress_binder.set_stage(0, 'CLA_RESULT')
        self._cla_result()
        self.progress_binder.set_stage(100, 'CLA_RESULT')
        # 生成混合结果
        self.progress_binder.set_stage(0, 'MIX_RESULT')
        self._mix_result()
        self.progress_binder.set_stage(100, 'MIX_RESULT')
        # 生成报告文件
        self.generate_reports()
        # 最终化进度条
        self.progress_binder.set(100)

    def _seg_slice(self):
        """
        生成分割切片
        :return: 无
        """
        if not self.resumer.seg_slice_done:
            self.logger.info('正在生成分割切片...')
            make_directory(self.seg_slices_dir, delete_old=True)
            self.seg_slicer.file_to_slices(self.file, image_dir=self.seg_slices_dir)
        else:
            self.logger.info('正在恢复分割切片...')
            assert os.path.exists(self.seg_slices_dir)
        self.resumer.set_state(seg_slice_done=True)

    def _cla_slice(self):
        """
        生成分类切片
        :return: 无
        """
        if not self.resumer.cla_slice_done:
            self.logger.info('正在生成分类切片...')
            make_directory(self.cla_slices_dir, delete_old=True)
            self.cla_slicer.file_to_slices(self.file, image_dir=self.cla_slices_dir)
        else:
            self.logger.info('正在恢复分类切片...')
            assert os.path.exists(self.cla_slices_dir)
        self.resumer.set_state(cla_slice_done=True)

    def _seg_inference(self):
        """
        分割推理
        :return: 无
        """
        if not self.resumer.seg_inference_done:
            self.logger.info('正在进行分割推理...')
            self.seg_dict_results = self.seg_inferencer.inference_folder(self.seg_slices_dir)
            write_object(self.seg_dict_results, self.seg_dict_results_file)
        else:
            self.logger.info('正在恢复分割推理...')
            self.seg_dict_results = read_object(self.seg_dict_results_file)
        self.resumer.set_state(seg_inference_done=True)

    def _cla_inference(self):
        """
        分类推理
        :return: 无
        """
        if not self.resumer.cla_inference_done:
            self.logger.info('正在进行分类推理...')
            self.cla_dict_results = self.cla_inferencer.inference_folder(self.cla_slices_dir)
            write_object(self.cla_dict_results, self.cla_dict_results_file)
        else:
            self.logger.info('正在恢复分类推理...')
            self.cla_dict_results = read_object(self.cla_dict_results_file)
        self.resumer.set_state(cla_inference_done=True)

    def _seg_result(self):
        """
        生成分割结果
        :return: 无
        """
        self.logger.info('正在生成分割结果...')
        self.seg_result = self.result_builder.build_seg_result(self.seg_dict_results)
        # write_object(self.seg_result, self.seg_result_file)
        self.seg_result_table = self.seg_result.get_summary_table()  # 已被动态代理
        self.seg_result.get_summary_image(self.origin_size, save_path=self.seg_result_image_file)

    def _cla_result(self):
        """
        生成分类结果
        :return: 无
        """
        self.logger.info('正在生成分类结果...')
        self.cla_result = self.result_builder.build_cla_result(self.cla_dict_results)
        # write_object(self.cla_result, self.cla_result_file)
        self.cla_result_table = self.cla_result.get_summary_table()  # 已被动态代理
        self.cla_result.get_summary_image(self.origin_size, save_path=self.cla_result_image_file)

    def _mix_result(self):
        """
        生成混合结果
        :return: 无
        """
        self.logger.info('正在生成混合结果...')
        self.mix_result = self.result_builder.build_mix_result(self.seg_result, self.cla_result, self.origin_size)
        # write_object(self.mix_result, self.mix_result_file)
        self.mix_result_table = self.mix_result.get_summary_table()  # 已被动态代理

    def _prepare_results(self):
        """
        准备结果文件夹，结果文件夹如下所示
        |-- result_folder
           |-- filename (result_root)
               |-- seg_slices
                   |-- dx_ri_cj.png
                   |-- ...
               |-- cla_slices
                   |--dx_ri_cj.jpg
                   |-- ...
               |-- intermediate_files
               |-- other-folders
        方式1，指定result_folder，结果文件夹将为result_folder
        方式2，未指定result_folder，结果文件夹将为filepath，即result_folder为file所在的file_path
        :param file: 切片文件
        :return: 生成文件夹
        """
        self.logger.info('准备结果文件夹...')
        # 相关文件夹
        self.result_root = make_directory(self.result_root)
        self.seg_slices_dir = make_directory(os.path.join(self.result_root, 'seg_slices'))
        self.cla_slices_dir = make_directory(os.path.join(self.result_root, 'cla_slices'))
        self.intermediate_files_dir = make_directory(os.path.join(self.result_root, 'intermediate_files'))
        self.analyzed_result_dir = make_directory(os.path.join(self.result_root, 'analyzed_results'))
        # 相关文件
        self.resumer_file = os.path.join(self.intermediate_files_dir, 'resumer.pkl')
        self.seg_dict_results_file = os.path.join(self.intermediate_files_dir, 'seg_dict_results.pkl')
        self.cla_dict_results_file = os.path.join(self.intermediate_files_dir, 'cla_dict_results.pkl')
        self.seg_result_file = os.path.join(self.intermediate_files_dir, 'seg_result.pkl')
        self.cla_result_file = os.path.join(self.intermediate_files_dir, 'cla_result.pkl')
        self.mix_result_file = os.path.join(self.intermediate_files_dir, 'mix_result.pkl')
        self.seg_result_image_file = os.path.join(self.analyzed_result_dir, 'seg_image_result.png')
        self.cla_result_image_file = os.path.join(self.analyzed_result_dir, 'cla_image_result.png')
        # self.mix_image_result_file = os.path.join(self.analyzed_result_dir, 'mix_image_result.png')
        self.report_file = os.path.join(self.result_root, f'report-{self.filename}.md')

    def _prepare_resumer(self):
        """
        准备恢复器
        :return: 恢复器resumer
        """
        self.logger.info('准备断点恢复器...')
        if not os.path.exists(self.resumer_file):
            self.logger.info(f'未发现断点恢复器，已创建恢复器至{self.resumer_file}！')
            self.resumer = Resumer(self.resumer_file, self.config)
            return
        self.logger.info('发现断点恢复器，正在读取...')
        resumer: Resumer = read_object(self.resumer_file)
        self.resumer = resumer.resume_self(self.resumer_file, self.config)

    def generate_reports(self):
        """
        生成报告
        :return:
        """
        self.logger.info('生成结果报告中...')
        text = read_text('./resources/report.md')
        res = text.format(
            filepath = self.filepath,
            filename = self.filename,
            origin_size = self.origin_size,
            filesize = self.filesize,
            seg_classes = self.seg_classes,
            cla_classes = self.cla_classes,
            result_root = self.result_root,
            yml_config = self.yml_config,
            seg_result_table = self.seg_result_table,
            cla_result_table = self.cla_result_table,
            mix_result_table = self.mix_result_table,
        )
        write_text(res, self.report_file)
        self.logger.info(f'结果报告已生成至{self.report_file}！')
