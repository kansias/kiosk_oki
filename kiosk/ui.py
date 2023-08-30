# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerPQbpFw.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1072, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"	\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Menu_layout = QVBoxLayout()
        self.Menu_layout.setObjectName(u"Menu_layout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(640, 0))
        self.label_3.setMaximumSize(QSize(1100, 15))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.Menu_layout.addWidget(self.label_3)
        self.Menu_layout.addLayout(self.gridLayout)


        self.horizontalLayout.addLayout(self.Menu_layout)

        self.Order_layout = QVBoxLayout()
        self.Order_layout.setObjectName(u"Order_layout")
        self.Order_layout.SetMinimumSize(QSize(400, 0))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(550, 480))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widget)
        self.centralwidget.layout().setAlignment(self.label, Qt.AlignCenter)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label)


        self.Order_layout.addWidget(self.widget)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.Order_layout.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.Order_layout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"오키", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"메뉴", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"CAM", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"주문하실 메뉴를 말씀해주세요.", None))
    # retranslateUi

