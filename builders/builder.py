import logging
import pickle
from abc import ABC

from utils import read_config


class Builder(ABC):
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = read_config(self.config_file)
        self.logger = logging.getLogger(name='file-logger')

    def build_from_dict(self, object_cls, params_dict):
        """
        从字典中构造对象
        :param object_cls: 对象的类
        :param params_dict: 参数字典
        :return:
        """
        return object_cls(**params_dict)

    def build_from_file(self, object_file):
        """
        从文件中构造对象
        :param object_file: 存储对象的文件
        :return:
        """
        with open(object_file, 'rb') as f:
            return pickle.load(f)

if __name__ == '__main__':
    b = Builder('../conf/settings.yml')
    print(b.config)
