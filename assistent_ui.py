# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assistent.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QFrame, QLabel,
    QMainWindow, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 911)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.prompt = QLabel(self.centralwidget)
        self.prompt.setObjectName(u"prompt")
        self.prompt.setMinimumSize(QSize(0, 22))

        self.verticalLayout_2.addWidget(self.prompt)

        self.text_user = QTextEdit(self.centralwidget)
        self.text_user.setObjectName(u"text_user")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_user.sizePolicy().hasHeightForWidth())
        self.text_user.setSizePolicy(sizePolicy)
        self.text_user.setMinimumSize(QSize(400, 200))
        self.text_user.setMaximumSize(QSize(16777215, 200))
        self.text_user.setBaseSize(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.text_user)

        self.button_abort = QCommandLinkButton(self.centralwidget)
        self.button_abort.setObjectName(u"button_abort")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_abort.sizePolicy().hasHeightForWidth())
        self.button_abort.setSizePolicy(sizePolicy1)
        self.button_abort.setMinimumSize(QSize(0, 0))
        self.button_abort.setMaximumSize(QSize(80, 30))

        self.verticalLayout_2.addWidget(self.button_abort, 0, Qt.AlignRight)

        self.text_message = QTextEdit(self.centralwidget)
        self.text_message.setObjectName(u"text_message")
        self.text_message.setEnabled(True)
        sizePolicy.setHeightForWidth(self.text_message.sizePolicy().hasHeightForWidth())
        self.text_message.setSizePolicy(sizePolicy)
        self.text_message.setMinimumSize(QSize(400, 600))
        self.text_message.setBaseSize(QSize(0, 0))
        self.text_message.setFrameShape(QFrame.NoFrame)
        self.text_message.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.text_message)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.corner = QFrame(self.centralwidget)
        self.corner.setObjectName(u"corner")
        self.corner.setMinimumSize(QSize(10, 10))
        self.corner.setFrameShape(QFrame.NoFrame)
        self.corner.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.corner, 0, Qt.AlignRight|Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.text_user, self.button_abort)
        QWidget.setTabOrder(self.button_abort, self.text_message)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.prompt.setText(QCoreApplication.translate("MainWindow", u"Prompt", None))
#if QT_CONFIG(tooltip)
        self.button_abort.setToolTip(QCoreApplication.translate("MainWindow", u"Press to submit", None))
#endif // QT_CONFIG(tooltip)
        self.button_abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.text_message.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.text_message.setPlaceholderText(QCoreApplication.translate("MainWindow", u"GPT Answer:", None))
        pass
    # retranslateUi

