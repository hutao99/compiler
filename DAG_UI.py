from PyQt5 import QtCore, QtGui, QtWidgets


# DAG界面UI类
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSplitter


class Ui_MainWindow_DAG(object):

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
        # 设置提示文本
        self.textEdit.setPlaceholderText("存放待分析的四元式列表")

        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")


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
        self.pushButton.setText("打开四元式文件")


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
        self.pushButton_1.setText("DAG优化")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 511, 191))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        # 设置提示文本
        self.textEdit_2.setPlaceholderText("DAG优化图")

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
        self.pushButton_2.setObjectName("pushButton_1")
        self.pushButton_2.setText("查看DAG优化图")

        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(0, 240, 256, 192))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        # 设置提示文本
        self.textEdit_3.setPlaceholderText("优化后的四元式列表")

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.pushButton)
        self.splitter2.addWidget(self.textEdit)

        self.splitter3 = QSplitter(Qt.Vertical)
        self.splitter3.addWidget(self.pushButton_1)
        self.splitter3.addWidget(self.textEdit_2)
        self.splitter3.addWidget(self.textEdit_3)
        self.splitter3.addWidget(self.pushButton_2)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.splitter2)
        self.splitter1.addWidget(self.splitter3)

        sizes = [200, 300]
        self.splitter1.setSizes(sizes)
        self.gridLayout.addWidget(self.splitter1, 0, 1, 0, 1)
        size = self.pushButton_1.minimumSizeHint()
        self.pushButton.setFixedHeight(size.height())
        self.pushButton_1.setFixedHeight(size.height())
        self.pushButton_2.setFixedHeight(size.height())
        MainWindow.setCentralWidget(self.centralwidget)


