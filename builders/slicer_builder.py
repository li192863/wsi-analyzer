from builders.builder import Builder
from slicers import Slicer, BaseSlicer, VipsSlicer


class SlicerBuilder(Builder):
    @staticmethod
    def create_slicer(
            engine,
            slice_size,
            down_sample,
            drop_last,
            prefix='',
            suffix='.jpg',
            memory=True
    ) -> Slicer:
        if engine == 'base':
            # memory选项不生效
            return BaseSlicer(
                slice_size,
                down_sample=down_sample,
                drop_last=drop_last,
                prefix=prefix,
                suffix=suffix
            )
        elif engine == 'vips':
            return VipsSlicer(
                slice_size,
                down_sample=down_sample,
                drop_last=drop_last,
                prefix=prefix,
                suffix=suffix,
                memory=memory
            )
        else:
            raise ValueError(f'{repr(engine)}为非法的切片器类型！')

    def build_seg_slicer(self) -> Slicer:
        """ 依据配置构造分割切片器 """
        params_dict = {
            'engine': self.config.slicer.engine,
            'slice_size': self.config.slicer.segmentation.slice_size,
            'down_sample': self.config.slicer.segmentation.down_sample,
            'drop_last': self.config.slicer.drop_last,
            'prefix': self.config.slicer.segmentation.prefix,
            'suffix': self.config.slicer.segmentation.suffix,
            'memory': self.config.slicer.segmentation.memory
        }
        self.logger.debug(f'seg_slicer参数-{params_dict}')
        return self.build_from_dict(self.create_slicer, params_dict)

    def build_cla_slicer(self) -> Slicer:
        """ 依据配置构造分类切片器 """
        params_dict = {
            'engine': self.config.slicer.engine,
            'slice_size': self.config.slicer.classification.slice_size,
            'down_sample': self.config.slicer.classification.down_sample,
            'drop_last': self.config.slicer.drop_last,
            'prefix': self.config.slicer.classification.prefix,
            'suffix': self.config.slicer.classification.suffix,
            'memory': self.config.slicer.classification.memory
        }
        self.logger.debug(f'cla_slicer参数-{params_dict}')
        return self.build_from_dict(self.create_slicer, params_dict)


if __name__ == '__main__':
    slicer_builder = SlicerBuilder('../conf/settings.yml')
    seg_slicer = slicer_builder.build_seg_slicer()
    cla_slicer = slicer_builder.build_cla_slicer()
    print(seg_slicer)
    print(cla_slicer)
