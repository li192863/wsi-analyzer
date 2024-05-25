import logging
import threading


class Binder(object):
    """ 绑定器，其子类与某一UI元素绑定（进度条、状态栏等），线程安全的单例 """
    _instance = None
    _lock = threading.Lock()

    def __init__(self, name='binder'):
        self.name = name
        self.logger = logging.getLogger('file-logger')

    def __new__(cls, *args, **kwargs):
        """ 创建一个新对象 """
        # 双重检验锁
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Binder, cls).__new__(cls)
                    cls._instance.__init__(*args, **kwargs)
        return cls._instance


def get_binder(name):
    """
    获取绑定器
    :param name: 名称
    :return: 绑定器的弱引用
    """
    return Binder(name)


if __name__ == '__main__':
    b1 = Binder('bbb')
    b2 = Binder('ccc')
    b3 = Binder()
    print(id(b1))
    print(id(b2))
    print(id(b3))