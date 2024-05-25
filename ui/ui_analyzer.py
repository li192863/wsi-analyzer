# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analyzer.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_Analyzer(object):
    def setupUi(self, Analyzer):
        if not Analyzer.objectName():
            Analyzer.setObjectName(u"Analyzer")
        Analyzer.setWindowModality(Qt.NonModal)
        Analyzer.resize(600, 400)
        Analyzer.setMinimumSize(QSize(0, 299))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        Analyzer.setFont(font)
        icon = QIcon()
        icon.addFile(u"resources/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Analyzer.setWindowIcon(icon)
        Analyzer.setWindowOpacity(1.000000000000000)
        self.action_exit = QAction(Analyzer)
        self.action_exit.setObjectName(u"action_exit")
        self.action_about = QAction(Analyzer)
        self.action_about.setObjectName(u"action_about")
        self.action_open_default_config = QAction(Analyzer)
        self.action_open_default_config.setObjectName(u"action_open_default_config")
        self.action_stop = QAction(Analyzer)
        self.action_stop.setObjectName(u"action_stop")
        self.action_open_running_config = QAction(Analyzer)
        self.action_open_running_config.setObjectName(u"action_open_running_config")
        self.centralwidget = QWidget(Analyzer)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_seg_slice = QHBoxLayout()
        self.layout_seg_slice.setObjectName(u"layout_seg_slice")
        self.layout_seg_slice.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_seg_slice.setContentsMargins(-1, 0, -1, 0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"\u5e7c\u5706"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(0)

        self.layout_seg_slice.addWidget(self.label)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(8)
        self.label_5.setFont(font2)
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.layout_seg_slice.addWidget(self.label_5)

        self.spinBox_seg_slice_down_sample = QSpinBox(self.centralwidget)
        self.spinBox_seg_slice_down_sample.setObjectName(u"spinBox_seg_slice_down_sample")
        self.spinBox_seg_slice_down_sample.setAlignment(Qt.AlignCenter)
        self.spinBox_seg_slice_down_sample.setMinimum(1)
        self.spinBox_seg_slice_down_sample.setMaximum(100)

        self.layout_seg_slice.addWidget(self.spinBox_seg_slice_down_sample)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.layout_seg_slice.addWidget(self.label_6)

        self.spinBox_seg_slice_width = QSpinBox(self.centralwidget)
        self.spinBox_seg_slice_width.setObjectName(u"spinBox_seg_slice_width")
        self.spinBox_seg_slice_width.setAlignment(Qt.AlignCenter)
        self.spinBox_seg_slice_width.setMinimum(1)
        self.spinBox_seg_slice_width.setMaximum(8192)

        self.layout_seg_slice.addWidget(self.spinBox_seg_slice_width)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.layout_seg_slice.addWidget(self.label_7)

        self.spinBox_seg_slice_height = QSpinBox(self.centralwidget)
        self.spinBox_seg_slice_height.setObjectName(u"spinBox_seg_slice_height")
        self.spinBox_seg_slice_height.setAlignment(Qt.AlignCenter)
        self.spinBox_seg_slice_height.setMinimum(1)
        self.spinBox_seg_slice_height.setMaximum(8192)

        self.layout_seg_slice.addWidget(self.spinBox_seg_slice_height)

        self.layout_seg_slice.setStretch(0, 4)
        self.layout_seg_slice.setStretch(1, 1)
        self.layout_seg_slice.setStretch(2, 3)
        self.layout_seg_slice.setStretch(3, 1)
        self.layout_seg_slice.setStretch(4, 3)
        self.layout_seg_slice.setStretch(5, 1)
        self.layout_seg_slice.setStretch(6, 3)

        self.verticalLayout.addLayout(self.layout_seg_slice)

        self.layout_cla_slice = QHBoxLayout()
        self.layout_cla_slice.setObjectName(u"layout_cla_slice")
        self.layout_cla_slice.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_cla_slice.setContentsMargins(-1, 0, -1, 0)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setIndent(0)

        self.layout_cla_slice.addWidget(self.label_2)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font2)
        self.label_8.setLayoutDirection(Qt.LeftToRight)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.layout_cla_slice.addWidget(self.label_8)

        self.spinBox_cla_slice_down_sample = QSpinBox(self.centralwidget)
        self.spinBox_cla_slice_down_sample.setObjectName(u"spinBox_cla_slice_down_sample")
        self.spinBox_cla_slice_down_sample.setAlignment(Qt.AlignCenter)
        self.spinBox_cla_slice_down_sample.setMinimum(1)
        self.spinBox_cla_slice_down_sample.setMaximum(100)

        self.layout_cla_slice.addWidget(self.spinBox_cla_slice_down_sample)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.layout_cla_slice.addWidget(self.label_9)

        self.spinBox_cla_slice_width = QSpinBox(self.centralwidget)
        self.spinBox_cla_slice_width.setObjectName(u"spinBox_cla_slice_width")
        self.spinBox_cla_slice_width.setAlignment(Qt.AlignCenter)
        self.spinBox_cla_slice_width.setMinimum(1)
        self.spinBox_cla_slice_width.setMaximum(8192)

        self.layout_cla_slice.addWidget(self.spinBox_cla_slice_width)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.layout_cla_slice.addWidget(self.label_10)

        self.spinBox_cla_slice_height = QSpinBox(self.centralwidget)
        self.spinBox_cla_slice_height.setObjectName(u"spinBox_cla_slice_height")
        self.spinBox_cla_slice_height.setAlignment(Qt.AlignCenter)
        self.spinBox_cla_slice_height.setMinimum(1)
        self.spinBox_cla_slice_height.setMaximum(8192)

        self.layout_cla_slice.addWidget(self.spinBox_cla_slice_height)

        self.layout_cla_slice.setStretch(0, 4)
        self.layout_cla_slice.setStretch(1, 1)
        self.layout_cla_slice.setStretch(2, 3)
        self.layout_cla_slice.setStretch(3, 1)
        self.layout_cla_slice.setStretch(4, 3)
        self.layout_cla_slice.setStretch(5, 1)
        self.layout_cla_slice.setStretch(6, 3)

        self.verticalLayout.addLayout(self.layout_cla_slice)

        self.layout_runing_set = QHBoxLayout()
        self.layout_runing_set.setObjectName(u"layout_runing_set")
        self.layout_runing_set.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_runing_set.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setIndent(0)

        self.layout_runing_set.addWidget(self.label_3)

        self.checkbox_auto_resume = QCheckBox(self.centralwidget)
        self.checkbox_auto_resume.setObjectName(u"checkbox_auto_resume")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkbox_auto_resume.sizePolicy().hasHeightForWidth())
        self.checkbox_auto_resume.setSizePolicy(sizePolicy1)
        self.checkbox_auto_resume.setFont(font)
        self.checkbox_auto_resume.setChecked(True)

        self.layout_runing_set.addWidget(self.checkbox_auto_resume)

        self.checkbox_force_inference = QCheckBox(self.centralwidget)
        self.checkbox_force_inference.setObjectName(u"checkbox_force_inference")
        sizePolicy1.setHeightForWidth(self.checkbox_force_inference.sizePolicy().hasHeightForWidth())
        self.checkbox_force_inference.setSizePolicy(sizePolicy1)
        self.checkbox_force_inference.setFont(font)

        self.layout_runing_set.addWidget(self.checkbox_force_inference)

        self.checkbox_drop_last = QCheckBox(self.centralwidget)
        self.checkbox_drop_last.setObjectName(u"checkbox_drop_last")
        sizePolicy1.setHeightForWidth(self.checkbox_drop_last.sizePolicy().hasHeightForWidth())
        self.checkbox_drop_last.setSizePolicy(sizePolicy1)
        self.checkbox_drop_last.setFont(font)
        self.checkbox_drop_last.setChecked(False)

        self.layout_runing_set.addWidget(self.checkbox_drop_last)

        self.layout_runing_set.setStretch(0, 3)
        self.layout_runing_set.setStretch(1, 3)
        self.layout_runing_set.setStretch(2, 3)
        self.layout_runing_set.setStretch(3, 3)

        self.verticalLayout.addLayout(self.layout_runing_set)

        self.layout_result_folder = QHBoxLayout()
        self.layout_result_folder.setObjectName(u"layout_result_folder")
        self.layout_result_folder.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_result_folder.setContentsMargins(-1, 0, -1, 0)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setIndent(0)

        self.layout_result_folder.addWidget(self.label_4)

        self.lineEdit_result_folder = QLineEdit(self.centralwidget)
        self.lineEdit_result_folder.setObjectName(u"lineEdit_result_folder")
        self.lineEdit_result_folder.setAlignment(Qt.AlignCenter)

        self.layout_result_folder.addWidget(self.lineEdit_result_folder)

        self.button_choose_result_folder = QPushButton(self.centralwidget)
        self.button_choose_result_folder.setObjectName(u"button_choose_result_folder")
        sizePolicy1.setHeightForWidth(self.button_choose_result_folder.sizePolicy().hasHeightForWidth())
        self.button_choose_result_folder.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(10)
        self.button_choose_result_folder.setFont(font3)

        self.layout_result_folder.addWidget(self.button_choose_result_folder)

        self.layout_result_folder.setStretch(0, 3)
        self.layout_result_folder.setStretch(1, 6)
        self.layout_result_folder.setStretch(2, 3)

        self.verticalLayout.addLayout(self.layout_result_folder)

        self.layout_progress = QHBoxLayout()
        self.layout_progress.setObjectName(u"layout_progress")
        self.layout_progress.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_progress.setContentsMargins(-1, 0, -1, 0)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignCenter)
        self.label_11.setIndent(0)

        self.layout_progress.addWidget(self.label_11)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.layout_progress.addWidget(self.progressBar)

        self.layout_progress.setStretch(0, 3)
        self.layout_progress.setStretch(1, 9)

        self.verticalLayout.addLayout(self.layout_progress)

        self.layout_operation = QHBoxLayout()
        self.layout_operation.setObjectName(u"layout_operation")
        self.layout_operation.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_operation.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_1)

        self.button_choose_file = QPushButton(self.centralwidget)
        self.button_choose_file.setObjectName(u"button_choose_file")
        sizePolicy1.setHeightForWidth(self.button_choose_file.sizePolicy().hasHeightForWidth())
        self.button_choose_file.setSizePolicy(sizePolicy1)
        self.button_choose_file.setFont(font3)

        self.layout_operation.addWidget(self.button_choose_file)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_2)

        self.button_open_result_folder = QPushButton(self.centralwidget)
        self.button_open_result_folder.setObjectName(u"button_open_result_folder")
        sizePolicy1.setHeightForWidth(self.button_open_result_folder.sizePolicy().hasHeightForWidth())
        self.button_open_result_folder.setSizePolicy(sizePolicy1)
        self.button_open_result_folder.setFont(font3)

        self.layout_operation.addWidget(self.button_open_result_folder)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_3)

        self.button_process = QPushButton(self.centralwidget)
        self.button_process.setObjectName(u"button_process")
        sizePolicy1.setHeightForWidth(self.button_process.sizePolicy().hasHeightForWidth())
        self.button_process.setSizePolicy(sizePolicy1)
        self.button_process.setFont(font3)

        self.layout_operation.addWidget(self.button_process)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_4)

        self.layout_operation.setStretch(0, 1)
        self.layout_operation.setStretch(1, 5)
        self.layout_operation.setStretch(2, 1)
        self.layout_operation.setStretch(3, 5)
        self.layout_operation.setStretch(4, 1)
        self.layout_operation.setStretch(5, 5)
        self.layout_operation.setStretch(6, 1)

        self.verticalLayout.addLayout(self.layout_operation)

        Analyzer.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Analyzer)
        self.statusbar.setObjectName(u"statusbar")
        font4 = QFont()
        font4.setFamilies([u"\u4eff\u5b8b"])
        font4.setPointSize(10)
        font4.setBold(True)
        self.statusbar.setFont(font4)
        Analyzer.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Analyzer)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 600, 22))
        self.menu_file = QMenu(self.menuBar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_about = QMenu(self.menuBar)
        self.menu_about.setObjectName(u"menu_about")
        self.menu_edit = QMenu(self.menuBar)
        self.menu_edit.setObjectName(u"menu_edit")
        Analyzer.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu_edit.menuAction())
        self.menuBar.addAction(self.menu_about.menuAction())
        self.menu_file.addAction(self.action_stop)
        self.menu_file.addAction(self.action_exit)
        self.menu_about.addAction(self.action_about)
        self.menu_edit.addAction(self.action_open_running_config)
        self.menu_edit.addAction(self.action_open_default_config)

        self.retranslateUi(Analyzer)

        QMetaObject.connectSlotsByName(Analyzer)
    # setupUi

    def retranslateUi(self, Analyzer):
        Analyzer.setWindowTitle(QCoreApplication.translate("Analyzer", u"\u5207\u7247\u5206\u6790\u5668", None))
        self.action_exit.setText(QCoreApplication.translate("Analyzer", u"\u9000\u51fa\u7a0b\u5e8f", None))
#if QT_CONFIG(statustip)
        self.action_exit.setStatusTip(QCoreApplication.translate("Analyzer", u"\u9000\u51fa\u7a0b\u5e8f", None))
#endif // QT_CONFIG(statustip)
        self.action_about.setText(QCoreApplication.translate("Analyzer", u"\u5173\u4e8e\u8f6f\u4ef6", None))
#if QT_CONFIG(statustip)
        self.action_about.setStatusTip(QCoreApplication.translate("Analyzer", u"\u5173\u4e8e\u8f6f\u4ef6", None))
#endif // QT_CONFIG(statustip)
        self.action_open_default_config.setText(QCoreApplication.translate("Analyzer", u"\u9ed8\u8ba4\u914d\u7f6e", None))
#if QT_CONFIG(statustip)
        self.action_open_default_config.setStatusTip(QCoreApplication.translate("Analyzer", u"\u6253\u5f00\u9ed8\u8ba4\u914d\u7f6e\uff0c\u8f6f\u4ef6\u542f\u52a8\u65f6\u6709\u6548", None))
#endif // QT_CONFIG(statustip)
        self.action_stop.setText(QCoreApplication.translate("Analyzer", u"\u7ec8\u6b62\u5904\u7406", None))
        self.action_stop.setIconText(QCoreApplication.translate("Analyzer", u"\u7ec8\u6b62\u5904\u7406", None))
#if QT_CONFIG(tooltip)
        self.action_stop.setToolTip(QCoreApplication.translate("Analyzer", u"\u7ec8\u6b62\u5904\u7406", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.action_stop.setStatusTip(QCoreApplication.translate("Analyzer", u"\u7ec8\u6b62\u5904\u7406", None))
#endif // QT_CONFIG(statustip)
        self.action_open_running_config.setText(QCoreApplication.translate("Analyzer", u"\u8fd0\u884c\u914d\u7f6e", None))
#if QT_CONFIG(statustip)
        self.action_open_running_config.setStatusTip(QCoreApplication.translate("Analyzer", u"\u6253\u5f00\u8fd0\u884c\u914d\u7f6e\uff0c\u4ec5\u672c\u6b21\u8fd0\u884c\u6709\u6548", None))
#endif // QT_CONFIG(statustip)
        self.label.setText(QCoreApplication.translate("Analyzer", u"\u5206\u5272\u5207\u7247", None))
        self.label_5.setText(QCoreApplication.translate("Analyzer", u"\u964d\u91c7\u6837", None))
#if QT_CONFIG(tooltip)
        self.spinBox_seg_slice_down_sample.setToolTip(QCoreApplication.translate("Analyzer", u"\u964d\u91c7\u6837\u503c", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Analyzer", u"\u5bbd\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.spinBox_seg_slice_width.setToolTip(QCoreApplication.translate("Analyzer", u"\u5207\u7247\u5bbd\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("Analyzer", u"\u9ad8\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.spinBox_seg_slice_height.setToolTip(QCoreApplication.translate("Analyzer", u"\u5207\u7247\u9ad8\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Analyzer", u"\u5206\u7c7b\u5207\u7247", None))
        self.label_8.setText(QCoreApplication.translate("Analyzer", u"\u964d\u91c7\u6837", None))
#if QT_CONFIG(tooltip)
        self.spinBox_cla_slice_down_sample.setToolTip(QCoreApplication.translate("Analyzer", u"\u964d\u91c7\u6837\u503c", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("Analyzer", u"\u5bbd\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.spinBox_cla_slice_width.setToolTip(QCoreApplication.translate("Analyzer", u"\u5207\u7247\u5bbd\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("Analyzer", u"\u9ad8\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.spinBox_cla_slice_height.setToolTip(QCoreApplication.translate("Analyzer", u"\u5207\u7247\u9ad8\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Analyzer", u"\u8fd0\u884c\u9009\u9879", None))
#if QT_CONFIG(tooltip)
        self.checkbox_auto_resume.setToolTip(QCoreApplication.translate("Analyzer", u"\u5c1d\u8bd5\u4ece\u4e0a\u6b21\u8fd0\u884c\u5904\u6062\u590d", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_auto_resume.setText(QCoreApplication.translate("Analyzer", u"\u81ea\u52a8\u6062\u590d", None))
#if QT_CONFIG(tooltip)
        self.checkbox_force_inference.setToolTip(QCoreApplication.translate("Analyzer", u"\u5373\u4f7f\u53ef\u81ea\u52a8\u6062\u590d\u4ecd\u8fdb\u884c\u63a8\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_force_inference.setText(QCoreApplication.translate("Analyzer", u"\u5f3a\u5236\u63a8\u7406", None))
#if QT_CONFIG(tooltip)
        self.checkbox_drop_last.setToolTip(QCoreApplication.translate("Analyzer", u"\u56fe\u7247\u88c1\u5207\u540e\u53bb\u9664\u591a\u4f59\u8fb9\u7f18", None))
#endif // QT_CONFIG(tooltip)
        self.checkbox_drop_last.setText(QCoreApplication.translate("Analyzer", u"\u820d\u5f03\u8fb9\u7f18", None))
        self.label_4.setText(QCoreApplication.translate("Analyzer", u"\u8f93\u51fa\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_result_folder.setToolTip(QCoreApplication.translate("Analyzer", u"\u7ed3\u679c\u6587\u4ef6\u5939\u8def\u5f84\uff0c\u9ed8\u8ba4\u4e3a\u5207\u7247\u6240\u5728\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_result_folder.setText("")
        self.lineEdit_result_folder.setPlaceholderText(QCoreApplication.translate("Analyzer", u"\u81ea\u52a8\u6307\u5b9a", None))
#if QT_CONFIG(tooltip)
        self.button_choose_result_folder.setToolTip(QCoreApplication.translate("Analyzer", u"\u9009\u62e9\u7ed3\u679c\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.button_choose_result_folder.setText(QCoreApplication.translate("Analyzer", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.label_11.setText(QCoreApplication.translate("Analyzer", u"\u8fd0\u884c\u8fdb\u5ea6", None))
        self.progressBar.setFormat(QCoreApplication.translate("Analyzer", u"%p%", None))
#if QT_CONFIG(tooltip)
        self.button_choose_file.setToolTip(QCoreApplication.translate("Analyzer", u"\u9009\u62e9\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.button_choose_file.setText(QCoreApplication.translate("Analyzer", u"\u9009\u62e9\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.button_open_result_folder.setToolTip(QCoreApplication.translate("Analyzer", u"\u6253\u5f00\u7ed3\u679c", None))
#endif // QT_CONFIG(tooltip)
        self.button_open_result_folder.setText(QCoreApplication.translate("Analyzer", u"\u6253\u5f00\u7ed3\u679c", None))
#if QT_CONFIG(tooltip)
        self.button_process.setToolTip(QCoreApplication.translate("Analyzer", u"\u5f00\u59cb\u5904\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.button_process.setText(QCoreApplication.translate("Analyzer", u"\u5f00\u59cb\u5904\u7406", None))
        self.menu_file.setTitle(QCoreApplication.translate("Analyzer", u"\u6587\u4ef6", None))
        self.menu_about.setTitle(QCoreApplication.translate("Analyzer", u"\u5173\u4e8e", None))
        self.menu_edit.setTitle(QCoreApplication.translate("Analyzer", u"\u7f16\u8f91", None))
    # retranslateUi

