import os
import threading

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QDesktopServices, QPalette
from PySide6.QtWidgets import QFileDialog, QApplication, QLabel

from binders import StatusbarBinder, ProgressbarBinder
from ui.about_dialog import AboutDialog
from ui.ui_analyzer import Ui_Analyzer
from ui.threads import ProcessThread
from utils import read_config, write_config


class AnalyzerWindow(QtWidgets.QMainWindow):
    def __init__(self, default_config_file = './conf/settings.yml', running_confile_file = './conf/running_set.yml'):
        super(AnalyzerWindow, self).__init__()
        # 配置
        self.default_config_file = default_config_file
        self.running_confile_file = running_confile_file
        # 界面
        self.ui = Ui_Analyzer()
        self.ui.setupUi(self)
        # 初始化
        self.read_binders()  # 初始化绑定器
        self.read_config()  # 读取默认配置
        self.write_config()  # 写入运行配置
        self.init_ui()  # 初始化应用界面
        self.bind_events()  # 绑定应用事件

    def read_binders(self):
        """
        读取绑定器
        :return: 无
        """
        self.status_binder = StatusbarBinder(self.ui.statusbar)
        self.status_binder.emitter.status_message_signal.connect(self.on_status_message_signal)
        self.progress_binder = ProgressbarBinder(self.ui.progressBar)
        self.progress_binder.emitter.progress_update_signal.connect(self.on_progress_update_signal)

    def read_config(self, file=None):
        """
        读取默认配置
        :param file: 要读取的文件
        :return: 无
        """
        file = file or self.default_config_file
        # 读取默认配置
        self.config = read_config(file)

    def write_config(self, file=None):
        """
        写入运行配置
        :param file: 要写入的文件
        :return: 无
        """
        file = file or self.running_confile_file
        # 写入运行配置
        write_config(self.config, file)

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
        # 切片文件
        self.filelist = []
        self.result_folder = None
        # 设置焦点
        self.ui.button_choose_file.setFocus()

    def bind_events(self):
        """
        绑定事件
        :return:
        """
        # 菜单栏
        self.ui.action_stop.triggered.connect(self.on_action_stop)
        self.ui.action_exit.triggered.connect(self.on_action_exit)
        self.ui.action_open_running_config.triggered.connect(self.on_action_open_running_config)
        self.ui.action_open_default_config.triggered.connect(self.on_action_open_default_config)
        self.ui.action_about.triggered.connect(self.on_action_about)
        # 按钮
        self.ui.button_choose_result_folder.clicked.connect(self.on_button_choose_result_folder_clicked)
        self.ui.button_choose_file.clicked.connect(self.on_button_choose_file_clicked)
        self.ui.button_open_result_folder.clicked.connect(self.on_button_open_result_folder_clicked)
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
        self.config.basic.filelist = self.filelist

    def _change_window(self, enabled):
        """
        冻结/解冻按钮，避免用户触发其他操作
        :param enabled: 启用或不启用
        :return: 无
        """
        # 编辑菜单
        self.ui.action_open_running_config.setEnabled(enabled)
        self.ui.action_open_default_config.setEnabled(enabled)
        # 输出地址
        self.ui.lineEdit_result_folder.setEnabled(enabled)
        self.ui.button_choose_result_folder.setEnabled(enabled)
        # 按钮区域
        self.ui.button_choose_file.setEnabled(enabled)
        self.ui.button_open_result_folder.setEnabled(enabled)
        self.ui.button_process.setEnabled(enabled)

    def on_action_stop(self):
        """ 中断处理 """
        if hasattr(self, 'process_thread') and self.process_thread is not None and self.process_thread.is_alive():
            # 终止线程
            self.status_binder.warning('正在尝试终止...')
            threading.Thread(target=self.process_thread.stop).start()
        else:
            self.status_binder.warning('未在处理中！')
            # 设置焦点
            self.ui.button_choose_file.setFocus()

    def on_action_exit(self):
        """ 退出程序 """
        QApplication.quit()

    def on_action_open_running_config(self):
        """ 打开运行配置 """
        # 打开配置文件
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.running_confile_file))
        # 显示警告信息
        self.status_binder.warning('请注意界面配置优于运行配置！')

    def on_action_open_default_config(self):
        """ 打开默认配置 """
        # 打开配置文件
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.default_config_file))
        # 显示警告信息
        self.status_binder.warning('请注意重启应用才可生效配置！')

    def on_action_about(self):
        """ 关于软件 """
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def on_button_choose_result_folder_clicked(self):
        """ 选择文件夹被点击时触发 """
        self.status_binder.info('请选择输出文件夹地址')
        self.config.basic.result_folder = QFileDialog.getExistingDirectory(
            caption='请选择输出文件夹地址'
        )
        self.ui.lineEdit_result_folder.setText(self.config.basic.result_folder)
        # 设置焦点
        self.ui.button_choose_file.setFocus()

    def on_button_choose_file_clicked(self):
        """ 选择文件被点击时触发 """
        self.status_binder.info('请选择一个或多个病理切片文件')
        self.filelist, _ = QFileDialog.getOpenFileNames(
            caption='请选择一个或多个病理切片文件',
            filter='病理切片(*.svs *.tif *.tiff *.mrxs *.jpg *.jpeg *.png *webp)'
        )
        self.status_binder.info(f'已选择{len(self.filelist)}个病理切片文件')
        # 设置焦点
        self.ui.button_process.setFocus()

    def on_button_open_result_folder_clicked(self):
        """ 打开结果被点击 """
        # 确定打开文件夹
        if self.result_folder is None or self.result_folder == '':
            self.status_binder.warning('请选择文件进行处理！')
            # 设置焦点
            self.ui.button_choose_file.setFocus()
            return
        # 打开配置文件
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.result_folder))
        # 设置焦点
        self.ui.button_choose_file.setFocus()

    def on_button_process_clicked(self):
        """ 开始处理被点击时触发 """
        # 读取运行配置
        self.read_config(self.running_confile_file)
        # 读取界面配置
        self.read_ui_config()
        # 冻结应用按钮
        self._change_window(False)
        # 启动处理线程
        self.process_thread: ProcessThread = ProcessThread(self.config, self.running_confile_file)
        self.process_thread.emitter.process_complete_signal.connect(self.on_process_complete_signal)
        self.process_thread.emitter.process_failed_signal.connect(self.on_process_failed_signal)
        self.process_thread.emitter.process_stop_signal.connect(self.on_process_stop_signal)
        self.process_thread.start()

    def _get_result_folder(self):
        """ 获取结果文件夹 """
        self.read_ui_config()
        result_folder = self.config.basic.result_folder
        if result_folder == '':
            if self.filelist is None or len(self.filelist) == 0:
                return None
            result_folder, _ = os.path.split(self.filelist[0])
        return result_folder

    @Slot(str)
    def on_process_complete_signal(self, value):
        """ 处理完成时触发事件 """
        self._change_window(True)
        self.status_binder.success(value)
        self.result_folder = self._get_result_folder()
        self.filelist = []
        # 设置焦点
        self.ui.button_open_result_folder.setFocus()
        # 设置提示
        QApplication.beep()  # 提示音
        QApplication.alert(self)  # 任务栏闪烁提醒

    @Slot(str)
    def on_process_failed_signal(self, value):
        """ 处理识别时触发事件 """
        self._change_window(True)
        self.status_binder.error(value)
        self.result_folder = self._get_result_folder()
        self.progress_binder.set(0)
        # 设置焦点
        self.ui.button_open_result_folder.setFocus()
        # 设置提示
        QApplication.beep()  # 提示音
        QApplication.alert(self)  # 任务栏闪烁提醒

    @Slot(str)
    def on_process_stop_signal(self, value):
        """ 处理终止时触发事件 """
        self._change_window(True)
        self.status_binder.error(value)
        self.result_folder = self._get_result_folder()
        self.progress_binder.set(0)
        # 设置焦点
        self.ui.button_open_result_folder.setFocus()
        # 设置提示
        QApplication.beep()  # 提示音
        QApplication.alert(self)  # 任务栏闪烁提醒

    @Slot(str, QPalette)
    def on_status_message_signal(self, message, palette):
        """ 状态栏变化时触发事件 """
        # 设置颜色
        if self.ui.statusbar.palette() != palette:
            self.ui.statusbar.setPalette(palette)
        # 显示消息
        self.ui.statusbar.showMessage(message)

    @Slot(float)
    def on_progress_update_signal(self, value):
        """ 进度条更新是触发事件 """
        self.ui.progressBar.setValue(value)