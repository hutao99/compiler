from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication


class Ui_MainWindow_LR(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1033, 837)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setStyleSheet('QWidget{background-color:%s}' % QColor("#c9daf8").name())
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(510, 190, 521, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开文件")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 6)

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(510, 0, 521, 191))
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 6)

        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setEnabled(True)
        self.pushButton_1.setGeometry(QtCore.QRect(510, 190, 521, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.setText("显示状态信息")
        self.gridLayout.addWidget(self.pushButton_1, 3, 0, 1, 6)

        # 显示图片
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 511, 191))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        self.gridLayout.addWidget(self.textEdit_2, 4, 0, 5, 6)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 190, 521, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("构建LR分析表")
        self.gridLayout.addWidget(self.pushButton_2, 0, 6, 1, 1)

        # 构建LR分析表
        self.tableStack = QtWidgets.QTableWidget(self.centralwidget)
        self.tableStack.setGeometry(QtCore.QRect(510, 240, 521, 550))
        self.tableStack.setObjectName("tableStack")
        self.tableStack.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.tableStack, 1, 6, 3, 2)

        # self.tableStack.setColumnCount(4)

        # 设置tablewidget 栈分析表的表头
        # self.tableStack.setHorizontalHeaderLabels(["输入栈", "剩余输入串", "所用表达式", "动作"])
        self.tableStack.horizontalHeader().setVisible(True)  # 显示行表头

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.setGeometry(QtCore.QRect(510, 190, 521, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("输入分析句子")
        self.gridLayout.addWidget(self.pushButton_4, 4, 6, 1, 1)

        # 输入测试内容
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(0, 0, 511, 191))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_2")
        self.textEdit_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        self.gridLayout.addWidget(self.textEdit_3, 5, 6, 1, 1)

        # 分析句子
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 190, 521, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("分析")
        self.gridLayout.addWidget(self.pushButton_3, 6, 6, 1, 1)

        self.tableStack1 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableStack1.setGeometry(QtCore.QRect(510, 240, 521, 240))
        self.tableStack1.setObjectName("tableStack")
        self.tableStack1.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.tableStack1, 7, 6, 2, 2)

        #
        # self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        # self.textEdit_4.setGeometry(QtCore.QRect(0, 0, 511, 191))
        # font = QtGui.QFont()
        # font.setPointSize(18)
        # self.textEdit_4.setFont(font)
        # self.textEdit_4.setObjectName("textEdit_4")
        # self.textEdit_4.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        # self.gridLayout.addWidget(self.textEdit_4, 7, 6, 2, 2)

        MainWindow.setCentralWidget(self.centralwidget)
