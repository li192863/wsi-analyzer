from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QColor, QPalette

from binders.binder import Binder


class StatusbarEmitter(QObject):
    """
    状态栏消息信号发送器
    """
    status_message_signal = Signal(str, QPalette)

class StatusbarBinder(Binder):
    """
    不同级别对应的消息颜色
    """
    LEVEL_COLORS = {
        'INFO': QColor(17,168,205),  # 蓝色
        'SUCCESS': QColor(13,188,121),  # 绿色
        'WARNING': QColor(208,194,25),  # 黄色
        'ERROR': QColor(189,38,37),  # 红色
    }


    def __init__(self, statusbar=None, name='status binder'):
        """
        创建Binder，绑定状态栏
        :param statusbar: 状态栏
        :param name: 名称
        """
        super(StatusbarBinder, self).__init__(name)
        # 若已实例化则返回
        if statusbar is None:
            return
        # 初始化，仅会被执行1次
        self.statusbar = statusbar
        self.emitter = StatusbarEmitter()
        self.palette = QPalette()
        self.palette.setColor(QPalette.WindowText, self.LEVEL_COLORS['INFO'])

    def _level(self, message, level):
        """
        显示某一级别信息，不同消息类型不同颜色
        :param message: 信息
        :param level: 级别
        :return: 无
        """
        # 消息颜色
        self.palette.setColor(QPalette.WindowText, self.LEVEL_COLORS[level])
        # 发送信号
        self.emitter.status_message_signal.emit(message, self.palette)

    def info(self, message):
        """
        显示普通信息
        :param message: 信息
        :return: 无
        """
        self._level(message, 'INFO')

    def success(self, message):
        """
        显示成功信息
        :param message: 信息
        :return: 无
        """
        self._level(message, 'SUCCESS')

    def warning(self, message):
        """
        显示警告信息
        :param message: 信息
        :return: 无
        """
        self._level(message, 'WARNING')

    def error(self, message):
        """
        显示错误信息
        :param message: 信息
        :return: 无
        """
        self._level(message, 'ERROR')


def get_status_binder(statusbar=None, name='status binder'):
    """
    获取状态绑定器
    :param name: 名称
    :return: 绑定器的弱引用
    """
    return StatusbarBinder(statusbar, name)


if __name__ == '__main__':
    sb1 = StatusbarBinder(None, 'status binder')
    sb2 = StatusbarBinder(None, 'status binder')
    print(id(sb1))
    print(id(sb2))