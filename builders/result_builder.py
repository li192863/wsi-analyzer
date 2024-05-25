from functools import partial
from typing import Union

from builders.builder import Builder
from results import Result, ClassificationResult, SegmentationResult, ResultMerger


class ResultBuilder(Builder):
    @staticmethod
    def create_result(
            type,
            dict_results=None,
            slice_size=None,
            down_sample=None,
            naming_regex=None,
            prefix=None,
            suffix=None,
            seg_result=None,
            cla_result=None,
            origin_size=None,
            drop_last=None,
    ) -> Union[Result, ResultMerger]:
        if type == 'cla' or type == 'classification':
            assert suffix.startswith('.')
            naming_regex = f'{prefix}{naming_regex}\\.{suffix[1:]}'
            return ClassificationResult(
                dict_results=dict_results,
                slice_size=slice_size,
                down_sample=down_sample,
                naming_regex=naming_regex,
            )
        elif type == 'seg' or type == 'segmentation':
            assert suffix.startswith('.')
            naming_regex = f'{prefix}{naming_regex}\\.{suffix[1:]}'
            return SegmentationResult(
                dict_results=dict_results,
                slice_size=slice_size,
                down_sample=down_sample,
                naming_regex=naming_regex,
            )
        elif type == 'mix' or type == 'mixed':
            return ResultMerger(
                seg_result=seg_result,
                cla_result=cla_result,
                origin_size=origin_size,
                drop_last=drop_last
            )
        else:
            raise ValueError(f'{repr(type)}为非法的结果器类型！')

    def build_seg_result(self, dict_results) -> SegmentationResult:
        """ 依据配置构造分割结果 """
        params_dict = {
            'type': 'seg',
            'dict_results': dict_results,
            'slice_size': self.config.slicer.segmentation.slice_size,
            'down_sample': self.config.slicer.segmentation.down_sample,
            'naming_regex': self.config.result.segmentation.naming_regex,
            'prefix': self.config.slicer.segmentation.prefix,
            'suffix': self.config.slicer.segmentation.suffix,
        }
        seg_result_log_info = {
            key: value if key != "dict_results" else "***HIDDEN***" for key, value in params_dict.items()
        }
        self.logger.debug(f'seg_result参数 - {seg_result_log_info}')
        seg_result: SegmentationResult = self.build_from_dict(self.create_result, params_dict)
        # get_summary_table
        seg_result.get_summary_table = partial(
            seg_result.get_summary_table,
            classes=self.config.inferencer.segmentation.classes
        )
        self.logger.debug('已代理seg_result的get_summary_table方法！')
        # get_summary_image
        plot_kwargs = self.config.result.segmentation.summary_image.plot_kwargs
        plot_kwargs.vmin, plot_kwargs.vmax = 0, len(self.config.inferencer.segmentation.classes) - 1
        save_kwargs = self.config.result.segmentation.summary_image.save_kwargs
        seg_result.get_summary_image = partial(
            seg_result.get_summary_image,
            show_image=self.config.result.segmentation.summary_image.show_image,
            plot_kwargs=plot_kwargs,
            save_kwargs=save_kwargs,
        )
        self.logger.debug('已代理seg_result的get_summary_image方法！')
        return seg_result

    def build_cla_result(self, dict_results) -> ClassificationResult:
        """ 依据配置构造分类结果 """
        params_dict = {
            'type': 'cla',
            'dict_results': dict_results,
            'slice_size': self.config.slicer.classification.slice_size,
            'down_sample': self.config.slicer.classification.down_sample,
            'naming_regex': self.config.result.classification.naming_regex,
            'prefix': self.config.slicer.classification.prefix,
            'suffix': self.config.slicer.classification.suffix,
        }
        cla_result_log_info = {
            key: value if key != "dict_results" else "***HIDDEN***" for key, value in params_dict.items()
        }
        self.logger.debug(f'cla_result参数 - {cla_result_log_info}')
        cla_result:ClassificationResult = self.build_from_dict(self.create_result, params_dict)
        # get_summary_table
        cla_result.get_summary_table = partial(
            cla_result.get_summary_table,
            classes=self.config.inferencer.classification.classes
        )
        self.logger.debug('已代理cla_result的get_summary_table方法！')
        # get_summary_image
        # plot_kwargs={'cmap':'viridis', 'vmin':0, 'vmax':6}, save_kwargs={'dpi':256})
        # get_summary_image
        plot_kwargs = self.config.result.classification.summary_image.plot_kwargs
        plot_kwargs.vmin, plot_kwargs.vmax = 0, len(self.config.inferencer.classification.classes) - 1
        save_kwargs = self.config.result.classification.summary_image.save_kwargs
        cla_result.get_summary_image = partial(
            cla_result.get_summary_image,
            show_image=self.config.result.classification.summary_image.show_image,
            plot_kwargs=plot_kwargs,
            save_kwargs=save_kwargs,
        )
        self.logger.debug('已代理cla_result的get_summary_image方法！')
        return cla_result

    def build_mix_result(self, seg_result, cla_result, origin_size):
        """ 依据配置构造混合结果 """
        params_dict = {
            'type': 'mix',
            'seg_result': seg_result,
            'cla_result': cla_result,
            'origin_size': origin_size,
            'drop_last': self.config.slicer.drop_last
        }
        self.logger.debug(f'mix_result参数-{params_dict}')
        mix_result: ResultMerger = self.build_from_dict(self.create_result, params_dict)
        # get_summary_table
        mix_result.get_summary_table = partial(
            mix_result.get_summary_table,
            seg_classes=self.config.inferencer.segmentation.classes,
            cla_classes=self.config.inferencer.classification.classes,
        )
        self.logger.debug('已代理mix_result的get_summary_table方法！')
        return mix_result


if __name__ == '__main__':
    from utils import *
    result_builder = ResultBuilder('../conf/settings.yml')
    seg_result = result_builder.build_seg_result(result_builder.build_from_file('../tmp/seg_dict_result.pkl'))
    cla_result = result_builder.build_cla_result(result_builder.build_from_file('../tmp/cla_dict_result.pkl'))
    mix_result = result_builder.build_mix_result(seg_result, cla_result, get_image_size(r"E:\Projects\Carcinoma\#Temp\new_test\TCGA-2Y-A9H5-01Z-00-DX1.08348C3C-A16F-45F6-8AE9-D0613268D703.svs"))
    print(seg_result)
    print(cla_result)
    print(mix_result)

