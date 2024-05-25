from PySide6.QtWidgets import QDialog

from ui.ui_about import Ui_About


class AboutDialog(QDialog, Ui_About):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)