from builders.Builder import Builder
from inferencers import ClassificationInferencer, SegmentationInferencer, Inferencer
from inferencers.ClassificationInferencer import ClassificationPresetEval
from inferencers.SegmentationInferencer import SegmentationPresetEval
from model import get_cla_model, get_seg_model


class InferencerBuilder(Builder):
    @staticmethod
    def create_inferencer(
            type,
            weight,
            classes,
            inference_size,
            required_size,
            batch_size,
            device=None
    ) -> Inferencer:
        if type == 'cla' or type == 'classification':
            model = get_cla_model(classes)
            transform_cls = ClassificationPresetEval
            return ClassificationInferencer(
                model=model,
                weight=weight,
                classes=classes,
                transform_cls=transform_cls,
                inference_size=inference_size,
                required_size=required_size,
                batch_size=batch_size,
                device=device
            )
        elif type == 'seg' or type == 'segmentation':
            model = get_seg_model(classes)
            transform_cls = SegmentationPresetEval
            return SegmentationInferencer(
                model=model,
                weight=weight,
                classes=classes,
                transform_cls=transform_cls,
                inference_size=inference_size,
                required_size=required_size,
                batch_size=batch_size,
                device=device
            )
        else:
            raise ValueError(f'{repr(type)}为非法的推理器类型！')

    def build_seg_inferencer(self) -> SegmentationInferencer:
        """ 依据配置构造分割推理器 """
        params_dict = {
            'type': 'seg',
            'weight': self.config.inferencer.segmentation.weight,
            'classes': self.config.inferencer.segmentation.classes,
            'inference_size': self.config.inferencer.segmentation.inference_size,  # [h, w]
            'required_size': self.config.slicer.segmentation.slice_size[::-1],  # [w, h] -> [h, w]
            'batch_size': self.config.inferencer.segmentation.batch_size,
            'device': self.config.inferencer.segmentation.device,
        }
        self.logger.debug(f'seg_inferencer参数-{params_dict}')
        return self.build_from_dict(self.create_inferencer, params_dict)

    def build_cla_inferencer(self) -> ClassificationInferencer:
        """ 依据配置构造分类推理器 """
        params_dict = {
            'type': 'cla',
            'weight': self.config.inferencer.classification.weight,
            'classes': self.config.inferencer.classification.classes,
            'inference_size': self.config.inferencer.classification.inference_size,  # [h, w]
            'required_size': self.config.slicer.classification.slice_size[::-1],  # [w, h] -> [h, w]
            'batch_size': self.config.inferencer.classification.batch_size,
            'device': self.config.inferencer.classification.device,
        }
        self.logger.debug(f'cla_inferencer参数-{params_dict}')
        return self.build_from_dict(self.create_inferencer, params_dict)


if __name__ == '__main__':
    inferencer_builder = InferencerBuilder('../conf/settings.yml')
    seg_inferencer = inferencer_builder.build_seg_inferencer()
    cla_inferencer = inferencer_builder.build_cla_inferencer()
    print(seg_inferencer)
    print(cla_inferencer)

