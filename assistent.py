# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assistent.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 911)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.prompt = QtWidgets.QLabel(self.centralwidget)
        self.prompt.setMinimumSize(QtCore.QSize(0, 22))
        self.prompt.setObjectName("prompt")
        self.verticalLayout_2.addWidget(self.prompt)
        self.test_user = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test_user.sizePolicy().hasHeightForWidth())
        self.test_user.setSizePolicy(sizePolicy)
        self.test_user.setMinimumSize(QtCore.QSize(400, 200))
        self.test_user.setMaximumSize(QtCore.QSize(16777215, 200))
        self.test_user.setBaseSize(QtCore.QSize(0, 0))
        self.test_user.setObjectName("test_user")
        self.verticalLayout_2.addWidget(self.test_user)
        self.button_submit = QtWidgets.QCommandLinkButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_submit.sizePolicy().hasHeightForWidth())
        self.button_submit.setSizePolicy(sizePolicy)
        self.button_submit.setMinimumSize(QtCore.QSize(0, 0))
        self.button_submit.setMaximumSize(QtCore.QSize(80, 30))
        self.button_submit.setObjectName("button_submit")
        self.verticalLayout_2.addWidget(self.button_submit, 0, QtCore.Qt.AlignRight)
        self.text_message = QtWidgets.QTextEdit(self.centralwidget)
        self.text_message.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_message.sizePolicy().hasHeightForWidth())
        self.text_message.setSizePolicy(sizePolicy)
        self.text_message.setMinimumSize(QtCore.QSize(400, 600))
        self.text_message.setBaseSize(QtCore.QSize(0, 0))
        self.text_message.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.text_message.setReadOnly(True)
        self.text_message.setObjectName("text_message")
        self.verticalLayout_2.addWidget(self.text_message)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.corner = QtWidgets.QFrame(self.centralwidget)
        self.corner.setMinimumSize(QtCore.QSize(10, 10))
        self.corner.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.corner.setFrameShadow(QtWidgets.QFrame.Plain)
        self.corner.setObjectName("corner")
        self.verticalLayout.addWidget(self.corner, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.test_user, self.button_submit)
        MainWindow.setTabOrder(self.button_submit, self.text_message)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.prompt.setText(_translate("MainWindow", "Prompt"))
        self.button_submit.setToolTip(_translate("MainWindow", "Press to submit"))
        self.button_submit.setText(_translate("MainWindow", "Submit"))
        self.text_message.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.text_message.setPlaceholderText(_translate("MainWindow", "GPT Answer:"))
