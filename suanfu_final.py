from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QComboBox, QDialog, QPushButton, \
    QHBoxLayout

import Analyzer
from TABLE import Predictive_Analysis, ASTNode

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox
import sys


class LL1GrammarSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个选项卡窗口部件
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.setWindowTitle("算符优先分析")
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.tabWidget.resize(800, 600)

        # 创建第一个选项卡
        self.tab1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab1, "FirstVT和LastVT")
        # 创建下拉框，用于选择模式
        self.mode_combo = QComboBox(self.tab1)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.mode_combo.setFont(font)

        self.mode_combo.setWindowTitle('模式选择')
        self.mode_combo.setObjectName('模式选择')
        self.mode_combo.addItem("系统分词模式")
        self.mode_combo.addItem("用户分词模式")
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        self.mode_combo.setStyleSheet("#模式选择 {text-align:center;} QComboBox::drop-down {subcontrol-origin: padding; subcontrol-position: top right; width: 20px;}")


        # 创建第二个选项卡
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, "算符优先关系表")

        # 创建第三个选项卡
        self.tab3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab3, "测试案例")

        layout1 = QtWidgets.QGridLayout()

        # 导入LL1文法的按钮
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("算符优先文法分析")
        self.pushButton.setStyleSheet("QPushButton {text-align:left;}")

        # 导入LL1文法的按钮
        self.pushButton_ = QtWidgets.QPushButton()
        self.pushButton_.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_.setFont(font)
        self.pushButton_.setObjectName("pushButton")
        self.pushButton_.setText("导入算符优先文法")
        self.pushButton_.setStyleSheet("QPushButton {text-align:left;}")

        # 求解FIRST集合的按钮
        # 求解FOLLOW集合的按钮
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("保存FirstVT内容")

        # 显示LL1文法的内容
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        # 显示FIRST集合的内容
        self.table_FIRST = QtWidgets.QTableWidget()
        self.table_FIRST.setObjectName("tableAnalyze")
        self.table_FIRST.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        # 隐藏分析表的横纵表头
        # self.table_FIRST.verticalHeader().setVisible(False)  # 隐藏垂直表头
        # self.table_FIRST.horizontalHeader().setVisible(False)  # 隐藏水平表头

        # 显示FOLLOW集合的内容
        self.table_FOLLOW = QtWidgets.QTableWidget()
        self.table_FOLLOW.setObjectName("tableAnalyze")
        self.table_FOLLOW.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        # 隐藏分析表的横纵表头
        # self.table_FOLLOW.verticalHeader().setVisible(False)  # 隐藏垂直表头
        # self.table_FOLLOW.horizontalHeader().setVisible(False)  # 隐藏水平表头

        self.pushButton_3_ = QtWidgets.QPushButton()
        self.pushButton_3_.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3_.setFont(font)
        self.pushButton_3_.setObjectName("pushButton_2")
        self.pushButton_3_.setText("保存LastVT内容")

        # 将文法导入按钮和显示文法的文本框垂直布局
        buttonSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        buttonSplitter.addWidget(self.mode_combo)
        buttonSplitter.addWidget(self.pushButton_)
        buttonSplitter.addWidget(self.textEdit)
        buttonSplitter.addWidget(self.pushButton)

        # 将FIRST和FOLLOW集合求解按钮和显示的表格布局垂直布局
        textEditSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        textEditSplitter.addWidget(self.table_FIRST)
        textEditSplitter.addWidget(self.pushButton_2)
        textEditSplitter.addWidget(self.table_FOLLOW)
        textEditSplitter.addWidget(self.pushButton_3_)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(buttonSplitter)
        self.splitter1.addWidget(textEditSplitter)



        # 将两个水平布局添加到垂直布局中
        layout1.addWidget(self.splitter1)

        self.tab1.setLayout(layout1)
        size = self.pushButton_2.minimumSizeHint()
        self.pushButton.setFixedHeight(size.height())
        self.pushButton_.setFixedHeight(size.height())
        self.mode_combo.setFixedHeight(size.height())

        self.pushButton_.clicked.connect(self.open_text)
        #计算FirstVT、LastVT
        # self.pushButton.clicked.connect(self.onClick_create_first_follow)
        # 保存FirstVT
        # self.pushButton_2.clicked.connect(self.save_first)
        # 保存LastVT
        # self.pushButton_3_.clicked.connect(self.save_follow)

        layout2 = QtWidgets.QGridLayout()

        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("算符优先关系表")

        # 显示预测分析表的内容
        self.tableAnalyze = QtWidgets.QTableWidget()
        self.tableAnalyze.setObjectName("tableAnalyze")
        self.tableAnalyze.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        # 隐藏分析表的横纵表头
        self.tableAnalyze.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableAnalyze.horizontalHeader().setVisible(False)  # 隐藏水平表头

        self.pushButton_3__ = QtWidgets.QPushButton()
        self.pushButton_3__.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3__.setFont(font)
        self.pushButton_3__.setObjectName("pushButton_3__")
        self.pushButton_3__.setText("保存算符优先关系表")

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.pushButton_3)
        self.splitter2.addWidget(self.tableAnalyze)
        self.splitter2.addWidget(self.pushButton_3__)

        layout2.addWidget(self.splitter2)

        self.tab2.setLayout(layout2)
        size = self.pushButton_2.minimumSizeHint()
        self.pushButton_3.setFixedHeight(size.height())
        self.pushButton_3__.setFixedHeight(size.height())
        # 显示算符优先分析表
        # self.pushButton_3.clicked.connect(self.analyze_table)
        # 保存算符优先分析表
        # self.pushButton_3__.clicked.connect(self.save_analyze_table)
        # 测试案例布局
        layout3 = QtWidgets.QGridLayout()

        self.pushButton_4 = QtWidgets.QPushButton()
        self.pushButton_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("分析过程")

        # 显示待分析的内容
        self.textEdit_1 = QtWidgets.QTextEdit()
        self.textEdit_1.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setItalic(False)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit")
        # 设置提示文本
        self.textEdit_1.setPlaceholderText("请输入要分析的句子或打开本地测试案例")

        self.pushButton_5 = QtWidgets.QPushButton()
        self.pushButton_5.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("打开测试案例或手动输入")

        # 显示分析过程
        self.tableStack = QtWidgets.QTableWidget()
        self.tableStack.setObjectName("tableStack")
        self.tableStack.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5DC").name())

        self.tableStack.setColumnCount(3)

        # 设置tablewidget 栈分析表的表头
        self.tableStack.setHorizontalHeaderLabels(["符号栈", "产生式", "匹配字符"])
        '''
        使用 QSizePolicy 控件来实现 QTableWidget 表格的大小随着界面的变化而自动调整
        如果表格中的数据量很大，自动调整表格大小可能会影响程序的性能
        好处：可以在一个单元格中把所有的内容一次性展示出来
        坏处：效率变低了，还有些卡
        '''
        # 设置 QSizePolicy 控件
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.tableStack.setSizePolicy(sizePolicy)

        self.pushButton_5_ = QtWidgets.QPushButton()
        self.pushButton_5_.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_5_.setFont(font)
        self.pushButton_5_.setObjectName("pushButton_5")
        self.pushButton_5_.setText("保存算符优先分析过程")

        # 连接信号和槽
        self.tableStack.itemChanged.connect(self.onItemChanged)

        self.splitter1_ = QSplitter(Qt.Vertical)
        self.splitter1_.addWidget(self.pushButton_5)
        self.splitter1_.addWidget(self.textEdit_1)

        self.splitter2_ = QSplitter(Qt.Vertical)
        self.splitter2_.addWidget(self.splitter1_)
        self.splitter2_.addWidget(self.pushButton_4)
        self.splitter2_.addWidget(self.tableStack)
        self.splitter2_.addWidget(self.pushButton_5_)
        layout3.addWidget(self.splitter2_)

        self.tab3.setLayout(layout3)
        # 按钮显示分析栈的分析过程
        # self.pushButton_4.clicked.connect(self.onClick_analyze_stack)
        self.pushButton_5.clicked.connect(self.open_sample)
        # 保存预测分析过程
        # self.pushButton_5_.clicked.connect(self.save_analyze_process)

    def on_mode_changed(self, index):
        # 处理用户选择的模式
        mode = self.mode_combo.currentText()
        print("当前模式：", mode)

    def onItemChanged(self, item):
        # 自动调整表格大小
        self.tableStack.resizeColumnsToContents()
        self.tableStack.resizeRowsToContents()

    def select_mode(self):
        # 弹出 QDialog，并在其中添加 QComboBox 和 QPushButton
        dialog = QDialog(self.tab1)
        dialog.setModal(True)

        combo = QComboBox(dialog)
        combo.addItem("模式1")
        combo.addItem("模式2")

        button = QPushButton("确定", dialog)
        button.clicked.connect(lambda: self.on_mode_changed(combo.currentText()))

        hbox = QHBoxLayout(dialog)
        hbox.addWidget(combo)
        hbox.addWidget(button)

    def showEvent(self, event):
        super().showEvent(event)
        self.resize(800, 600)  # 调整窗口大小为800x600

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tabWidget.resize(event.size())

    def closeEvent(self, event):
        # 弹出消息框
        reply = QMessageBox.question(self, '确认', '确定要退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                print(fname[0])
                with open(fname[0], encoding=self.check_charset(fname[0])) as f:
                    str = f.read()
                    print(str)
                    self.textEdit.setText(str)
                    # self.onClick_create_first_follow()
        except Exception as e:
            print("Error: ", e)

    def open_sample(self):
        # 定义打开文件夹目录的函数
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                print(fname[0])
                with open(fname[0], encoding=self.check_charset(fname[0])) as f:
                    str = f.read()
                    print(str)
                    self.textEdit_1.setText(str)
        except Exception as e:
            print("Error: ", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LL1GrammarSolver()
    window.show()
    sys.exit(app.exec_())
