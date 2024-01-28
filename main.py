import faulthandler
import sys

from PySide6.QtWidgets import QApplication

from ui import AnalyzerWindow
from utils import init_file_logger


def main():
    """
    主函数
    :return:
    """
    # error
    sys.stderr = open('./logs/error.txt', 'w')
    faulthandler.enable()
    # logger
    init_file_logger()
    # Application
    app = QApplication(sys.argv)
    analyzer = AnalyzerWindow()
    # Run
    analyzer.show()
    app.exec()


if __name__ == '__main__':
    main()