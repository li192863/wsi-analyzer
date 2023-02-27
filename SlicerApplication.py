import sys
from threading import Thread

import yaml
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog

from ImageSlicer import ImageSlicer


class SlicerApplication():
    def __init__(self):
        super(SlicerApplication, self).__init__()
        self.file_names = []  # 已选择的文件
        self.default_config = self.read_config()  # 定义配置
        self.slicer = ImageSlicer([self.default_config['image_height'], self.default_config['image_width']])  # 图片切片器

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
        self.ui = QUiLoader().load('resources/slicer.ui')  # 加载ui
        self.ui.spinbox_image_height.setValue(self.default_config['image_height'])  # 切片高
        self.ui.spinbox_image_width.setValue(self.default_config['image_width'])  # 切片宽
        self.ui.checkbox_drop_last.setChecked(self.default_config['drop_last'])  # 舍弃边缘
        self.ui.checkbox_enable_filter.setChecked(self.default_config['enable_filter'])  # 是否过滤
        self.ui.spinbox_threshold.setValue(self.default_config['threshold'])  # 颜色阈值
        self.ui.lineedit_file_format.setText(self.default_config['file_format'])  # 文件格式
        self.ui.lineEdit_target_dir.setText(self.default_config['target_dir'])  # 输出文件夹

        # 是否过滤
        self.ui.checkbox_enable_filter.clicked.connect(self.handle_checkbox_enable_filter_clicked)
        # 颜色阈值
        self.ui.spinbox_threshold.setEnabled(self.ui.checkbox_enable_filter.isChecked())  # 启用过滤时可点击
        # 输出地址
        self.ui.button_choose_target_dir.clicked.connect(self.handle_button_choose_target_dir_clicked)
        # 按钮区域
        self.ui.button_convert.clicked.connect(self.handle_button_convert_clicked)
        self.ui.button_choose_file.clicked.connect(self.handle_button_choose_file_clicked)

        self.ui.button_choose_file.setFocus()  # 设置焦点
        self.ui.button_convert.setEnabled(len(self.file_names) != 0)  # 选择文件不为0时可点击

        # 状态栏
        self.ui.statusbar.showMessage('请选择一个或多个切片文件')

    def handle_checkbox_enable_filter_clicked(self):
        """ 是否过滤被点击时触发方差阈值变化 """
        self.ui.spinbox_threshold.setEnabled(self.ui.checkbox_enable_filter.isChecked())

    def handle_button_choose_file_clicked(self):
        """ 选择文件被点击时触发 """
        self.file_names, _ = QFileDialog.getOpenFileNames(caption='选择一个或多个病理切片文件', filter='病理切片(*.svs)')
        self.ui.button_convert.setEnabled(len(self.file_names) != 0)

        # 状态栏
        self.ui.statusbar.showMessage(f'已选择{len(self.file_names)}个文件，请点击开始转换生成切片'
                                      if len(self.file_names) != 0 else
                                      '请选择一个或多个切片文件')

    def handle_button_choose_target_dir_clicked(self):
        """ 选择输出文件夹 """
        self.slicer.target_dir = QFileDialog.getExistingDirectory(caption='选择输出文件夹地址')
        self.ui.lineEdit_target_dir.setText(self.slicer.target_dir)


    def handle_button_convert_clicked(self):
        """ 点击开始转换时触发 """
        self.ui.statusbar.showMessage('正在转换，请稍后...')
        self.ui.button_choose_file.setEnabled(False)
        self.ui.button_convert.setEnabled(False)
        thread = Thread(target=self.convert)
        thread.start()

    def convert(self):
        """ 转换文件 """
        self.slicer.slice_size = [self.ui.spinbox_image_height.value(), self.ui.spinbox_image_width.value()]
        self.slicer.drop_last = self.ui.checkbox_drop_last.isChecked()
        self.slicer.enable_filter = self.ui.checkbox_enable_filter.isChecked()
        self.slicer.threshold = self.ui.spinbox_threshold.value()
        self.slicer.target_dir = self.ui.lineEdit_target_dir.text().strip()  # 去除无效空格
        self.slicer.suffix = self.ui.lineedit_file_format.text().strip()  # 去除无效空格

        try:
            self.slicer.generate_slices(self.file_names)  # 开始转换
            self.ui.statusbar.showMessage('转换完成！请打开切片所在文件夹或指定文件夹查看切片文件')  # 状态栏
        except Exception as e:
            self.ui.statusbar.showMessage(f'转换失败！错误信息: {str(e)}')  # 状态栏
        self.ui.button_choose_file.setEnabled(True)
        QApplication.beep()  # 提示音
        QApplication.alert(self.ui)  # 任务栏闪烁提醒



if __name__ == '__main__':
    app = QApplication(sys.argv)
    slicer = SlicerApplication()
    slicer.ui.show()
    app.exec()
