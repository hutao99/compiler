from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QComboBox

import Analyzer
from TABLE import Predictive_Analysis, ASTNode

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox
import sys


class LL1GrammarSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个选项卡窗口部件
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.setWindowTitle("LL1预测分析")
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.tabWidget.resize(800, 600)

        # 创建第一个选项卡
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.tabWidget.addTab(self.tab1, "FIRST和FOLLOW集合")

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
        self.mode_combo.setStyleSheet(
            "#模式选择 {text-align:center;} QComboBox::drop-down {subcontrol-origin: padding; subcontrol-position: top right; width: 20px;}")
        # choice=0代表系统分词模式||choice=1代表用户分词模式
        self.choice = 0
        # 创建第二个选项卡
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, "预测分析表")

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
        self.pushButton.setText("LL1文法分析")
        self.pushButton.setStyleSheet("QPushButton {text-align:left;}")
        self.pushButton.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

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
        self.pushButton_.setText("导入LL1文法")
        self.pushButton_.setStyleSheet("QPushButton {text-align:left;}")
        self.pushButton_.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

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
        self.pushButton_2.setText("保存FIRST集合内容")
        self.pushButton_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

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
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        # 显示FIRST集合的内容
        self.table_FIRST = QtWidgets.QTableWidget()
        self.table_FIRST.setObjectName("tableAnalyze")
        self.table_FIRST.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        # 隐藏分析表的横纵表头
        # self.table_FIRST.verticalHeader().setVisible(False)  # 隐藏垂直表头
        # self.table_FIRST.horizontalHeader().setVisible(False)  # 隐藏水平表头

        # 显示FOLLOW集合的内容
        self.table_FOLLOW = QtWidgets.QTableWidget()
        self.table_FOLLOW.setObjectName("tableAnalyze")
        self.table_FOLLOW.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

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
        self.pushButton_3_.setText("保存FOLLOW集合内容")
        self.pushButton_3_.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

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

        self.pushButton.clicked.connect(self.onClick_create_first_follow)
        self.pushButton_.clicked.connect(self.open_text)
        self.pushButton_2.clicked.connect(self.save_first)
        self.pushButton_3_.clicked.connect(self.save_follow)
        self.mode_combo.setFixedHeight(size.height())

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
        self.pushButton_3.setText("预测分析表")
        self.pushButton_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 显示预测分析表的内容
        self.tableAnalyze = QtWidgets.QTableWidget()
        self.tableAnalyze.setObjectName("tableAnalyze")
        self.tableAnalyze.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

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
        self.pushButton_3__.setText("保存预测分析表")

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.pushButton_3)
        self.splitter2.addWidget(self.tableAnalyze)
        self.splitter2.addWidget(self.pushButton_3__)

        layout2.addWidget(self.splitter2)

        self.tab2.setLayout(layout2)
        size = self.pushButton_2.minimumSizeHint()
        self.pushButton_3.setFixedHeight(size.height())
        self.pushButton_3__.setFixedHeight(size.height())
        self.pushButton_3.clicked.connect(self.analyze_table)
        self.pushButton_3__.clicked.connect(self.save_analyze_table)
        self.pushButton_3__.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
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
        self.pushButton_4.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 显示待分析的内容
        self.textEdit_1 = QtWidgets.QTextEdit()
        self.textEdit_1.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())
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
        self.pushButton_5.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())


        # 显示分析过程
        self.tableStack = QtWidgets.QTableWidget()
        self.tableStack.setObjectName("tableStack")
        self.tableStack.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

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
        self.pushButton_5_.setText("保存预测分析过程")

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
        if self.choice == 1:
            self.pushButton_4.clicked.connect(self.onClick_analyze_stack_1)
        elif self.choice == 0:
            self.pushButton_4.clicked.connect(self.onClick_analyze_stack_2)
        self.pushButton_5_.clicked.connect(self.save_analyze_process)

    def on_mode_changed(self, index):
        if index == 0:
            self.choice = 0
            print('用户选择了系统分词模式')
        elif index == 1:
            self.choice = 1
            print('用户选择了用户分词模式')

    def onItemChanged(self, item):
        # 自动调整表格大小
        self.tableStack.resizeColumnsToContents()
        self.tableStack.resizeRowsToContents()

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
            fname = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/11LL(1)测试用例',
                                                '文本文件 (*.txt)')
            if fname[0]:
                print(fname[0])
                with open(fname[0], encoding=self.check_charset(fname[0])) as f:
                    str = f.read()
                    print(str)
                    self.textEdit.setText(str)
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

    def onClick_create_first_follow(self):
        test = Predictive_Analysis()
        grammar = ""
        if self.choice == 0:
            text = self.textEdit.toPlainText()
            lines = text.splitlines(True)
            res = ""
            for line in lines:
                print(line.rstrip('\r\n'))
                line = line.rstrip()
                new_s = line[0]
                for i in range(1, len(line)):
                    if line[i] != ' ' and line[i - 1] != ' ':
                        new_s += ' '
                    new_s += line[i]
                print(new_s)
                res += new_s.strip() + '\n'
            print(res)
            grammar = res.replace(' - > ', ':')
            grammar = grammar.replace(' | ', '|')
        elif self.choice == 1:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')
        print("\ngrammar如下\n")
        print(grammar)
        test.input(grammar)
        VN = test.vn
        VT = test.vt
        FIRST = test.first_dict
        FOLLOW = test.last
        print('----------------------------')
        print("\nfirst集合如下\n")
        for i in test.first:
            print(i, test.first[i])
        print("\nfollow集合如下\n")
        for j in test.last:
            print(j, test.last[j])

        # 设置FIRST集合的列数
        self.table_FIRST.setColumnCount(len(VT) + 1)
        layer_analyze = 1
        # 设置FIRST集合的行数
        self.table_FIRST.setRowCount(layer_analyze)
        VT_1 = VT[:]

        for size in range(len(VT_1)):
            self.table_FIRST.setColumnWidth(size, 70)
            item1 = QtWidgets.QTableWidgetItem(VT_1[size])
            self.table_FIRST.setItem(0, size + 1, item1)

        for i in range(len(VN)):
            # 每遍历一次增加一层
            layer_analyze = layer_analyze + 1
            self.table_FIRST.setRowCount(layer_analyze)
            # 显示FIRST集合的第一列 非终结符
            item1 = QtWidgets.QTableWidgetItem(VN[i])
            self.table_FIRST.setItem(i + 1, 0, item1)
            # 显示FIRST集合的每一行 动作
            for size in range(len(VT_1)):
                if VT_1[size] in FIRST[VN[i]]:
                    item1 = QtWidgets.QTableWidgetItem(VT_1[size])
                    self.table_FIRST.setItem(i + 1, size + 1, item1)

        # FOLLOW
        self.table_FOLLOW.setColumnCount(len(VT) + 1)
        layer_analyze = 1
        self.table_FOLLOW.setRowCount(layer_analyze)
        VT_1 = VT[:]

        for size in range(len(VT_1)):
            self.table_FOLLOW.setColumnWidth(size, 70)
            item1 = QtWidgets.QTableWidgetItem(VT_1[size])
            self.table_FOLLOW.setItem(0, size + 1, item1)

        for i in range(len(VN)):
            # 没遍历一次增加一层
            layer_analyze = layer_analyze + 1
            self.table_FOLLOW.setRowCount(layer_analyze)
            item1 = QtWidgets.QTableWidgetItem(VN[i])
            self.table_FOLLOW.setItem(i + 1, 0, item1)
            # 显示预测分析表的每一行 动作
            for size in range(len(VT_1)):
                if VT_1[size] in FOLLOW[VN[i]]:
                    item1 = QtWidgets.QTableWidgetItem(VT_1[size])
                    self.table_FOLLOW.setItem(i + 1, size + 1, item1)

    def save_first(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存FIRST集合', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.table_FIRST.rowCount()):
                    for col in range(self.table_FIRST.columnCount()):
                        item = self.table_FIRST.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def save_follow(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存FOLLOW集合', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.table_FIRST.rowCount()):
                    for col in range(self.table_FIRST.columnCount()):
                        item = self.table_FIRST.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def analyze_table(self):
        test = Predictive_Analysis()
        grammar = ""
        if self.choice == 0:
            text = self.textEdit.toPlainText()
            lines = text.splitlines(True)
            res = ""
            for line in lines:
                print(line.rstrip('\r\n'))
                line = line.rstrip()
                new_s = line[0]
                for i in range(1, len(line)):
                    if line[i] != ' ' and line[i - 1] != ' ':
                        new_s += ' '
                    new_s += line[i]
                print(new_s)
                res += new_s.strip() + '\n'
            print(res)
            grammar = res.replace(' - > ', ':')
            grammar = grammar.replace(' | ', '|')
        elif self.choice == 1:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')

        test.input(grammar)
        VN = test.vn
        VT = test.vt
        SELECT = test.predict_table_
        # 设置预测分析表的列数 len(VT)+2 终结符的数量加2,2 为第一列非终结符占一列，最后#占一列
        self.tableAnalyze.setColumnCount(len(VT) + 2)
        layer_analyze = 1
        # 设置预测分析表的层数
        self.tableAnalyze.setRowCount(layer_analyze)
        VT_1 = VT[:]

        for size in range(len(VT_1)):
            self.tableAnalyze.setColumnWidth(size, 70)
            item1 = QtWidgets.QTableWidgetItem(VT_1[size])
            self.tableAnalyze.setItem(0, size + 1, item1)

        for i in range(len(VN)):
            # 没遍历一次增加一层
            layer_analyze = layer_analyze + 1
            self.tableAnalyze.setRowCount(layer_analyze)
            # 界面显示 预测分析表
            # 显示预测分析表的第一列 非终结符
            item1 = QtWidgets.QTableWidgetItem(VN[i])
            self.tableAnalyze.setItem(i + 1, 0, item1)
            # 显示预测分析表的每一行 动作
            for size in range(len(VT_1)):
                if VT_1[size] in SELECT[VN[i]]:
                    item1 = QtWidgets.QTableWidgetItem(SELECT[VN[i]][VT_1[size]])
                    self.tableAnalyze.setItem(i + 1, size + 1, item1)

    def save_analyze_table(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存预测分析表', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.tableAnalyze.rowCount()):
                    for col in range(self.tableAnalyze.columnCount()):
                        item = self.tableAnalyze.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def obtain_type(self, stack):
        res = []
        for item in stack:
            res.append(item.type)
        return res

    def onClick_analyze_stack_1(self):
        test = Predictive_Analysis()
        grammar = ""
        if self.choice == 0:
            text = self.textEdit.toPlainText()
            lines = text.splitlines(True)
            res = ""
            for line in lines:
                print(line.rstrip('\r\n'))
                line = line.rstrip()
                new_s = line[0]
                for i in range(1, len(line)):
                    if line[i] != ' ' and line[i - 1] != ' ':
                        new_s += ' '
                    new_s += line[i]
                print(new_s)
                res += new_s.strip() + '\n'
            print(res)
            grammar = res.replace(' - > ', ':')
            grammar = grammar.replace(' | ', '|')
        elif self.choice == 1:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')
        test.input(grammar)
        VN = test.vn
        VT = test.vt
        self.predict_table = test.predict_table
        self.predict_table_ = test.predict_table_
        # 获取输入串并加入‘#’结束标志
        layer_stack = 0
        # 先设置 table层数为1 后 动态增加
        self.tableStack.setRowCount(layer_stack)
        # 获取 输入串 输入框中的句子 并且保存在 STACK_INPUT 列表中
        lex = Analyzer.AnalyzerLex()
        lex.input(self.textEdit_1.toPlainText())
        word_table = []

        while True:
            tok = lex.token()
            if not tok:
                break
            s1 = ['operator', 'keyword', 'Boundary']
            s2 = ['integer', 'character', 'string', 'identifier', 'float']
            if tok.type in s1:
                word_table.append([tok.value, tok.value])
            elif tok.type in s2:
                word_table.append([tok.type, tok.value])
        word_table.append(['#', '#'])
        print('--------------------')
        print(word_table)
        stack = []
        # 注意这里的顺序
        root = ASTNode(test.begin)
        end = ASTNode("#")
        # 将#和文法开始符号压入堆栈,不能压反
        stack.append(end)
        stack.append(root)
        index = 0

        while len(stack) != 0:
            # 层数增加一层
            layer_stack = layer_stack + 1
            self.tableStack.setRowCount(layer_stack)
            cur = stack.pop()

            if cur.type == "#" and len(stack) == 0:
                print("符号栈：", self.obtain_type(stack), "\n匹配字符: ", '#')
                item1 = QtWidgets.QTableWidgetItem(str(self.obtain_type(stack)))
                self.tableStack.setItem(layer_stack - 1, 0, item1)

                item1 = QtWidgets.QTableWidgetItem(str(word_table[index][1]))
                self.tableStack.setItem(layer_stack - 1, 2, item1)

                print("分析完成")
                break
            # 输入的字符表和符号栈中节点匹配
            elif cur.type == word_table[index][0]:
                print(index)
                print("符号栈：", self.obtain_type(stack), "\n匹配字符: ", word_table[index][1])
                item1 = QtWidgets.QTableWidgetItem(str(self.obtain_type(stack)))
                self.tableStack.setItem(layer_stack - 1, 0, item1)

                item1 = QtWidgets.QTableWidgetItem(str(word_table[index][1]))
                self.tableStack.setItem(layer_stack - 1, 2, item1)

                cur.text = word_table[index][1]
                index += 1
                if index >= len(word_table):
                    index -= 1
            else:
                a = word_table[index][0]

                if a in self.predict_table[cur.type]:
                    if self.predict_table[cur.type][a] == "$":
                        print("\n符号栈：", self.obtain_type(stack), "\n产生式: ", cur.type, "->",
                              self.predict_table[cur.type][a])
                        item1 = QtWidgets.QTableWidgetItem(str(self.obtain_type(stack)))
                        self.tableStack.setItem(layer_stack - 1, 0, item1)

                        item1 = QtWidgets.QTableWidgetItem(str(self.predict_table_[cur.type][a]))
                        self.tableStack.setItem(layer_stack - 1, 1, item1)
                        continue
                    next_epr = self.predict_table[cur.type][a].split()
                    print("\n符号栈：", self.obtain_type(stack), "\n产生式: ", cur.type, "->",
                          self.predict_table[cur.type][a])
                    item1 = QtWidgets.QTableWidgetItem(str(self.obtain_type(stack)))
                    self.tableStack.setItem(layer_stack - 1, 0, item1)

                    item1 = QtWidgets.QTableWidgetItem(str(self.predict_table_[cur.type][a]))
                    self.tableStack.setItem(layer_stack - 1, 1, item1)

                    node_list = []
                    """
                       产生式右部符号入栈,反序入栈
                       子节点入栈
                     """
                    for epr in next_epr:
                        node_list.append(ASTNode(epr))
                    for nl in node_list:
                        cur.child_node.append(nl)
                    node_list.reverse()
                    for nl in node_list:
                        stack.append(nl)
                else:
                    # 发生错误,直到跳到第二行为止
                    print("error", stack, cur.type, word_table[index][0])
                    item1 = QtWidgets.QTableWidgetItem('ERROR')
                    self.tableStack.setItem(layer_stack - 1, 0, item1)
                    break

    def obtain_con(self, stack):
        res = []
        for item in stack:
            res.append(item)
        return res

    def onClick_analyze_stack_2(self):
        test = Predictive_Analysis()
        grammar = ""
        if self.choice == 0:
            text = self.textEdit.toPlainText()
            lines = text.splitlines(True)
            res = ""
            for line in lines:
                print(line.rstrip('\r\n'))
                line = line.rstrip()
                new_s = line[0]
                for i in range(1, len(line)):
                    if line[i] != ' ' and line[i - 1] != ' ':
                        new_s += ' '
                    new_s += line[i]
                print(new_s)
                res += new_s.strip() + '\n'
            print(res)
            grammar = res.replace(' - > ', ':')
            grammar = grammar.replace(' | ', '|')
        elif self.choice == 1:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')
        test.input(grammar)
        VN = test.vn
        VT = test.vt
        self.predict_table = test.predict_table
        self.predict_table_ = test.predict_table_
        # 获取输入串并加入‘#’结束标志
        layer_stack = 0
        # 先设置 table层数为1 后 动态增加
        self.tableStack.setRowCount(layer_stack)
        analyze_str = self.textEdit_1.toPlainText()
        analyze_str += '#'
        print('09999999999999999999999')
        print(analyze_str)
        stack = []
        index = 0
        stack.append('#')
        stack.append(test.begin)

        while len(stack) != 0:
            # 层数增加一层
            layer_stack = layer_stack + 1
            self.tableStack.setRowCount(layer_stack)
            cur = stack.pop()
            if cur == "#" and len(stack) == 0:
                print("符号栈：", self.obtain_con(stack), "\n匹配字符: ", '#')
                item1 = QtWidgets.QTableWidgetItem(str(self.obtain_con(stack)))
                self.tableStack.setItem(layer_stack - 1, 0, item1)

                item1 = QtWidgets.QTableWidgetItem(str(analyze_str[index]))
                self.tableStack.setItem(layer_stack - 1, 2, item1)

                print("分析完成")
                break
            elif cur in VT:
                a = analyze_str[index]
                if a == cur:
                    print("符号栈：", self.obtain_con(stack), "\n匹配字符: ", analyze_str[index])
                    item1 = QtWidgets.QTableWidgetItem(str(self.obtain_con(stack)))
                    self.tableStack.setItem(layer_stack - 1, 0, item1)

                    item1 = QtWidgets.QTableWidgetItem(str(analyze_str[index]))
                    self.tableStack.setItem(layer_stack - 1, 2, item1)
                    index += 1
                    if index >= len(analyze_str):
                        index -= 1
                else:
                    print("分析错误")
                    item1 = QtWidgets.QTableWidgetItem('ERROR')
                    self.tableStack.setItem(layer_stack - 1, 0, item1)
                    break

            else:
                a = analyze_str[index]
                if a in self.predict_table[cur]:
                    if self.predict_table[cur][a] == "$":
                        print("\n符号栈：", self.obtain_con(stack), "\n产生式: ", cur, "->",
                              self.predict_table[cur][a])
                        item1 = QtWidgets.QTableWidgetItem(str(self.obtain_con(stack)))
                        self.tableStack.setItem(layer_stack - 1, 0, item1)

                        item1 = QtWidgets.QTableWidgetItem(str(self.predict_table_[cur][a]))
                        self.tableStack.setItem(layer_stack - 1, 1, item1)
                        continue
                    next_epr = self.predict_table[cur][a].split()

                    print("\n符号栈：", self.obtain_con(stack), "\n产生式: ", cur, "->",
                          self.predict_table[cur][a])
                    item1 = QtWidgets.QTableWidgetItem(str(self.obtain_con(stack)))
                    self.tableStack.setItem(layer_stack - 1, 0, item1)

                    item1 = QtWidgets.QTableWidgetItem(str(self.predict_table_[cur][a]))
                    self.tableStack.setItem(layer_stack - 1, 1, item1)
                    node_list = []
                    """
                      产生式右部符号入栈,反序入栈
                      子节点入栈
                    """
                    for epr in next_epr:
                        node_list.append(epr)

                    node_list.reverse()
                    for nl in node_list:
                        stack.append(nl)
                else:
                    print("分析错误")
                    item1 = QtWidgets.QTableWidgetItem('ERROR')
                    self.tableStack.setItem(layer_stack - 1, 0, item1)
                    break

    def save_analyze_process(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存符号串的分析过程', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.tableStack.rowCount()):
                    for col in range(self.tableStack.columnCount()):
                        item = self.tableStack.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LL1GrammarSolver()
    window.show()
    sys.exit(app.exec_())
