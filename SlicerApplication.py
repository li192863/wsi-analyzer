import sys
from threading import Thread

import yaml
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog

from ImageSlicer import ImageSlicer
from MainWindow import Ui_Slicer


class SlicerApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super(SlicerApplication, self).__init__()
        self.ui = Ui_Slicer()
        self.ui.setupUi(self)
        self.file_name = ''  # 已选择的文件
        self.default_config = self.read_config()  # 定义配置
        self.slicer = ImageSlicer([self.default_config['image_height'], self.default_config['image_width']],
                                  drop_last=self.default_config['drop_last'],
                                  enable_filter=self.default_config['enable_filter'],
                                  threshold=self.default_config['threshold'],
                                  down_sample=self.default_config['down_sample'],
                                  target_dir=self.default_config['target_dir'],
                                  suffix=self.default_config['file_format'])  # 图片切片器
        self.analyze_thread = None
        self.convert_thread = None
        self.init_ui()  # 加载配置

    def read_config(self):
        """ 读取配置文件 """
        f = open('resources/settings.yml', 'r', encoding="utf-8")
        config = yaml.load(f, Loader=yaml.FullLoader)  # Loader为了更加安全
        f.close()
        return config

    def init_ui(self):
        """ 初始化界面 """
        # 加载配置
        self.ui.spinbox_image_height.setValue(self.default_config['image_height'])  # 切片高
        self.ui.spinbox_image_width.setValue(self.default_config['image_width'])  # 切片宽
        self.ui.checkbox_drop_last.setChecked(self.default_config['drop_last'])  # 舍弃边缘
        self.ui.checkbox_enable_filter.setChecked(self.default_config['enable_filter'])  # 是否过滤
        self.ui.doubleSpinBox_down_sample.setValue(self.default_config['down_sample'])  # 降采样值
        self.ui.spinbox_threshold.setValue(self.default_config['threshold'])  # 颜色阈值
        self.ui.lineEdit_file_format.setText(self.default_config['file_format'])  # 文件格式
        self.ui.lineEdit_target_dir.setText(self.default_config['target_dir'])  # 输出文件夹

        # 切片大小
        self.ui.spinbox_image_height.valueChanged.connect(self.handle_spinbox_image_height_value_changed)
        self.ui.spinbox_image_width.valueChanged.connect(self.handle_spinbox_image_width_value_changed)
        # 舍弃边缘
        self.ui.checkbox_drop_last.stateChanged.connect(self.handle_checkbox_drop_last_state_changed)
        # 是否过滤
        self.ui.checkbox_enable_filter.clicked.connect(self.handle_checkbox_enable_filter_clicked)
        # 白色阈值
        self.ui.spinbox_threshold.valueChanged.connect(self.handle_spinbox_threshold_value_changed)
        self.ui.spinbox_threshold.setEnabled(self.ui.checkbox_enable_filter.isChecked())  # 启用过滤时可点击
        # 降采样值
        self.ui.doubleSpinBox_down_sample.valueChanged.connect(self.handle_double_spinbox_down_sample_value_changed)
        # 文件格式
        self.ui.lineEdit_file_format.textChanged.connect(self.handle_line_edit_file_format_text_changed)
        # 输出地址
        self.ui.button_choose_target_dir.clicked.connect(self.handle_button_choose_target_dir_clicked)
        # 按钮区域
        self.ui.button_convert.clicked.connect(self.handle_button_convert_clicked)
        self.ui.button_choose_file.clicked.connect(self.handle_button_choose_file_clicked)

        self.ui.button_choose_file.setFocus()  # 设置焦点
        self.ui.button_convert.setEnabled(self.file_name != '')  # 选择文件不为0时可点击

        # 状态栏
        self.ui.statusbar.showMessage('请选择一个病理切片文件，格式不限')

    def handle_spinbox_image_height_value_changed(self):
        """ 图片高度数值变化时触发 """
        self.slicer.slice_size[0] = self.ui.spinbox_image_height.value()
        # 关联事件
        self.analyze_file()

    def handle_spinbox_image_width_value_changed(self):
        """ 图片高度数值变化时触发 """
        self.slicer.slice_size[1] = self.ui.spinbox_image_width.value()
        # 关联事件
        self.analyze_file()

    def handle_checkbox_drop_last_state_changed(self):
        """ 舍弃边缘改变时触发 """
        self.slicer.drop_last = self.ui.checkbox_drop_last.isChecked()
        # 关联事件
        self.analyze_file()

    def handle_checkbox_enable_filter_clicked(self):
        """ 是否过滤被点击时触发方差阈值变化 """
        self.slicer.enable_filter = self.ui.checkbox_enable_filter.isChecked()
        # 关联控价
        self.ui.spinbox_threshold.setEnabled(self.ui.checkbox_enable_filter.isChecked())

    def handle_spinbox_threshold_value_changed(self):
        """ 空白阈值数值变化时触发 """
        self.slicer.threshold = self.ui.spinbox_threshold.value()
        # 关联事件
        self.analyze_file()

    def handle_double_spinbox_down_sample_value_changed(self):
        """ 降采样数值变化时触发 """
        self.slicer.down_sample = self.ui.doubleSpinBox_down_sample.value()
        # 关联事件
        self.analyze_file()

    def handle_line_edit_file_format_text_changed(self):
        """ 文件格式改变时触发 """
        self.slicer.suffix = self.ui.lineEdit_file_format.text()

    def handle_button_choose_target_dir_clicked(self):
        """ 选择输出文件夹 """
        self.slicer.target_dir = QFileDialog.getExistingDirectory(caption='选择输出文件夹地址')
        # 关联控价
        self.ui.lineEdit_target_dir.setText(self.slicer.target_dir)

    def handle_button_choose_file_clicked(self):
        """ 选择文件被点击时触发 """
        file_name, _ = QFileDialog.getOpenFileName(caption='请选择一个病理切片文件，格式不限', filter='病理切片(*.svs *.jpg *.jpeg *.png *.tiff *.tif)')
        self.file_name = file_name
        self.slicer.set_file(file_name)
        if self.file_name == '':
            return
        # 关联控价
        self.ui.button_convert.setEnabled(True)
        # 关联事件
        self.analyze_file()

    def handle_button_convert_clicked(self):
        """ 点击开始转换时触发 """
        # 关联控价
        self.ui.statusbar.showMessage('正在转换，请稍后...')
        self.freeze_window()
        # 转换文件
        # 注意，此处需将convert_thread声明为实例变量，若为局部变量，函数执行完立即释放，而del函数使主线程卡死
        self.convert_thread = ConvertThread(self.slicer)
        self.convert_thread.convert_signal.connect(self.event_convert_completed)
        self.convert_thread.start()

    def event_convert_completed(self, message):
        """ 转换文件完成响应 """
        self.ui.statusbar.showMessage(message)
        self.file_name = ''
        self.restore_window()
        QApplication.beep()  # 提示音
        QApplication.alert(self)  # 任务栏闪烁提醒

    def event_analyze_completed(self, message):
        """ 获取文件信息完成响应 """
        self.ui.statusbar.showMessage(message)

    def analyze_file(self):
        """ 获取文件信息 """
        if self.file_name == '':
            return
        if self.analyze_thread is not None and self.analyze_thread.isRunning():
            self.analyze_thread.requestInterruption()
            self.analyze_thread.wait()
        self.analyze_thread = AnalyzeThread(self.slicer)
        self.analyze_thread.analyze_signal.connect(self.event_analyze_completed)
        self.analyze_thread.start()

    def freeze_window(self):
        """ 冻结窗口 """
        self.ui.spinbox_image_height.setEnabled(False)
        self.ui.spinbox_image_width.setEnabled(False)
        self.ui.checkbox_drop_last.setEnabled(False)
        self.ui.checkbox_enable_filter.setEnabled(False)
        self.ui.spinbox_threshold.setEnabled(False)
        self.ui.doubleSpinBox_down_sample.setEnabled(False)
        self.ui.lineEdit_file_format.setEnabled(False)
        self.ui.lineEdit_target_dir.setEnabled(False)
        self.ui.button_choose_target_dir.setEnabled(False)
        self.ui.button_choose_file.setEnabled(False)
        self.ui.button_convert.setEnabled(False)

    def restore_window(self):
        """ 恢复窗口 """
        self.ui.spinbox_image_height.setEnabled(True)
        self.ui.spinbox_image_width.setEnabled(True)
        self.ui.checkbox_drop_last.setEnabled(True)
        self.ui.checkbox_enable_filter.setEnabled(True)
        self.ui.spinbox_threshold.setEnabled(self.ui.checkbox_enable_filter.isChecked())
        self.ui.doubleSpinBox_down_sample.setEnabled(True)
        self.ui.lineEdit_file_format.setEnabled(True)
        self.ui.lineEdit_target_dir.setEnabled(True)
        self.ui.button_choose_target_dir.setEnabled(True)
        self.ui.button_choose_file.setEnabled(True)
        self.ui.button_convert.setEnabled(False)


class ConvertThread(QThread):
    """ 转换线程 """
    convert_signal = Signal(str)
    def __init__(self, slicer):
        super(ConvertThread, self).__init__()
        self.slicer = slicer

    def run(self) -> None:
        try:
            self.slicer.generate_slices()
            self.convert_signal.emit('转换完成！请打开切片所在文件夹或指定文件夹查看切片文件')
        except Exception as e:
            self.convert_signal.emit(f'转换失败！错误信息: {str(e)}')

class AnalyzeThread(QThread):
    """ 分析线程 """
    analyze_signal = Signal(str)
    def __init__(self, slicer):
        super(AnalyzeThread, self).__init__()
        self.slicer = slicer

    def run(self) -> None:
        try:
            info = self.slicer.analyze_slices()
            self.analyze_signal.emit(info)
        except Exception as e:
            self.analyze_signal.emit(f'获取失败！错误信息: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    slicer = SlicerApplication()
    slicer.show()
    app.exec()
