import numpy as np

from results.result import Result
from utils import write_image


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
        self.logger.info('开始扫描分类结果...')
        self.progress_binder.set_stage(0, 'CLA_RESULT')
        for i, (file, result) in enumerate(self.dict_results.items()):
            # 解析路径
            d, r, c = self.parse_path(file)
            key, value = (r, c), result['class']
            # slice_paths: (r, c) -> path
            slice_paths[key] = file
            # results: (r, c) -> class_idx
            results[key] = value
            # counts
            counts[value] = counts.get(value, 0) + 1
            if i % 4 == 0:
                self.progress_binder.set_stage((i + 1) / len(self.dict_results), 'CLA_RESULT')
        self.logger.info('分类结果扫描完成！')
        self.progress_binder.set_stage(100, 'CLA_RESULT')
        self.slice_paths = slice_paths
        self.results = results
        self.counts = counts

    def get_summary_table(self, classes: list):
        """
        获取统计表格
        :param classes: 种类信息，列表
        :return:
        """
        # idx_to_class = {idx: clazz for idx, clazz in enumerate(classes)}
        # count_res = {idx_to_class[i]: count for i, count in self.counts.items()}
        # ratio_res = {idx_to_class[i]: count/sum(self.counts.values()) for i, count in self.counts.items()}
        count_res = [self.counts.get(cla_idx, 0) for cla_idx in range(len(classes))]
        ratio_res = [count / sum(count_res) for count in count_res]
        classes_str = '\t'.join(list(map(str, ['分类'] + classes)))
        count_str = '\t'.join(list(map(str, ['计数'] + count_res)))
        ratio_str = '\t'.join(list(map(str, ['占比'] + ratio_res)))
        res = '\n'.join([classes_str, count_str, ratio_str])
        return res

    def get_summary_image(self, origin_size, save_path=None, show_image=False, plot_kwargs=dict(), save_kwargs=dict()):
        """
        获取统计图片
        :param origin_size:
        :return:
        """
        tensor = self.get_origin_region_class(0, 0, *origin_size)
        write_image(
            tensor,
            save_path=save_path,
            show_image=show_image,
            plot_kwargs=plot_kwargs,
            save_kwargs=save_kwargs
        )

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
    inferencer = ClassificationInferencer(model, weight, classes, batch_size=16)
    predictions = read_object('../tmp/cla_dict_result.pkl')
    # predictions = inferencer.inference_folder('E:\Projects\Carcinoma\#Temp\素材\cla_slices')
    # write_object(predictions, '../tmp/cla_dict_result.pkl')
    # 分类结果
    cla_result = ClassificationResult(predictions, (1024, 1024), 1)
    print(cla_result.get_summary_table(classes))

    write_image(cla_result.get_scaled_region_class(0, 0, 2048 * 16, 2048 * 16))
    print(cla_result.get_scaled_region_result(0, 0, 2048 * 16, 2048 * 16))
    write_image(cla_result.get_origin_region_class(0, 0, 2048 * 16, 2048 * 16))
    print(cla_result.get_origin_region_result(0, 0, 2048 * 16, 2048 * 16))

    write_image(cla_result.get_scaled_region_class(2048 * 16, 0, 4096 * 16, 2048 * 16))
    print(cla_result.get_scaled_region_result(2048 * 16, 0, 4096 * 16, 2048 * 16))
    write_image(cla_result.get_origin_region_class(2048 * 16, 0, 4096 * 16, 2048 * 16))
    print(cla_result.get_origin_region_result(2048 * 16, 0, 4096 * 16, 2048 * 16))

    write_image(cla_result.get_scaled_region_class(3072 * 16, 0 * 16, 4096 * 16, 2048 * 16))
    print(cla_result.get_scaled_region_result(3072 * 16, 0 * 16, 4096 * 16, 2048 * 16))
    write_image(cla_result.get_origin_region_class(3072 * 16, 0 * 16, 4096 * 16, 2048 * 16))
    print(cla_result.get_origin_region_result(3072 * 16, 0 * 16, 4096 * 16, 2048 * 16))

    write_image(cla_result.get_scaled_region_class(4096 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    print(cla_result.get_scaled_region_result(4096 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    write_image(cla_result.get_origin_region_class(4096 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    print(cla_result.get_origin_region_result(4096 * 16, 0 * 16, 5120 * 16, 2048 * 16))

    write_image(cla_result.get_scaled_region_class(3072 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    print(cla_result.get_scaled_region_result(3072 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    write_image(cla_result.get_origin_region_class(3072 * 16, 0 * 16, 5120 * 16, 2048 * 16))
    print(cla_result.get_origin_region_result(3072 * 16, 0 * 16, 5120 * 16, 2048 * 16))

    write_image(cla_result.get_scaled_region_class(3072 * 16 + 367, 0 * 16 + 569, 5120 * 16 - 568, 2048 * 16 - 1023))
    write_image(cla_result.get_origin_region_class(3072 * 16 + 367, 0 * 16 + 569, 5120 * 16 - 568, 2048 * 16 - 1023))

    write_image(cla_result.get_scaled_region_class(3072 * 16 - 367, 0 * 16 - 569, 5120 * 16 + 568, 2048 * 16 + 1023))
    write_image(cla_result.get_origin_region_class(3072 * 16 - 367, 0 * 16 - 569, 5120 * 16 + 568, 2048 * 16 + 1023))

    print('unit test is done!')