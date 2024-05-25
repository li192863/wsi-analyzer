from PySide6.QtCore import QObject, Signal

from binders.binder import Binder


class ProgressbarEmitter(QObject):
    """
    进度条更新信号发送器
    """
    progress_update_signal = Signal(float)


class ProgressbarBinder(Binder):
    """
    不同阶段对应的进度条占比
    """
    STAGE_PORTIONS = [
        ('SEG_READ', 5),
        ('SEG_SLICE', 15),
        ('CLA_READ', 5),
        ('CLA_SLICE', 15),
        ('SEG_INFERENCE', 20),
        ('CLA_INFERENCE', 20),
        ('SEG_RESULT', 5),
        ('CLA_RESULT', 5),
        ('MIX_RESULT', 10)
    ]

    def __init__(self, progressbar=None, name='progress binder'):
        """
        创建Binder，绑定进度条
        :param progressbar: 进度条
        :param name: 名称
        """
        super(ProgressbarBinder, self).__init__(name)
        # 若已实例化则返回
        if progressbar is None:
            return
        # 初始化，仅会被执行1次
        self.progressbar = progressbar
        self.emitter = ProgressbarEmitter()

        self.value = 0.00
        n = len(self.STAGE_PORTIONS)
        self.stages = [stage_portion[0] for stage_portion in self.STAGE_PORTIONS]
        self.portions = [stage_portion[1] for stage_portion in self.STAGE_PORTIONS]
        self.stage_to_idx = {self.stages[i]: i for i in range(n)}
        self.stage_to_portion = {self.stages[i]: self.portions[i] for i in range(n)}
        self.starts = [sum(self.portions[:i]) for i in range(n)]
        self.ends = [sum(self.portions[:i + 1]) for i in range(n)]
        if self.ends[-1] != 100:
            raise ValueError('请确保STAGE_PORTIONS值之和为100！')

    def set(self, value):
        """
        设置总进度条的值
        :param value: 总进度条的值 0 ~ 100
        :return: 无
        """
        # 容错
        self.value = max(0.0, value)
        self.value = min(100.0, value)
        # 若更新值超过阈值，则发送信号
        if (abs(self.value - self.progressbar.value()) >= 1):
            self.emitter.progress_update_signal.emit(self.value)

    def get(self):
        """
        获取总进度条的值
        :return: 总进度条的值
        """
        return self.value

    def update(self, delta_value):
        """
        更新总进度条的值
        :param delta_value: 总进度条变化值 0 ~ 100
        :return: 无
        """
        # current_value = self.get()
        # self.set(current_value + delta_value)
        self.set(self.value + delta_value)

    def set_stage(self, stage_value, stage):
        """
        设置某一阶段的进度条的值
        :param stage_value: 阶段进度条的值 0 ~ 100
        :param stage: 阶段
        :return: 无
        """
        try:
            start, end = self.starts[self.stage_to_idx[stage]], self.ends[self.stage_to_idx[stage]]
            # y - start = ((end - start) / 100) * (x - 0) ==>  y = (end - start) * x / 100 + start
            self.value = (end - start) * stage_value / 100.0 + start
            self.set(self.value)
        except Exception as e:
            self.logger.error('设置阶段状态失败！')

    def get_stage(self):
        """
        获取某一阶段以及阶段进度条值
        :param value: 阶段进度条的值 0 ~ 100
        :param stage: 阶段
        :return: (stage, stage_value)
        """
        try:
            # find first idx where self.starts[idx] <= v_float
            global idx, start, end
            for idx, (start, end) in enumerate(zip(self.starts, self.ends)):
                if self.value >= start and self.value < end:
                    break
            # y - start = ((end - start) / 100) * (x - 0) ==>  x = 100 * (y - start) / (end - start)
            stage_value = 100 * (self.value - start) / (end - start)
            # 容错
            stage_value = max(0.0, stage_value)
            stage_value = min(100.0, stage_value)
            return self.stages[idx], stage_value
        except Exception as e:
            self.logger.error(f'获取阶段状态失败！')
            return 'UNKNOWN', 0

    def update_stage(self, stage_delta_value, stage):
        """
        更新某一阶段的进度条的值
        :param stage_delta_value: 阶段进度条变化值 0 ~ 100
        :param stage: 阶段
        :return: 无
        """
        try:
            current_stage, current_stage_value = self.get_stage()
            self.set_stage(current_stage_value + stage_delta_value, stage)
        except Exception as e:
            self.logger.error('更新阶段状态失败！')

    def set_current_stage(self, stage_value):
        """
        设置当前某一阶段的进度条的值
        :param stage_value: 阶段进度条的值 0 ~ 100
        :return: 无
        """
        self.set_stage(stage_value, self.get_stage()[0])


def get_progress_binder(progressbar=None, name='progress binder'):
    """
    获取进度绑定器
    :param name: 名称
    :return: 绑定器的弱引用
    """
    return ProgressbarBinder(progressbar, name)


if __name__ == '__main__':
    class Progressbar(object):
        def __init__(self):
            self.value = 0
        def setValue(self, value):
            self.value = value
    pb = Progressbar()

    pb1 = ProgressbarBinder(pb, 'progress binder')
    pb2 = ProgressbarBinder(pb, 'progress binder')
    print(id(pb1))
    print(id(pb2))
    print()

    pb1.set(0)
    print(pb2.get())
    pb1.set(100)
    print(pb2.get())
    pb1.set(60.51)
    print(pb2.get())
    pb1.set(50.50)
    print(pb2.get())
    pb1.set(40.49)
    print(pb2.get())
    print()

    pb1.update(10.49)
    print(pb2.get())
    pb1.update(10.50)
    print(pb2.get())
    pb1.update(10.51)
    print(pb2.get())
    print()

    pb1.set_stage(0, 'SEG_SLICE')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.set_stage(49, 'SEG_SLICE')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.set_stage(100, 'SEG_SLICE')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.set_stage(0, 'CLA_SLICE')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.set_stage(0, 'MIX_RESULT')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.set_stage(51, 'MIX_RESULT')
    print(pb2.get())
    print(pb2.get_stage())
    pb1.update_stage(49, 'MIX_RESULT')
    print(pb2.get())
    print(pb2.get_stage())

    print('unit test is done!')
