import pickle

import numpy as np

from results.Result import Result


class ClassificationResult(Result):
    """ 分类结果 """
    default_value = 5
    def __init__(self, dict_results, slice_size, down_sample, naming_regex=r'd(\d+)_r(\d+)_c(\d+)\..*'):
        """
        初始化结果对象
        :param dict_results: 结果字典
        :param slice_size: 切片大小 [width, height]
        :param down_sample: 降采样倍数
        :param naming_regex: 文件命名的正则表达式
        """
        super(ClassificationResult, self).__init__(dict_results, slice_size, down_sample, naming_regex)

    def scan_dict_results(self):
        """
        扫描dict_results
        :return: 无
        """
        slice_paths, results, counts = dict(), dict(), dict()
        for file, result in self.dict_results.items():
            # 解析路径
            d, r, c = self.parse_path(file)
            key, value = (r, c), result['class']
            # slice_paths: (r, c) -> path
            slice_paths[key] = file
            # results: (r, c) -> class_idx
            results[key] = value
            # counts
            counts[value] = counts.get(value, 0) + 1
        self.slice_paths = slice_paths
        self.results = results
        self.counts = counts
        # self.counts[self.default_value] = max_r * max_c - sum(counts.values())  # 处理缺失值
        # self.ratios = {cla_idx: count / max_r / max_c for cla_idx, count in counts.items()}

    def get_summary(self, classes: list):
        """
        统计信息
        :param classes: 种类信息，列表
        :return:
        """
        idx_to_class = {idx: clazz for idx, clazz in enumerate(classes)}
        count_res = {idx_to_class[i]: count for i, count in self.counts.items()}
        ratio_res = {idx_to_class[i]: count/sum(self.counts.values()) for i, count in self.counts.items()}
        return count_res, ratio_res

    def get_scaled_region_class(self, scaled_x1: int, scaled_y1: int, scaled_x2: int, scaled_y2: int):
        """
        获取某一区域的分类的Class
        :param scaled_x1: 左上角点横坐标，经过缩放的坐标
        :param scaled_y1: 左上角点纵坐标，经过缩放的坐标
        :param scaled_x2: 右下角点横坐标 + 1，经过缩放的坐标
        :param scaled_y2: 右下角点纵坐标 + 1，经过缩放的坐标
        :return: Tensor
        """
        r1, c1 = self.scaled_to_box(scaled_x1, scaled_y1)
        r2, c2 = self.scaled_to_box(scaled_x2 - 1, scaled_y2 - 1)  # note: minus 1 to get right bottom pixel's position
        rows, cols = r2 - r1 + 1, c2 - c1 + 1
        res = np.empty((rows, cols), dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                res[i, j] = self[r1 + i, c1 + j]
        # r_s = scaled_y1 % self.slice_height
        # r_e = r_s + scaled_y2 - scaled_y1
        # c_s = scaled_x1 % self.slice_width
        # c_e = c_s + scaled_x2 - scaled_x1
        return res

    def get_scaled_region_result(self, scaled_x1: int, scaled_y1: int, scaled_x2: int, scaled_y2: int):
        """
        获取某一区域的分类的结果
        :param scaled_x1: 左上角点横坐标，经过缩放的坐标
        :param scaled_y1: 左上角点纵坐标，经过缩放的坐标
        :param scaled_x2: 右下角点横坐标 + 1，经过缩放的坐标
        :param scaled_y2: 右下角点纵坐标 + 1，经过缩放的坐标
        :return: Index
        """
        res = self.get_scaled_region_class(scaled_x1, scaled_y1, scaled_x2, scaled_y2)
        unique_values, counts = np.unique(res, return_counts=True)
        mode_index = np.argmax(counts)
        return unique_values[mode_index]

    def get_origin_region_class(self, origin_x1: int, origin_y1: int, origin_x2: int, origin_y2: int):
        """
        获取某一区域的分类的Class
        :param origin_x1: 左上角点横坐标，未经过缩放的坐标
        :param origin_y1: 左上角点纵坐标，未经过缩放的坐标
        :param origin_x2: 右下角点横坐标 + 1，未经过缩放的坐标
        :param origin_y2: 右下角点纵坐标 + 1，未经过缩放的坐标
        :return: Tensor
        """
        scaled_x1, scaled_y1, scaled_x2, scaled_y2 = \
            origin_x1 // self.down_sample, origin_y1 // self.down_sample, origin_x2 // self.down_sample, origin_y2 // self.down_sample
        return self.get_scaled_region_class(scaled_x1, scaled_y1, scaled_x2, scaled_y2)

    def get_origin_region_result(self, origin_x1: int, origin_y1: int, origin_x2: int, origin_y2: int):
        """
        获取某一区域的分类的结果
        :param origin_x1: 左上角点横坐标，未经过缩放的坐标
        :param origin_y1: 左上角点纵坐标，未经过缩放的坐标
        :param origin_x2: 右下角点横坐标 + 1，未经过缩放的坐标
        :param origin_y2: 右下角点纵坐标 + 1，未经过缩放的坐标
        :return: Tensor
        """
        scaled_x1, scaled_y1, scaled_x2, scaled_y2 = \
            origin_x1 // self.down_sample, origin_y1 // self.down_sample, origin_x2 // self.down_sample, origin_y2 // self.down_sample
        return self.get_scaled_region_result(scaled_x1, scaled_y1, scaled_x2, scaled_y2)


if __name__ == '__main__':
    from model import get_cla_model
    from inferencers import ClassificationInferencer
    from utils import *
    classes = ['出血', '坏死', '实质', '淋巴', '空泡', '空白', '间质']
    model = get_cla_model(classes)
    weight = '../weights/cla_model.pth'
    inferencer = ClassificationInferencer(model, weight, classes, batch_size=32)
    predictions = read_object('../tmp/cla_dict_result.pkl')
    # 分割结果
    cla_result = ClassificationResult(predictions, (256, 256), 1)
    print(cla_result)
