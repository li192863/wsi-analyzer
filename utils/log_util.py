import logging

from PySide6.QtGui import QColor, QPalette


# class StatusbarHandler(logging.Handler):
#     """ 状态栏日志处理器 """
#     COLORS = {
#         'DEBUG': QColor(17,168,205),  # 蓝色
#         'INFO': QColor(13,188,121),  # 绿色
#         'WARNING': QColor(208,194,25),  # 黄色
#         'ERROR': QColor(189,38,37),  # 红色
#         'CRITICAL': QColor(255, 0, 0)  # 洋红色
#     }
#     def __init__(self, statusbar):
#         super(StatusbarHandler, self).__init__()
#         self.statusbar = statusbar
#         self.palette = QPalette()
#
#     def emit(self, record):
#         """ 触发状态栏显示日志 """
#         # 获取消息
#         log_message = self.format(record)
#         # 消息颜色
#         log_level = record.levelname
#         self.palette.setColor(QPalette.WindowText, self.COLORS[log_level])
#         # 设置颜色
#         if self.statusbar.palette() != self.palette:
#             self.statusbar.setPalette(self.palette)
#         # 显示消息
#         self.statusbar.showMessage(log_message)
#
#
# class ProgressbarHandler(logging.Handler):
#     """ 进度条日志处理器 """
#     def __init__(self, progressbar):
#         super(ProgressbarHandler, self).__init__()
#         self.progressbar = progressbar
#         self.palette = QPalette()
#
#     def emit(self, record) -> None:
#         """ 触发进度条发生变化 """
#         self.progressbar.setValue(int(record) * 100)


def init_file_logger(file='./logs/log.txt', name='file-logger', level=logging.DEBUG) -> logging.Logger:
    """
    初始化文件日志记录器
    :param file: 日志文件
    :param name: 日志记录器名称
    :param level: 日志级别
    :return: 日志记录器（单例、全局唯一）
    """
    # 日志记录器
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    # 文件处理器
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(level)
    file_handler_formatter = logging.Formatter('[%(asctime)s] - [%(levelname)7s] - [%(module)s]: %(message)s')
    file_handler.setFormatter(file_handler_formatter)
    logger.addHandler(file_handler)
    return logger


# def init_statusbar_logger(ui, name='status-logger', level=logging.DEBUG) -> logging.Logger:
#     """
#     初始化状态栏日志记录器
#     :param ui: 日志组件
#     :param name: 日志记录器名称
#     :param level: 日志级别
#     :return: 日志记录器（单例、全局唯一）
#     """
#     # 日志记录器
#     logger = logging.getLogger(name=name)
#     logger.setLevel(level)
#     # 文件处理器
#     status_handler = StatusbarHandler(ui)
#     status_handler.setLevel(level)
#     status_handler_formatter = logging.Formatter('%(message)s')
#     status_handler.setFormatter(status_handler_formatter)
#     logger.addHandler(status_handler)
#     return logger
#
#
# def init_progressbar_logger(ui, name='progress-logger', level=logging.DEBUG) -> logging.Logger:
#     """
#     初始化进度条日志记录器
#     :param ui: 日志组件
#     :param name: 日志记录器名称
#     :param level: 日志级别
#     :return: 日志记录器（单例、全局唯一）
#     """
#     # 日志记录器
#     logger = logging.getLogger(name=name)
#     logger.setLevel(level)
#     # 文件处理器
#     progressbar_handler = ProgressbarHandler(ui)
#     progressbar_handler.setLevel(level)
#     status_handler_formatter = logging.Formatter('%(message)s')
#     progressbar_handler.setFormatter(status_handler_formatter)
#     logger.addHandler(progressbar_handler)
#     return logger


if __name__ == '__main__':
    logger = init_file_logger(name='test')
    logger.info('test1')
    logger.warning('test2')
    logger.error('test3')