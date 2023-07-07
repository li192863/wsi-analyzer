# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'slicer.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_Slicer(object):
    def setupUi(self, Slicer):
        if not Slicer.objectName():
            Slicer.setObjectName(u"Slicer")
        Slicer.setWindowModality(Qt.NonModal)
        Slicer.resize(475, 300)
        Slicer.setMinimumSize(QSize(0, 299))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        Slicer.setFont(font)
        icon = QIcon()
        icon.addFile(u"resources/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Slicer.setWindowIcon(icon)
        self.action_choose_file = QAction(Slicer)
        self.action_choose_file.setObjectName(u"action_choose_file")
        self.action_choose_file.setCheckable(False)
        self.action_choose_file.setEnabled(True)
        self.action_choose_file.setFont(font)
        self.action_convert = QAction(Slicer)
        self.action_convert.setObjectName(u"action_convert")
        self.action_help = QAction(Slicer)
        self.action_help.setObjectName(u"action_help")
        self.action_about = QAction(Slicer)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(Slicer)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_config_slice_size = QHBoxLayout()
        self.layout_config_slice_size.setObjectName(u"layout_config_slice_size")
        self.layout_config_slice_size.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_slice_size.setContentsMargins(-1, 0, -1, 0)
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

        self.layout_config_slice_size.addWidget(self.label)

        self.spinbox_image_height = QSpinBox(self.centralwidget)
        self.spinbox_image_height.setObjectName(u"spinbox_image_height")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinbox_image_height.sizePolicy().hasHeightForWidth())
        self.spinbox_image_height.setSizePolicy(sizePolicy1)
        self.spinbox_image_height.setAlignment(Qt.AlignCenter)
        self.spinbox_image_height.setMinimum(1)
        self.spinbox_image_height.setMaximum(65536)

        self.layout_config_slice_size.addWidget(self.spinbox_image_height)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setBold(True)
        self.label_2.setFont(font2)
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setIndent(0)

        self.layout_config_slice_size.addWidget(self.label_2)

        self.spinbox_image_width = QSpinBox(self.centralwidget)
        self.spinbox_image_width.setObjectName(u"spinbox_image_width")
        sizePolicy1.setHeightForWidth(self.spinbox_image_width.sizePolicy().hasHeightForWidth())
        self.spinbox_image_width.setSizePolicy(sizePolicy1)
        self.spinbox_image_width.setAlignment(Qt.AlignCenter)
        self.spinbox_image_width.setMinimum(1)
        self.spinbox_image_width.setMaximum(65536)

        self.layout_config_slice_size.addWidget(self.spinbox_image_width)

        self.layout_config_slice_size.setStretch(0, 3)
        self.layout_config_slice_size.setStretch(1, 3)
        self.layout_config_slice_size.setStretch(2, 1)
        self.layout_config_slice_size.setStretch(3, 3)

        self.verticalLayout.addLayout(self.layout_config_slice_size)

        self.layout_drop_last = QHBoxLayout()
        self.layout_drop_last.setObjectName(u"layout_drop_last")
        self.layout_drop_last.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_drop_last.setContentsMargins(-1, 0, -1, 0)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setIndent(0)

        self.layout_drop_last.addWidget(self.label_6)

        self.checkbox_drop_last = QCheckBox(self.centralwidget)
        self.checkbox_drop_last.setObjectName(u"checkbox_drop_last")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkbox_drop_last.sizePolicy().hasHeightForWidth())
        self.checkbox_drop_last.setSizePolicy(sizePolicy3)
        self.checkbox_drop_last.setFont(font)

        self.layout_drop_last.addWidget(self.checkbox_drop_last)

        self.layout_drop_last.setStretch(0, 3)
        self.layout_drop_last.setStretch(1, 7)

        self.verticalLayout.addLayout(self.layout_drop_last)

        self.layout_config_filter = QHBoxLayout()
        self.layout_config_filter.setObjectName(u"layout_config_filter")
        self.layout_config_filter.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_filter.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setIndent(0)

        self.layout_config_filter.addWidget(self.label_3)

        self.checkbox_enable_filter = QCheckBox(self.centralwidget)
        self.checkbox_enable_filter.setObjectName(u"checkbox_enable_filter")
        sizePolicy3.setHeightForWidth(self.checkbox_enable_filter.sizePolicy().hasHeightForWidth())
        self.checkbox_enable_filter.setSizePolicy(sizePolicy3)
        self.checkbox_enable_filter.setFont(font)

        self.layout_config_filter.addWidget(self.checkbox_enable_filter)

        self.layout_config_filter.setStretch(0, 3)
        self.layout_config_filter.setStretch(1, 7)

        self.verticalLayout.addLayout(self.layout_config_filter)

        self.layout_config_threshold = QHBoxLayout()
        self.layout_config_threshold.setObjectName(u"layout_config_threshold")
        self.layout_config_threshold.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_threshold.setContentsMargins(-1, 0, -1, 0)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setIndent(0)

        self.layout_config_threshold.addWidget(self.label_4)

        self.spinbox_threshold = QSpinBox(self.centralwidget)
        self.spinbox_threshold.setObjectName(u"spinbox_threshold")
        sizePolicy3.setHeightForWidth(self.spinbox_threshold.sizePolicy().hasHeightForWidth())
        self.spinbox_threshold.setSizePolicy(sizePolicy3)
        self.spinbox_threshold.setFont(font)
        self.spinbox_threshold.setAlignment(Qt.AlignCenter)
        self.spinbox_threshold.setMinimum(0)
        self.spinbox_threshold.setMaximum(255)

        self.layout_config_threshold.addWidget(self.spinbox_threshold)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_config_threshold.addItem(self.horizontalSpacer_4)

        self.layout_config_threshold.setStretch(0, 3)
        self.layout_config_threshold.setStretch(1, 3)
        self.layout_config_threshold.setStretch(2, 4)

        self.verticalLayout.addLayout(self.layout_config_threshold)

        self.layout_config_down_sample = QHBoxLayout()
        self.layout_config_down_sample.setObjectName(u"layout_config_down_sample")
        self.layout_config_down_sample.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_down_sample.setContentsMargins(-1, 0, -1, 0)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setIndent(0)

        self.layout_config_down_sample.addWidget(self.label_8)

        self.doubleSpinBox_down_sample = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_down_sample.setObjectName(u"doubleSpinBox_down_sample")
        self.doubleSpinBox_down_sample.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_down_sample.setMinimum(1.000000000000000)
        self.doubleSpinBox_down_sample.setMaximum(1000.000000000000000)
        self.doubleSpinBox_down_sample.setSingleStep(0.100000000000000)

        self.layout_config_down_sample.addWidget(self.doubleSpinBox_down_sample)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_config_down_sample.addItem(self.horizontalSpacer_5)

        self.layout_config_down_sample.setStretch(0, 3)
        self.layout_config_down_sample.setStretch(1, 3)
        self.layout_config_down_sample.setStretch(2, 4)

        self.verticalLayout.addLayout(self.layout_config_down_sample)

        self.layout_config_file_format = QHBoxLayout()
        self.layout_config_file_format.setObjectName(u"layout_config_file_format")
        self.layout_config_file_format.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_file_format.setContentsMargins(-1, 0, -1, 0)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setIndent(0)

        self.layout_config_file_format.addWidget(self.label_5)

        self.lineEdit_file_format = QLineEdit(self.centralwidget)
        self.lineEdit_file_format.setObjectName(u"lineEdit_file_format")
        sizePolicy3.setHeightForWidth(self.lineEdit_file_format.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_format.setSizePolicy(sizePolicy3)
        self.lineEdit_file_format.setFont(font)
        self.lineEdit_file_format.setAlignment(Qt.AlignCenter)

        self.layout_config_file_format.addWidget(self.lineEdit_file_format)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_config_file_format.addItem(self.horizontalSpacer)

        self.layout_config_file_format.setStretch(0, 3)
        self.layout_config_file_format.setStretch(1, 3)
        self.layout_config_file_format.setStretch(2, 4)

        self.verticalLayout.addLayout(self.layout_config_file_format)

        self.layout_config_file_format_2 = QHBoxLayout()
        self.layout_config_file_format_2.setObjectName(u"layout_config_file_format_2")
        self.layout_config_file_format_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_config_file_format_2.setContentsMargins(-1, 0, -1, 0)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setIndent(0)

        self.layout_config_file_format_2.addWidget(self.label_7)

        self.lineEdit_target_dir = QLineEdit(self.centralwidget)
        self.lineEdit_target_dir.setObjectName(u"lineEdit_target_dir")
        self.lineEdit_target_dir.setAlignment(Qt.AlignCenter)

        self.layout_config_file_format_2.addWidget(self.lineEdit_target_dir)

        self.button_choose_target_dir = QPushButton(self.centralwidget)
        self.button_choose_target_dir.setObjectName(u"button_choose_target_dir")
        sizePolicy3.setHeightForWidth(self.button_choose_target_dir.sizePolicy().hasHeightForWidth())
        self.button_choose_target_dir.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font3.setPointSize(10)
        self.button_choose_target_dir.setFont(font3)

        self.layout_config_file_format_2.addWidget(self.button_choose_target_dir)

        self.layout_config_file_format_2.setStretch(0, 3)
        self.layout_config_file_format_2.setStretch(1, 3)
        self.layout_config_file_format_2.setStretch(2, 4)

        self.verticalLayout.addLayout(self.layout_config_file_format_2)

        self.layout_operation = QHBoxLayout()
        self.layout_operation.setObjectName(u"layout_operation")
        self.layout_operation.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_operation.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_8)

        self.button_choose_file = QPushButton(self.centralwidget)
        self.button_choose_file.setObjectName(u"button_choose_file")
        sizePolicy3.setHeightForWidth(self.button_choose_file.sizePolicy().hasHeightForWidth())
        self.button_choose_file.setSizePolicy(sizePolicy3)
        self.button_choose_file.setFont(font3)

        self.layout_operation.addWidget(self.button_choose_file)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_10)

        self.button_convert = QPushButton(self.centralwidget)
        self.button_convert.setObjectName(u"button_convert")
        sizePolicy3.setHeightForWidth(self.button_convert.sizePolicy().hasHeightForWidth())
        self.button_convert.setSizePolicy(sizePolicy3)
        self.button_convert.setFont(font3)

        self.layout_operation.addWidget(self.button_convert)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.layout_operation.addItem(self.horizontalSpacer_9)

        self.layout_operation.setStretch(0, 1)
        self.layout_operation.setStretch(1, 2)
        self.layout_operation.setStretch(2, 1)
        self.layout_operation.setStretch(3, 2)
        self.layout_operation.setStretch(4, 1)

        self.verticalLayout.addLayout(self.layout_operation)

        Slicer.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Slicer)
        self.statusbar.setObjectName(u"statusbar")
        font4 = QFont()
        font4.setFamilies([u"\u4eff\u5b8b"])
        font4.setPointSize(10)
        self.statusbar.setFont(font4)
        Slicer.setStatusBar(self.statusbar)

        self.retranslateUi(Slicer)

        QMetaObject.connectSlotsByName(Slicer)
    # setupUi

    def retranslateUi(self, Slicer):
        Slicer.setWindowTitle(QCoreApplication.translate("Slicer", u"\u56fe\u7247\u5207\u7247\u5668", None))
        self.action_choose_file.setText(QCoreApplication.translate("Slicer", u"\u9009\u62e9\u6587\u4ef6", None))
        self.action_convert.setText(QCoreApplication.translate("Slicer", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.action_help.setText(QCoreApplication.translate("Slicer", u"\u4f7f\u7528\u5e2e\u52a9", None))
        self.action_about.setText(QCoreApplication.translate("Slicer", u"\u5173\u4e8e\u4f5c\u8005", None))
        self.label.setText(QCoreApplication.translate("Slicer", u"\u5207\u7247\u5927\u5c0f", None))
        self.label_2.setText(QCoreApplication.translate("Slicer", u"\u00d7", None))
        self.label_6.setText(QCoreApplication.translate("Slicer", u"\u820d\u5f03\u8fb9\u7f18", None))
        self.checkbox_drop_last.setText(QCoreApplication.translate("Slicer", u"\u542f\u7528", None))
        self.label_3.setText(QCoreApplication.translate("Slicer", u"\u662f\u5426\u8fc7\u6ee4", None))
        self.checkbox_enable_filter.setText(QCoreApplication.translate("Slicer", u"\u542f\u7528", None))
        self.label_4.setText(QCoreApplication.translate("Slicer", u"\u767d\u8272\u9608\u503c", None))
        self.label_8.setText(QCoreApplication.translate("Slicer", u"\u964d\u91c7\u6837\u503c", None))
        self.label_5.setText(QCoreApplication.translate("Slicer", u"\u6587\u4ef6\u683c\u5f0f", None))
        self.label_7.setText(QCoreApplication.translate("Slicer", u"\u8f93\u51fa\u5730\u5740", None))
        self.lineEdit_target_dir.setText("")
        self.lineEdit_target_dir.setPlaceholderText(QCoreApplication.translate("Slicer", u"\u81ea\u52a8\u6307\u5b9a", None))
        self.button_choose_target_dir.setText(QCoreApplication.translate("Slicer", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.button_choose_file.setText(QCoreApplication.translate("Slicer", u"\u9009\u62e9\u6587\u4ef6", None))
        self.button_convert.setText(QCoreApplication.translate("Slicer", u"\u5f00\u59cb\u8f6c\u6362", None))
    # retranslateUi

