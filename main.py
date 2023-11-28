import faulthandler
import sys

from PySide2.QtWidgets import QApplication

from ui import Analyzer
from utils import init_file_logger


def main():
    """
    主函数
    :return:
    """
    faulthandler.enable()
    # logger
    init_file_logger()
    # Application
    app = QApplication(sys.argv)
    analyzer = Analyzer()
    # Run
    analyzer.show()
    app.exec_()


if __name__ == '__main__':
    main()