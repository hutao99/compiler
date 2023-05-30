from PyQt5 import QtCore, QtGui, QtWidgets


# 界面UI类
from PyQt5.QtGui import QColor


class Ui_MainWindow_LL(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1033, 837)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setStyleSheet('QWidget{background-color:%s}' % QColor("#c9daf8").name())
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(510, 0, 521, 191))
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setItalic(True)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.gridLayout.addWidget(self.textEdit, 0, 2, 1, 1)

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

        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)

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

        self.gridLayout.addWidget(self.pushButton_1, 1, 0, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(0, 790, 1031, 44))
        self.lineEdit.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.lineEdit, 4, 0, 1, 3)

        self.tableStack = QtWidgets.QTableWidget(self.centralwidget)
        self.tableStack.setGeometry(QtCore.QRect(510, 240, 521, 550))
        self.tableStack.setObjectName("tableStack")
        self.tableStack.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.tableStack, 2, 2, 2, 1)

        self.tableStack.setColumnCount(4)

        # 设置tablewidget 栈分析表的表头
        self.tableStack.setHorizontalHeaderLabels(["输入栈", "剩余输入串", "所用表达式", "动作"])
        self.tableStack.horizontalHeader().setVisible(True)  # 显示行表头
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 511, 191))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.textEdit_2, 0, 0, 1, 2)

        self.textFirst_set = QtWidgets.QTextEdit(self.centralwidget)
        self.textFirst_set.setGeometry(QtCore.QRect(0, 240, 256, 192))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.textFirst_set.setFont(font)
        self.textFirst_set.setObjectName("textFirst_set")
        self.textFirst_set.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.textFirst_set, 2, 0, 1, 1)

        self.textFollow_set = QtWidgets.QTextEdit(self.centralwidget)
        self.textFollow_set.setGeometry(QtCore.QRect(255, 240, 256, 192))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.textFollow_set.setFont(font)
        self.textFollow_set.setObjectName("textFollow_set")
        self.textFollow_set.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.textFollow_set, 2, 1, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 190, 511, 51))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton.setText("预测分析")
        self.pushButton_1.setText("选择文件")
        self.lineEdit.setText("                                           LL1预测分析")
        self.pushButton_2.setText("文法分析")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.tableAnalyze = QtWidgets.QTableWidget(self.centralwidget)
        self.tableAnalyze.setGeometry(QtCore.QRect(0, 430, 511, 361))
        self.tableAnalyze.setObjectName("tableAnalyze")
        self.tableAnalyze.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.gridLayout.addWidget(self.tableAnalyze, 3, 0, 1, 2)

        # 隐藏分析表的横纵表头
        self.tableAnalyze.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableAnalyze.horizontalHeader().setVisible(False)  # 隐藏水平表头
        MainWindow.setCentralWidget(self.centralwidget)

        # self.tableAnalyze.setColumnCount(0)
        # self.tableAnalyze.setRowCount(0)



# https://blog.51cto.com/u_13796931/5869022

