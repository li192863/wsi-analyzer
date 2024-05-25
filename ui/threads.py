import ctypes
import inspect
import logging
import threading
import time
import traceback

from PySide6.QtCore import QThread, Signal

from engine import Processor
from utils import write_config, read_config


class ProcessEmitter(QThread):
    """ 处理信号发送器 """
    process_failed_signal = Signal(str)
    process_complete_signal = Signal(str)
    process_stop_signal = Signal(str)


class ProcessThread(threading.Thread):
    """ 转换线程 """
    def __init__(self, config, running_confile_file):
        super(ProcessThread, self).__init__()
        self.config = config  # 包含界面配置
        self.running_confile_file = running_confile_file
        self.emitter = ProcessEmitter()
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
        """
        运行当前线程
        :return: 无
        """
        try:
            processor = Processor(self.running_confile_file)
            processor.process()
            self.emitter.process_complete_signal.emit('已转换完成！')
        except KeyboardInterrupt as e:
            with open('./logs/error.txt', 'w') as f:
                traceback.print_exc(file=f)
            self.emitter.process_stop_signal.emit('处理已终止！')
        except Exception as e:
            with open('./logs/error.txt', 'w') as f:
                traceback.print_exc(file=f)
            self.emitter.process_failed_signal.emit(str(e))

    def stop(self):
        """
        停止当前线程运行
        :return: 无
        """
        self.raise_exc(KeyboardInterrupt)
        while self.is_alive():
            time.sleep(0.1)
            try:
                self.raise_exc(KeyboardInterrupt)
            except Exception as e:
                pass

    def _async_raise(self, tid, exctype):
        """
        使用tid抛出异常
        :param tid: 线程id
        :param exctype: 异常类型
        :return:
        """
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))

        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
            self.emitter.process_stop_signal.emit('处理已终止！')
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def raise_exc(self, exctype):
        """
        抛出异常
        Raises the given exception type in the context of this thread.
        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raise_exc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raise_exc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL: this function is executed in the context of the
        caller thread, to raise an exception in the context of the
        thread represented by this instance.
        :param exctype: 异常类型
        :return: 无
        """
        self._async_raise(self.ident, exctype)
