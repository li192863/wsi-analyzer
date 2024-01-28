import logging
from copy import deepcopy


from utils import write_object


class Resumer(object):
    """ 断点恢复器 """
    def __init__(self, file_path, config):
        self.file_path = file_path
        self.config = config
        self.logger = logging.getLogger(name='file-logger')
        # 状态信息
        self.set_state(False, False, False, False)

    def set_state(self, seg_slice_done=None, cla_slice_done=None, seg_inference_done=None, cla_inference_done=None):
        """
        获取/更新内部状态
        :param seg_slice_done: 分割切片完成
        :param cla_slice_done: 分类切片完成
        :param seg_inference_done: 分割推理完成
        :param cla_inference_done: 分类推理完成
        :return: (seg_slice_done, self.cla_slice_done, self.seg_inference_done, self.cla_inference_done)
        """
        if seg_slice_done is not None:
            self.seg_slice_done = seg_slice_done
        if cla_slice_done is not None:
            self.cla_slice_done = cla_slice_done
        if seg_inference_done is not None:
            self.seg_inference_done = seg_inference_done
        if cla_inference_done is not None:
            self.cla_inference_done = cla_inference_done
        # 写入指定位置
        write_object(self, self.file_path)
        self.logger.info(
            f'更新状态信息'
            f'{self.seg_slice_done, self.cla_slice_done, self.seg_inference_done, self.cla_inference_done}'
            f'至{self.file_path}！'
        )
        return self.seg_slice_done, self.cla_slice_done, self.seg_inference_done, self.cla_inference_done

    def resume_self(self, new_file_path, new_config):
        """
        根据新配置，更新Resumer本身
        :param new_config: 新配置文件
        :return: self
        """
        self.logger.info('尝试进行断点恢复...')
        # 更新配置信息
        old_config = deepcopy(self.config)
        # 更新状态信息
        self.resume_state(old_config, new_config)
        # 避免错误覆盖
        self.file_path = new_file_path
        self.config = new_config
        self.set_state()  # 写入磁盘
        self.logger.info('断点恢复完成！')
        return self

    def resume_state(self, old_config, new_config):
        """
        通过对比新旧配置更新自身状态
        :param old_config: 旧配置
        :param new_config: 新配置
        :return:
        """
        # 若未开启自动恢复
        if not new_config.basic.auto_resume:
            self.seg_slice_done = False
            self.cla_slice_done = False
            self.seg_inference_done = False
            self.cla_inference_done = False
            return
        # 检查配置是否更改
        res = self.has_config_changed(old_config, new_config)
        seg_slice_cfg_changed, cla_slice_cfg_changed, seg_inference_cfg_changed, cla_inference_cfg_changed = res
        self.logger.debug(
            f'配置变化信息'
            f'{seg_slice_cfg_changed, cla_slice_cfg_changed, seg_inference_cfg_changed, cla_inference_cfg_changed}'
        )
        # 更新自身状态信息
        self.seg_slice_done = self.seg_slice_done and not seg_slice_cfg_changed
        self.cla_slice_done = self.cla_slice_done and not cla_slice_cfg_changed
        self.seg_inference_done = self.seg_inference_done and not seg_inference_cfg_changed and self.seg_slice_done and not new_config.basic.force_inference
        self.cla_inference_done = self.cla_inference_done and not cla_inference_cfg_changed and self.cla_slice_done and not new_config.basic.force_inference

    def has_config_changed(self, old_config, new_config):
        """
        检查配置是否发生更改
        :param old_config: 旧配置
        :param new_config: 新配置
        :return: (seg_slice_cfg_changed, cla_slice_cfg_changed, seg_inference_cfg_changed, cla_inference_cfg_changed)
        """
        # 分割切片配置是否更改
        seg_slice_cfg_changed = self.has_seg_slice_config_changed(old_config, new_config)
        # 分类切片配置是否更改
        cla_slice_cfg_changed = self.has_cla_slice_config_changed(old_config, new_config)
        # 分割推理配置是否更改
        seg_inference_cfg_changed = self.has_seg_inference_config_changed(old_config, new_config)
        # 分类推理配置是否更改
        cla_inference_cfg_changed = self.has_cla_inference_config_changed(old_config, new_config)
        return seg_slice_cfg_changed, cla_slice_cfg_changed, seg_inference_cfg_changed, cla_inference_cfg_changed

    def has_seg_slice_config_changed(self, old_config, new_config):
        """
        检查分割切片配置是否更改
        :param old_config: 旧配置
        :param new_config: 新配置
        :return:
        """
        if old_config.slicer.segmentation.slice_size[0] != new_config.slicer.segmentation.slice_size[0]:
            return True
        elif old_config.slicer.segmentation.slice_size[1] != new_config.slicer.segmentation.slice_size[1]:
            return True
        elif old_config.slicer.segmentation.down_sample != new_config.slicer.segmentation.down_sample:
            return True
        elif old_config.slicer.segmentation.prefix != new_config.slicer.segmentation.prefix:
            return True
        elif old_config.slicer.segmentation.suffix != new_config.slicer.segmentation.suffix:
            return True
        elif old_config.slicer.drop_last != new_config.slicer.drop_last:
            return True
        else:
            return False

    def has_cla_slice_config_changed(self, old_config, new_config):
        """
        检查分类切片配置是否更改
        :param old_config: 旧配置
        :param new_config: 新配置
        :return:
        """
        if old_config.slicer.classification.slice_size[0] != new_config.slicer.classification.slice_size[0]:
            return True
        elif old_config.slicer.classification.slice_size[1] != new_config.slicer.classification.slice_size[1]:
            return True
        elif old_config.slicer.classification.down_sample != new_config.slicer.classification.down_sample:
            return True
        elif old_config.slicer.classification.prefix != new_config.slicer.classification.prefix:
            return True
        elif old_config.slicer.classification.suffix != new_config.slicer.classification.suffix:
            return True
        elif old_config.slicer.drop_last != new_config.slicer.drop_last:
            return True
        else:
            return False

    def has_seg_inference_config_changed(self, old_config, new_config):
        """
        检查分割推理配置是否更改
        :param old_config: 旧配置
        :param new_config: 新配置
        :return:
        """
        if old_config.inferencer.segmentation.weight != new_config.inferencer.segmentation.weight:
            return True
        elif old_config.inferencer.segmentation.classes != new_config.inferencer.segmentation.classes:
            return True
        elif old_config.inferencer.segmentation.transforms.resize_size != new_config.inferencer.segmentation.transforms.resize_size:
            return True
        elif old_config.inferencer.segmentation.transforms.crop_size != new_config.inferencer.segmentation.transforms.crop_size:
            return True
        elif old_config.inferencer.segmentation.transforms.mean != new_config.inferencer.segmentation.transforms.mean:
            return True
        elif old_config.inferencer.segmentation.transforms.std != new_config.inferencer.segmentation.transforms.std:
            return True
        else:
            return False

    def has_cla_inference_config_changed(self, old_config, new_config):
        """
        检查分类推理配置是否更改
        :param old_config: 旧配置
        :param new_config: 新配置
        :return:
        """
        if old_config.inferencer.classification.weight != new_config.inferencer.classification.weight:
            return True
        elif old_config.inferencer.classification.classes != new_config.inferencer.classification.classes:
            return True
        elif old_config.inferencer.classification.transforms.resize_size != new_config.inferencer.classification.transforms.resize_size:
            return True
        elif old_config.inferencer.classification.transforms.crop_size != new_config.inferencer.classification.transforms.crop_size:
            return True
        elif old_config.inferencer.classification.transforms.mean != new_config.inferencer.classification.transforms.mean:
            return True
        elif old_config.inferencer.classification.transforms.std != new_config.inferencer.classification.transforms.std:
            return True
        else:
            return False
