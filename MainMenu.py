# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_mainmenu(object):
    def setupUi(self, mainmenu):
        if not mainmenu.objectName():
            mainmenu.setObjectName(u"mainmenu")
        mainmenu.resize(800, 600)
        mainmenu.setStyleSheet(u"QWidget{\n"
"	background-color:rgb(188, 212, 222);\n"
"}\n"
"QPushButton{\n"
"	background-color:rgb(165, 204, 209);\n"
"}")
        self.verticalLayoutWidget = QWidget(mainmenu)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        #self.verticalLayoutWidget.setGeometry(QRect(0, 0, 181, 191))
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 300, 300))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addWidget(self.pushButton_4)


        self.retranslateUi(mainmenu)

        QMetaObject.connectSlotsByName(mainmenu)
    # setupUi

    def retranslateUi(self, mainmenu):
        mainmenu.setWindowTitle(QCoreApplication.translate("mainmenu", u"mainmenu", None))
        self.label.setText(QCoreApplication.translate("mainmenu", u"Eartrainer", None))
        self.label_2.setText(QCoreApplication.translate("mainmenu", u"Select exercise type:", None))
        self.pushButton_2.setText(QCoreApplication.translate("mainmenu", u"Chords", None))
        self.pushButton.setText(QCoreApplication.translate("mainmenu", u"Intervals", None))
        self.pushButton_3.setText(QCoreApplication.translate("mainmenu", u"Scales", None))
        self.pushButton_4.setText(QCoreApplication.translate("mainmenu", u"Solfa", None))
    # retranslateUi

