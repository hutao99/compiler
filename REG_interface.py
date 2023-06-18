# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'REG_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QSplitter


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1033, 837)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(80, 100, 104, 64))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(210, 100, 104, 64))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(360, 100, 104, 64))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(200, 190, 104, 64))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 270, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 270, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 270, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        font = QFont()
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit_2.setFont(font)
        self.plainTextEdit_3.setFont(font)
        self.textEdit.setFont(font)

        self.splitter1 = QSplitter()
        self.splitter1.addWidget(self.plainTextEdit)
        self.splitter1.addWidget(self.plainTextEdit_2)
        self.splitter1.addWidget(self.plainTextEdit_3)
        self.splitter2 = QSplitter()
        self.splitter2.addWidget(self.pushButton)
        self.splitter2.addWidget(self.pushButton_2)
        self.splitter2.addWidget(self.pushButton_3)
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.splitter1)
        self.splitter.addWidget(self.textEdit)
        self.splitter.addWidget(self.splitter2)
        self.gridLayout.addWidget(self.splitter, 0, 1, 0, 1)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 879, 22))
        self.menubar.setObjectName("menubar")
        self.menu_F = QtWidgets.QMenu(self.menubar)
        self.menu_F.setObjectName("menu_F")
        self.menu_E = QtWidgets.QMenu(self.menubar)
        self.menu_E.setObjectName("menu_E")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_NFA_DFA = QtWidgets.QMenu(self.menubar)
        self.menu_NFA_DFA.setObjectName("menu_NFA_DFA")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_lexicalAnalyzer = QtWidgets.QAction(MainWindow)
        self.action_lexicalAnalyzer.setObjectName("action_lexicalAnalyzer")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_NFA = QtWidgets.QAction(MainWindow)
        self.action_NFA.setObjectName("action_NFA")
        self.actionNFA_DFA = QtWidgets.QAction(MainWindow)
        self.actionNFA_DFA.setObjectName("actionNFA_DFA")
        self.actionDFA_MFA = QtWidgets.QAction(MainWindow)
        self.actionDFA_MFA.setObjectName("actionDFA_MFA")
        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_13 = QtWidgets.QAction(MainWindow)
        self.action_13.setObjectName("action_13")
        self.actionNFA_DFA_2 = QtWidgets.QAction(MainWindow)
        self.actionNFA_DFA_2.setObjectName("actionNFA_DFA_2")
        self.actionDFA_MFA_2 = QtWidgets.QAction(MainWindow)
        self.actionDFA_MFA_2.setObjectName("actionDFA_MFA_2")
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(MainWindow)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_DFA_MFA = QtWidgets.QAction(MainWindow)
        self.action_DFA_MFA.setObjectName("action_DFA_MFA")
        self.action_NFA_DFA = QtWidgets.QAction(MainWindow)
        self.action_NFA_DFA.setObjectName("action_NFA_DFA")
        self.action_DFA_MFA_2 = QtWidgets.QAction(MainWindow)
        self.action_DFA_MFA_2.setObjectName("action_DFA_MFA_2")
        self.action_NFA_2 = QtWidgets.QAction(MainWindow)
        self.action_NFA_2.setObjectName("action_NFA_2")
        self.action_DFA = QtWidgets.QAction(MainWindow)
        self.action_DFA.setObjectName("action_DFA")
        self.action_MFA = QtWidgets.QAction(MainWindow)
        self.action_MFA.setObjectName("action_MFA")
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_DFA_2 = QtWidgets.QAction(MainWindow)
        self.action_DFA_2.setObjectName("action_DFA_2")
        self.action_MFA_2 = QtWidgets.QAction(MainWindow)
        self.action_MFA_2.setObjectName("action_MFA_2")
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.menu_F.addAction(self.action_7)
        self.menu_F.addAction(self.action_10)
        self.menu_F.addAction(self.action_13)

        self.menu_E.addAction(self.action_6)
        self.menu_E.addAction(self.actionNFA_DFA_2)
        self.menu_E.addAction(self.actionDFA_MFA_2)
        self.menu_E.addAction(self.action_8)
        self.menu.addAction(self.action_9)
        self.menu_NFA_DFA.addAction(self.action_NFA_DFA)
        self.menu_NFA_DFA.addAction(self.action_DFA_MFA_2)
        self.menu_2.addAction(self.action_NFA_2)
        self.menu_2.addAction(self.action_DFA)
        self.menu_2.addAction(self.action_MFA)
        self.menu_2.addAction(self.action_11)
        self.menu_2.addAction(self.action_DFA_2)
        self.menu_2.addAction(self.action_MFA_2)
        self.menu_2.addAction(self.action_12)
        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_E.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_NFA_DFA.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "REG正则表达式转换"))

        self.plainTextEdit.setPlaceholderText("输入正规式或NFA或DFA或导入文件")
        self.plainTextEdit_2.setPlaceholderText("输入待识别的符号串或导入文件")
        self.plainTextEdit_3.setPlaceholderText("状态转换图文字结果或词法分析结果")
        self.textEdit.setPlaceholderText("状态转换图结果")

        self.pushButton.setText(_translate("MainWindow", "NFA"))
        self.pushButton_2.setText(_translate("MainWindow", "DFA"))
        self.pushButton_3.setText(_translate("MainWindow", "MFA"))
        self.menu_F.setTitle(_translate("MainWindow", "导入文件"))
        self.menu_E.setTitle(_translate("MainWindow", "REG正则表达式转换"))
        self.menu.setTitle(_translate("MainWindow", "词法分析"))
        self.menu_NFA_DFA.setTitle(_translate("MainWindow", "单独转换"))
        self.menu_2.setTitle(_translate("MainWindow", "导出文件"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_lexicalAnalyzer.setText(_translate("MainWindow", " 词法分析器1"))
        self.action_2.setText(_translate("MainWindow", " 词法分析器2"))
        self.action.setText(_translate("MainWindow", " 语法分析器"))
        self.action_3.setText(_translate("MainWindow", "生成中间代码"))
        self.action_4.setText(_translate("MainWindow", " 算符优先"))
        self.action_5.setText(_translate("MainWindow", "生成目标代码"))
        self.action_NFA.setText(_translate("MainWindow", "正规式转NFA"))
        self.actionNFA_DFA.setText(_translate("MainWindow", "NFA转DFA"))
        self.actionDFA_MFA.setText(_translate("MainWindow", "DFA转MFA"))
        self.action_6.setText(_translate("MainWindow", "正规式转NFA"))
        self.action_7.setText(_translate("MainWindow", "导入正规式"))
        self.actionNFA_DFA_2.setText(_translate("MainWindow", "NFA转DFA"))
        self.actionDFA_MFA_2.setText(_translate("MainWindow", "DFA转MFA"))
        self.action_8.setText(_translate("MainWindow", "一键三连"))
        self.action_9.setText(_translate("MainWindow", "词法分析"))
        self.action_10.setText(_translate("MainWindow", "导入待识别符号串文件"))
        self.action_13.setText(_translate("MainWindow", "导入NFA或DFA"))
        self.action_DFA_MFA.setText(_translate("MainWindow", "DFA转MFA"))
        self.action_NFA_DFA.setText(_translate("MainWindow", "NFA转DFA"))
        self.action_DFA_MFA_2.setText(_translate("MainWindow", "DFA转MFA"))
        self.action_NFA_2.setText(_translate("MainWindow", "导出NFA"))
        self.action_DFA.setText(_translate("MainWindow", "导出DFA"))
        self.action_MFA.setText(_translate("MainWindow", "导出MFA"))
        self.action_11.setText(_translate("MainWindow", "导出NFA状态转换图"))
        self.action_DFA_2.setText(_translate("MainWindow", "导出DFA状态转换图"))
        self.action_MFA_2.setText(_translate("MainWindow", "导出MFA状态转换图"))
        self.action_12.setText(_translate("MainWindow", "导出全部"))
