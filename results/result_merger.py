import logging

import numpy as np

from binders import get_progress_binder
from results import SegmentationResult, ClassificationResult
from utils import get_inferencer_size


class ResultMerger(object):
    """ 结果融合器 """
    def __init__(self, seg_result: SegmentationResult, cla_result: ClassificationResult, origin_size, drop_last=False):
        """
        初始化结果对象
        :param seg_result: 分割结果对象
        :param cla_result: 分类结果对象
        :param origin_size: 原始图片大小
        :param drop_last: 是否舍弃图片边缘
        """
        self.seg_result = seg_result
        self.cla_result = cla_result
        self.origin_size = origin_size
        self.drop_last = drop_last
        self.logger = logging.getLogger(name='file-logger')
        self.progress_binder = get_progress_binder()
        # 获取信息
        self.origin_width, self.origin_height = self.origin_size
        self.seg_down_sample = self.seg_result.down_sample
        self.cla_down_sample = self.cla_result.down_sample
        self.seg_slice_width, self.seg_slice_height = self.seg_result.slice_size
        self.cla_slice_width, self.cla_slice_height = self.cla_result.slice_size
        self._prepare_size_info()
        # 确保映射大小匹配
        assert self.seg_slice_width * self.seg_down_sample % (self.cla_slice_width * self.cla_down_sample) == 0
        assert self.seg_slice_height * self.seg_down_sample % (self.cla_slice_height * self.cla_down_sample) == 0
        # 构建结果集
        self.scan_result()

    def _prepare_size_info(self):
        """
        准备图片尺寸相关信息
        :return:
        """
        self.seg_scaled_width, self.seg_scaled_height, self.seg_cols, self.seg_rows = get_inferencer_size(
            self.origin_size,
            self.seg_down_sample,
            self.seg_result.slice_size,
            self.drop_last,
            type='size'
        )
        self.cla_scaled_width, self.cla_scaled_height, self.cla_cols, self.cla_rows = get_inferencer_size(
            self.origin_size,
            self.cla_down_sample,
            self.cla_result.slice_size,
            self.drop_last,
            type='size'
        )

    def scan_result(self):
        """
        扫描results
        :return: 无
        """
        results = np.zeros((self.cla_rows, self.cla_cols, 2), dtype=int)
        counts = dict()
        self.logger.info('开始融合分类分割结果...')
        self.progress_binder.set_stage(0, 'MIX_RESULT')
        for r in range(self.cla_rows):
            for c in range(self.cla_cols):
                origin_x1, origin_y1 = self.cla_result.box_to_origin(r, c)
                origin_x2, origin_y2 = self.cla_result.box_to_origin(r + 1, c + 1)
                seg_class = self.seg_result.get_origin_region_result(origin_x1, origin_y1, origin_x2, origin_y2)
                cla_class = self.cla_result[r, c]
                # result r, c -> seg_class, cla_class
                results[r, c, :] = seg_class, cla_class
                # counts
                counts[(seg_class, cla_class)] = counts.get((seg_class, cla_class), 0) + 1
            if r % 4 == 0:
                self.progress_binder.set_stage((r + 1) / self.cla_rows, 'MIX_RESULT')
        self.logger.info('分类分割结果融合完成！')
        self.progress_binder.set_stage(100, 'MIX_RESULT')
        self.results = results
        self.counts = counts

    def get_summary_table(self, seg_classes: list, cla_classes: list):
        """
        扫描dict_results
        :return: 无
        """
        # idx_to_seg_class = {idx: clazz for idx, clazz in enumerate(seg_classes)}
        # idx_to_cla_class = {idx: clazz for idx, clazz in enumerate(cla_classes)}
        # count_res = np.array([[self.counts.get((r, c), 0) for c in range(len(cla_classes))] for r in range(len(seg_classes))], dtype=int)
        # ratio_res = count_res / (1.0 * self.cla_rows * self.cla_cols)
        classes = [f'{cla_class}占{seg_class}' for seg_class in seg_classes for cla_class in cla_classes]
        count_res = [self.counts.get((seg_idx, cla_idx), 0) for seg_idx in range(len(seg_classes)) for cla_idx in range(len(cla_classes))]
        ratio_res = [count / sum(count_res) for count in count_res]
        classes_str = '\t'.join(list(map(str, ['分类占分割'] + classes)))
        count_str = '\t'.join(list(map(str, ['计数'] + count_res)))
        ratio_str = '\t'.join(list(map(str, ['占比'] + ratio_res)))
        res = '\n'.join([classes_str, count_str, ratio_str])
        return res

    def scaled_to_origin(self, scaled_x1: int, scaled_y1: int, scaled_x2: int, scaled_y2: int, down_sample: int):
        """
        缩放后区域 -> 原始区域
        :param scaled_x1: 左上角点横坐标，经过缩放的坐标
        :param scaled_y1: 左上角点纵坐标，经过缩放的坐标
        :param scaled_x2: 右下角点横坐标，经过缩放的坐标
        :param scaled_y2: 右下角点纵坐标，经过缩放的坐标
        :param down_sample: 降采样倍数
        :return: (origin_x1, origin_y1, origin_x2, origin_y2)
        """
        return scaled_x1 * down_sample, scaled_y1 * down_sample, scaled_x2 * down_sample, scaled_y2 * down_sample

    def origin_to_scaled(self, origin_x1: int, origin_y1: int, origin_x2: int, origin_y2: int, down_sample: int):
        """
        原始区域 -> 缩放后区域
        :param origin_x1: 左上角点横坐标，未经过缩放的坐标
        :param origin_y1: 左上角点纵坐标，未经过缩放的坐标
        :param origin_x2: 右下角点横坐标，未经过缩放的坐标
        :param origin_y2: 右下角点纵坐标，未经过缩放的坐标
        :param down_sample: 降采样倍数
        :return: (scaled_x1, scaled_y1, scaled_x2, scaled_y2)
        """
        return origin_x1 // down_sample, origin_y1 // down_sample, origin_x2 // down_sample, origin_y2 // down_sample

    def scaled_to_scaled(self, scaled_x1: int, scaled_y1: int, scaled_x2: int, scaled_y2: int, self_down_sample: int,
                         target_down_sample: int):
        """
        缩放后区域1 -> 缩放后区域2
        :param origin_x1: 左上角点横坐标，未经过缩放的坐标
        :param origin_y1: 左上角点纵坐标，未经过缩放的坐标
        :param origin_x2: 右下角点横坐标，未经过缩放的坐标
        :param origin_y2: 右下角点纵坐标，未经过缩放的坐标
        :param self_down_sample: 自身坐标对应的图像的降采样倍数
        :param target_down_sample: 目标坐标对应的图像的降采样倍数
        :return: (scaled_x1, scaled_y1, scaled_x2, scaled_y2)
        """
        origin_x1, origin_y1, origin_x2, origin_y2 = self.scaled_to_origin(scaled_x1, scaled_y1, scaled_x2, scaled_y2,
                                                                           self_down_sample)
        return self.origin_to_scaled(origin_x1, origin_y1, origin_x2, origin_y2, target_down_sample)

    def cla_to_seg(self, x1: int, y1: int, x2: int, y2: int):
        """
        分类区域 -> 分割区域
        :param x1: 左上角点横坐标，分类区域
        :param y1: 左上角点纵坐标，分类区域
        :param x2: 右下角点横坐标，分类区域
        :param y2: 右下角点纵坐标，分类区域
        :return: (x1, y1, x2, y2)
        """
        return self.scaled_to_scaled(x1, y1, x2, y2, self.cla_down_sample, self.seg_down_sample)

    def seg_to_cla(self, x1: int, y1: int, x2: int, y2: int):
        """
        分割区域 -> 分类区域
        :param x1: 左上角点横坐标，分割区域
        :param y1: 左上角点纵坐标，分割区域
        :param x2: 右下角点横坐标，分割区域
        :param y2: 右下角点纵坐标，分割区域
        :return: (x1, y1, x2, y2)
        """
        return self.scaled_to_scaled(x1, y1, x2, y2, self.seg_down_sample, self.cla_down_sample)


if __name__ == '__main__':
    from utils import *
    file = r"E:\BaiduNetdiskDownload\TCGA-2Y-A9GY-01Z-00-DX1.9AF8DAB8-B99C-4484-A065-20E7345E1FF4.svs"
    # 分类结果
    cla_classes = ['出血', '坏死', '实质', '淋巴', '空泡', '空白', '间质']
    predictions = read_object('../tmp/cla_dict_result.pkl')
    cla_result = ClassificationResult(predictions, (1024, 1024), 1)
    # 分割结果
    seg_classes = ['_background_', 'Normal', 'Tumor']
    predictions = read_object('../tmp/seg_dict_result.pkl')
    seg_result = SegmentationResult(predictions, (2048, 2048), 16)
    # 融合结果
    mix_result = read_object('../tmp/mix_result.pkl')
    # mix_result = ResultMerger(seg_result, cla_result, get_image_size(file), drop_last=False)
    # write_object(mix_result, '../tmp/mix_result.pkl')
    print(mix_result.get_summary_table(seg_classes, cla_classes))
