# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kioskcXFLjr.ui'
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
        MainWindow.resize(1334, 707)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget  {\n"
"background-color: #222222;\n"
"}")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_frame = QFrame(self.page)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 60))
        self.top_frame.setMaximumSize(QSize(16777215, 55))
        self.top_frame.setStyleSheet(u"QFrame {\n"
"background-color: #fafafa;\n"
"border-radius : 5px;\n"
"\n"
"}")
        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.top_frame)
        self.horizontalLayout_4.setSpacing(22)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, 11)
        self.option_Button = QPushButton(self.top_frame)
        self.option_Button.setObjectName(u"option_Button")
        self.option_Button.setMinimumSize(QSize(30, 30))
        self.option_Button.setMaximumSize(QSize(30, 30))
        self.option_Button.setStyleSheet(u"QPushButton {\n"
"background-color: #fafafa;\n"
"}")
        self.option_Button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.option_Button)

        self.top_label1 = QLabel(self.top_frame)
        self.top_label1.setObjectName(u"top_label1")
        self.top_label1.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamily(u"\ud734\uba3c\ub465\uadfc\ud5e4\ub4dc\ub77c\uc778")
        font.setPointSize(16)
        self.top_label1.setFont(font)
        self.top_label1.setLayoutDirection(Qt.LeftToRight)
        self.top_label1.setStyleSheet(u"")
        self.top_label1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.top_label1)

        self.top_label2 = QLabel(self.top_frame)
        self.top_label2.setObjectName(u"top_label2")
        self.top_label2.setMinimumSize(QSize(0, 35))
        font1 = QFont()
        font1.setFamily(u"\ud734\uba3c\ub465\uadfc\ud5e4\ub4dc\ub77c\uc778")
        font1.setPointSize(22)
        self.top_label2.setFont(font1)
        self.top_label2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.top_label2)


        self.verticalLayout.addWidget(self.top_frame)

        self.main_frame = QFrame(self.page)
        self.main_frame.setObjectName(u"main_frame")
        self.horizontalLayout = QHBoxLayout(self.main_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menu_frame = QFrame(self.main_frame)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setMinimumSize(QSize(900, 0))
        self.menu_frame.setFrameShape(QFrame.Panel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.Menu_layout = QVBoxLayout(self.menu_frame)
        self.Menu_layout.setObjectName(u"Menu_layout")
        self.Menu_layout.setContentsMargins(5, -1, 5, 5)
        self.frame_2 = QFrame(self.menu_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 50))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(640, 30))
        self.label_3.setMaximumSize(QSize(640, 30))
        font2 = QFont()
        font2.setFamily(u"\ud734\uba3c\ub465\uadfc\ud5e4\ub4dc\ub77c\uc778")
        font2.setPointSize(14)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"QLabel {\n"
"background-color: #fafafa;\n"
"border-radius : 5px;\n"
"}")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)


        self.Menu_layout.addWidget(self.frame_2)

        self.list_frame = QFrame(self.menu_frame)
        self.list_frame.setObjectName(u"list_frame")
        self.list_frame.setStyleSheet(u"QFrame {\n"
"background-color: #fafafa;\n"
"border-radius : 5px;\n"
"\n"
"}")
        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.list_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout_2.addLayout(self.gridLayout)


        self.Menu_layout.addWidget(self.list_frame)


        self.horizontalLayout.addWidget(self.menu_frame)

        self.order_frame = QFrame(self.main_frame)
        self.order_frame.setObjectName(u"order_frame")
        self.order_frame.setMaximumSize(QSize(455, 16777215))
        self.order_frame.setLayoutDirection(Qt.LeftToRight)
        self.order_frame.setAutoFillBackground(False)
        self.order_frame.setFrameShape(QFrame.Panel)
        self.order_frame.setFrameShadow(QFrame.Raised)
        self.order_frame.setLineWidth(1)
        self.Order_layout = QVBoxLayout(self.order_frame)
        self.Order_layout.setObjectName(u"Order_layout")
        self.Order_layout.setContentsMargins(-1, 0, -1, -1)
        self.label_4 = QLabel(self.order_frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setMaximumSize(QSize(16777215, 30))
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"QLabel {\n"
"background-color: #fafafa;\n"
"border-radius : 5px;\n"
"}")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.Order_layout.addWidget(self.label_4)

        self.cam_frame = QFrame(self.order_frame)
        self.cam_frame.setObjectName(u"cam_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cam_frame.sizePolicy().hasHeightForWidth())
        self.cam_frame.setSizePolicy(sizePolicy)
        self.cam_frame.setMinimumSize(QSize(320, 240))
        self.cam_frame.setMaximumSize(QSize(2000, 240))
        self.cam_frame.setFrameShape(QFrame.Box)
        self.cam_frame.setFrameShadow(QFrame.Sunken)
        self.cam_frame.setLineWidth(4)
        self.verticalLayout_3 = QVBoxLayout(self.cam_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.cam_frame)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMaximumSize(QSize(320, 16777215))
        self.label.setStyleSheet(u"QLabel {\n"
"	background-color: rgb(218, 218, 218);\n"
"}")
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Plain)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label)


        self.Order_layout.addWidget(self.cam_frame, 0, Qt.AlignHCenter)

        self.ment_frame = QFrame(self.order_frame)
        self.ment_frame.setObjectName(u"ment_frame")
        self.ment_frame.setFrameShape(QFrame.StyledPanel)
        self.ment_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.ment_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ment_label = QLabel(self.ment_frame)
        self.ment_label.setObjectName(u"ment_label")
        self.ment_label.setMinimumSize(QSize(0, 50))
        self.ment_label.setMaximumSize(QSize(16777215, 50))
        font3 = QFont()
        font3.setFamily(u"\ud568\ucd08\ub86c\ub3cb\uc6c0")
        font3.setPointSize(16)
        font3.setBold(False)
        font3.setWeight(50)
        self.ment_label.setFont(font3)
        self.ment_label.setStyleSheet(u"QLabel {\n"
"	color: rgb(255, 182, 11);\n"
"}")
        self.ment_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.ment_label)

        self.ex_label = QLabel(self.ment_frame)
        self.ex_label.setObjectName(u"ex_label")
        self.ex_label.setMinimumSize(QSize(0, 50))
        self.ex_label.setMaximumSize(QSize(16777215, 50))
        font4 = QFont()
        font4.setFamily(u"\ud734\uba3c\ub465\uadfc\ud5e4\ub4dc\ub77c\uc778")
        font4.setPointSize(12)
        self.ex_label.setFont(font4)
        self.ex_label.setStyleSheet(u"QLabel {\n"
"	\n"
"	color: rgb(245, 245, 245);\n"
"}")
        self.ex_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.ex_label)

        self.frame = QFrame(self.ment_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(16777215, 30))
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"QLabel {\n"
"background-color: #fafafa;\n"
"border-radius : 5px;\n"
"}")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"QFrame {\n"
"	background-color: #fafafa;\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.verticalLayout_6.addLayout(self.gridLayout_2)


        self.verticalLayout_5.addWidget(self.frame_3)


        self.verticalLayout_4.addWidget(self.frame)


        self.Order_layout.addWidget(self.ment_frame)


        self.horizontalLayout.addWidget(self.order_frame)


        self.verticalLayout.addWidget(self.main_frame)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_9 = QVBoxLayout(self.page_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_5 = QFrame(self.page_2)
        self.frame_5.setObjectName(u"frame_5")
        font5 = QFont()
        font5.setFamily(u"\uc0c8\uad74\ub9bc")
        self.frame_5.setFont(font5)
        self.frame_5.setStyleSheet(u"QFrame {\n"
"	background-color: #f9f9f9;\n"
"	\n"
"\n"
"}")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_4 = QFrame(self.frame_5)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(600, 0))
        self.frame_4.setMaximumSize(QSize(600, 16777215))
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font5)

        self.horizontalLayout_6.addWidget(self.label_5, 0, Qt.AlignRight)

        self.comboBox = QComboBox(self.frame_4)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(200, 0))
        self.comboBox.setMaximumSize(QSize(200, 16777215))
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"	\n"
"	background-color: #f9f9f9;\n"
"\n"
"}")

        self.horizontalLayout_6.addWidget(self.comboBox, 0, Qt.AlignLeft)

        self.connect_button = QPushButton(self.frame_4)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setMinimumSize(QSize(0, 30))
        self.connect_button.setMaximumSize(QSize(150, 30))
        self.connect_button.setStyleSheet(u"QPushButton {\n"
"  height : 30px;\n"
"  font-size: 15px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  outline: none;\n"
"  color: #fff;\n"
"  background-color: rgb(17, 229, 2);\n"
"  border: none;\n"
"  border-radius: 15px;\n"
"  font-weight : 900;\n"
"}")

        self.horizontalLayout_6.addWidget(self.connect_button)


        self.verticalLayout_7.addWidget(self.frame_4, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.back_button = QPushButton(self.frame_5)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setMinimumSize(QSize(550, 50))
        self.back_button.setMaximumSize(QSize(550, 50))
        self.back_button.setStyleSheet(u"QPushButton {\n"
"  height : 30px;\n"
"  font-size: 15px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  outline: none;\n"
"  color: #fff;\n"
"  background-color: #222222;\n"
"  border: none;\n"
"  border-radius: 15px;\n"
"  font-weight : 900;\n"
"}")

        self.verticalLayout_7.addWidget(self.back_button, 0, Qt.AlignHCenter)


        self.verticalLayout_9.addWidget(self.frame_5)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_8.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.option_Button.setText("")
        self.top_label1.setText(QCoreApplication.translate("MainWindow", u"Smart Kiosk", None))
        self.top_label2.setText(QCoreApplication.translate("MainWindow", u"\uc624\ud0a4", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uba54\ub274", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38 \uc811\uc218", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"CAM", None))
        self.ment_label.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38\ud558\uc2e4 \uba54\ub274\ub97c \ub9d0\uc500\ud574\uc8fc\uc138\uc694.", None))
        self.ex_label.setText(QCoreApplication.translate("MainWindow", u"\uc608) \"000 \uc8fc\uc138\uc694\"", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38 \ub0b4\uc5ed", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc7a5\uce58", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.back_button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
    # retranslateUi

