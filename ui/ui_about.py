# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(500, 300)
        self.verticalLayoutWidget = QWidget(About)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 481, 281))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.label_8 = QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_8)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 4)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 4)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 4)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_6)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 4)

        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"\u5173\u4e8e", None))
        self.label_5.setText(QCoreApplication.translate("About", u"Version", None))
        self.label_8.setText(QCoreApplication.translate("About", u"v3.8.1", None))
        self.label.setText(QCoreApplication.translate("About", u"Author", None))
        self.label_2.setText(QCoreApplication.translate("About", u"Chestnut", None))
        self.label_3.setText(QCoreApplication.translate("About", u"GitHub", None))
        self.label_4.setText(QCoreApplication.translate("About", u"li192863", None))
        self.label_6.setText(QCoreApplication.translate("About", u"Email", None))
        self.label_7.setText(QCoreApplication.translate("About", u"li1928631@163.com", None))
    # retranslateUi

