import sys

from PySide6.QtWidgets import QApplication

from ui import Analyzer
from utils import init_file_logger


def main():
    """
    主函数
    :return:
    """
    # logger
    init_file_logger()
    # Application
    app = QApplication(sys.argv)
    analyzer = Analyzer()
    # Run
    analyzer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()