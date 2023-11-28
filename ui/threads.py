import logging
import traceback

from PySide2.QtCore import QThread, Signal

from engine import Processor
from utils import write_config, read_config


class ProcessThread(QThread):
    """ 转换线程 """
    process_failed_signal = Signal(str)
    process_complete_signal = Signal(str)
    def __init__(self, config, running_confile_file):
        super(ProcessThread, self).__init__()
        self.config = config  # 包含界面配置
        self.running_confile_file = running_confile_file
        self.logger = logging.getLogger('file-logger')

        self.write_config()
        self.logger.debug(read_config(self.running_confile_file))

    def write_config(self):
        """
        写入当前配置
        :return:
        """
        write_config(self.config, self.running_confile_file)

    def run(self):
        try:
            processor = Processor(self.running_confile_file)
            processor.process()
            self.process_complete_signal.emit('已转换完成！')
        except Exception as e:
            with open('./logs/error.txt', 'w') as f:
                traceback.print_exc(file=f)
            self.process_failed_signal.emit(str(e))