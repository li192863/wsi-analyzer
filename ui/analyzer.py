from PySide6 import QtWidgets
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog

from ui.ui_analyzer import Ui_Analyzer
from ui.threads import ProcessThread
from utils import read_config


class Analyzer(QtWidgets.QMainWindow):
    def __init__(self):
        super(Analyzer, self).__init__()
        self.ui = Ui_Analyzer()
        self.ui.setupUi(self)
        # 初始化
        self.read_config()
        self.init_ui()
        self.bind_events()

    def read_config(self):
        """
        读取默认配置
        :return:
        """
        # 读取默认配置
        self.default_config_file = './conf/settings.yml'
        self.config = read_config(self.default_config_file)

    def init_ui(self):
        """
        初始化界面
        :return: 无
        """
        # 分割切片
        self.ui.spinBox_seg_slice_width.setValue(self.config.slicer.segmentation.slice_size[0])
        self.ui.spinBox_seg_slice_height.setValue(self.config.slicer.segmentation.slice_size[1])
        self.ui.spinBox_seg_slice_down_sample.setValue(self.config.slicer.segmentation.down_sample)
        # 分类切片
        self.ui.spinBox_cla_slice_width.setValue(self.config.slicer.classification.slice_size[0])
        self.ui.spinBox_cla_slice_height.setValue(self.config.slicer.classification.slice_size[1])
        self.ui.spinBox_cla_slice_down_sample.setValue(self.config.slicer.classification.down_sample)
        # 运行选项
        self.ui.checkbox_auto_resume.setChecked(self.config.basic.auto_resume)
        self.ui.checkbox_force_inference.setChecked(self.config.basic.force_inference)
        self.ui.checkbox_drop_last.setChecked(self.config.slicer.drop_last)
        # 输出地址
        self.ui.lineEdit_result_folder.setText(self.config.basic.result_folder)

    def bind_events(self):
        """
        绑定事件
        :return:
        """
        self.ui.button_choose_result_folder.clicked.connect(self.on_button_choose_result_folder_clicked)
        self.ui.button_choose_file.clicked.connect(self.on_button_choose_file_clicked)
        self.ui.button_open_config.clicked.connect(self.on_button_open_config_clicked)
        self.ui.button_process.clicked.connect(self.on_button_process_clicked)

    def read_ui_config(self):
        """
        读取界面配置
        :return:
        """
        # 读取配置
        self.config.slicer.segmentation.down_sample = self.ui.spinBox_seg_slice_down_sample.value()
        self.config.slicer.segmentation.slice_size = [
            self.ui.spinBox_seg_slice_width.value(),
            self.ui.spinBox_seg_slice_height.value()
        ]
        self.config.slicer.classification.down_sample = self.ui.spinBox_cla_slice_down_sample.value()
        self.config.slicer.classification.slice_size = [
            self.ui.spinBox_cla_slice_width.value(),
            self.ui.spinBox_cla_slice_height.value()
        ]
        self.config.basic.auto_resume = self.ui.checkbox_auto_resume.isChecked()
        self.config.basic.force_inference = self.ui.checkbox_force_inference.isChecked()
        self.config.basic.slicer.drop_last = self.ui.checkbox_drop_last.isChecked()
        self.config.basic.result_folder = self.ui.lineEdit_result_folder.text()

    def on_button_choose_result_folder_clicked(self):
        """ 选择文件夹被点击时触发 """
        self.ui.statusbar.showMessage('请选择输出文件夹地址')
        self.config.basic.result_folder = QFileDialog.getExistingDirectory(caption='请选择输出文件夹地址')
        self.ui.lineEdit_result_folder.setText(self.config.basic.result_folder)

    def on_button_choose_file_clicked(self):
        """ 选择文件被点击时触发 """
        self.ui.statusbar.showMessage('请选择一个或多个病理切片文件')
        self.config.basic.filelist, _ = QFileDialog.getOpenFileNames(
            caption='请选择一个或多个病理切片文件',
            filter='病理切片(*.svs *.jpg *.jpeg *.png *.tiff *.tif)'
        )

    def on_button_open_config_clicked(self):
        """ 打开配置被点击 """
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.default_config_file))
        self.ui.statusbar.showMessage('请重启应用以生效配置！')

    def on_button_process_clicked(self):
        """ 开始处理被点击时触发 """
        self.read_ui_config()
        self.process_thread: ProcessThread = ProcessThread(self.config)
        self.process_thread.process_complete_signal.connect(self.on_process_complete_signal)
        self.process_thread.process_failed_signal.connect(self.on_process_failed_signal)
        self.process_thread.start()
        self.ui.statusbar.showMessage('正在开始转换...')

    @Slot(str)
    def on_process_complete_signal(self, value):
        """ 处理完成时触发事件 """
        self.ui.statusbar.showMessage(value)
        self.config.basic.filelist = []

    @Slot(str)
    def on_process_failed_signal(self, value):
        """ 处理识别时触发事件"""
        self.ui.statusbar.showMessage(value)
