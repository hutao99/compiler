from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QComboBox, QDialog, QPushButton, \
    QHBoxLayout

import Analyzer
from collection import FirstVTAndLastVT
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox
import sys


def grammar_cut(grammar):
    non_terminals = set()
    terminals = set()
    for line in grammar.split('\n'):
        if line == '':
            continue
        lhs, rhs = line.split(':')
        non_terminals.add(lhs)
        for symbol in rhs:
            if symbol.isalpha() and symbol.islower():
                terminals.add(symbol)

    # 为每个符号添加空格
    for symbol in non_terminals.union(terminals):
        grammar = grammar.replace(symbol, f" {symbol} ")
    return grammar, non_terminals, terminals


class OPGGrammarSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个选项卡窗口部件
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.setWindowTitle("算符优先分析")
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.tabWidget.resize(800, 600)

        # 控制选项的变量
        self.chose_mode = '系统分词模式'

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
        self.pushButton.clicked.connect(self.get_VT)
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
        self.pushButton_2.clicked.connect(self.save_first)

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
        self.pushButton_3_.clicked.connect(self.save_follow)

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
        #保存FirstVT
        # self.pushButton_2.clicked.connect(self.save_first)
        #保存LastVT
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
        #显示算符优先分析表
        self.pushButton_3.clicked.connect(self.analyze_table)
        #保存算符优先分析表
        self.pushButton_3__.clicked.connect(self.save_analyze_table)
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
        self.pushButton_4.clicked.connect(self.analyze_sentence)

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

        self.tableStack.setColumnCount(4)

        # 设置tablewidget 栈分析表的表头
        self.tableStack.setHorizontalHeaderLabels(["符号栈", "缓冲区符号", "优先级", "动作"])
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
        self.pushButton_5_.clicked.connect(self.save_analyze_process)

    def on_mode_changed(self, index):
        # 处理用户选择的模式
        mode = self.mode_combo.currentText()
        self.chose_mode = mode
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

    def get_VT(self):
        grammar = self.textEdit.toPlainText()
        grammar = grammar.replace('->', ':')
        if self.chose_mode == '系统分词模式':
            grammar, non_terminals, terminals = grammar_cut(grammar)
        op = FirstVTAndLastVT()
        op.input(grammar)
        terminal = set()
        for i in op.first:
            terminal.update(op.first[i])
        for i in op.last:
            terminal.update(op.last[i])
        del op.first[op.begin+"'"]
        del op.last[op.begin + "'"]
        self.table_FIRST.setColumnCount(len(terminal))  # 设置列数
        self.table_FIRST.setRowCount(len(op.first))  # 设置行数
        self.table_FOLLOW.setColumnCount(len(terminal))  # 设置列数
        self.table_FOLLOW.setRowCount(len(op.first))  # 设置行数
        idx = 0
        print(op.first)
        print(op.last)
        for i in op.first:
            item1 = QtWidgets.QTableWidgetItem(i)
            self.table_FIRST.setVerticalHeaderItem(idx, item1)
            print(op.first[i])
            for j in range(len(op.first[i])):
                item = QtWidgets.QTableWidgetItem(op.first[i][j])
                self.table_FIRST.setItem(idx, j, item)
            idx += 1
        idx = 0
        for i in op.last:
            item1 = QtWidgets.QTableWidgetItem(i)
            self.table_FOLLOW.setVerticalHeaderItem(idx, item1)
            for j in range(len(op.last[i])):
                item = QtWidgets.QTableWidgetItem(op.last[i][j])
                self.table_FOLLOW.setItem(idx, j, item)
            idx += 1

    def analyze_table(self):
        self.tableAnalyze.clear()
        try:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')
            if self.chose_mode == '系统分词模式':
                grammar, non_terminals, terminals = grammar_cut(grammar)
            op = FirstVTAndLastVT()
            op.input(grammar)
            sequence1, precedence_table1, is_opg = op.Table()
            if not is_opg:
                QMessageBox.warning(self, '警告', '该文法非算符优先文法，请谨慎使用')
            self.tableAnalyze.setColumnCount(len(sequence1)+1)  # 设置列数
            self.tableAnalyze.setRowCount(len(sequence1)+1)  # 设置行
            idx = 1
            for i in sequence1:
                item = QtWidgets.QTableWidgetItem(i)
                self.tableAnalyze.setItem(0, idx, item)
                idx += 1
            idx = 1
            for i in sequence1:
                item = QtWidgets.QTableWidgetItem(i)
                self.tableAnalyze.setItem(idx, 0, item)
                idx += 1
            idx = 1
            for i in sequence1:
                for j in range(len(sequence1)):
                    item = QtWidgets.QTableWidgetItem(precedence_table1[sequence1[i]][j])
                    self.tableAnalyze.setItem(idx, j+1, item)
                idx += 1
            print(precedence_table1)
        except Exception as e:
            print("Error: ", e)

    def analyze_sentence(self):

        grammar = self.textEdit.toPlainText()
        grammar = grammar.replace('->', ':')
        text = self.textEdit_1.toPlainText()
        if self.chose_mode == '系统分词模式':
            grammar, non_terminals, terminals = grammar_cut(grammar)
            for symbol in non_terminals.union(terminals):
                text = text.replace(symbol, f" {symbol} ")
        op = FirstVTAndLastVT()
        op.input(grammar)
        sequence1, precedence_table1, is_opg = op.Table()
        if not is_opg:
            QMessageBox.warning(self, '警告', '该文法非算符优先文法，请谨慎分析语句')
        expression = ['#']
        expression.extend(text.split())
        expression.append('#')
        t = [[], [], [], []]
        t[0], info, t[3], t[1], t[2] = op.OP(sequence1, precedence_table1, expression)
        # stack, info, action, remainder, priority
        # self.tableStack.setColumnCount(4)  # 设置列数
        self.tableStack.setRowCount(len(t[0]) + 1)  # 设置行数
        for i in range(len(t[0])):
            for j in range(4):
                if len(t[j]) == i:
                    item = QtWidgets.QTableWidgetItem(info)
                    self.tableStack.setItem(len(t[0]), 0, item)
                    break
                p = str(t[j][i])
                item = QtWidgets.QTableWidgetItem(p)
                self.tableStack.setItem(i, j, item)
        '''except Exception as e:
            QMessageBox.warning(self, '警告', '句子中可能存在文法中没有的终结符')
            print("Error: ", e)'''

    def save_first(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存FirstVT集合', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.table_FIRST.rowCount()):
                    f.write(self.table_FIRST.verticalHeaderItem(row).text() + '\t')
                    for col in range(self.table_FIRST.columnCount()):
                        item = self.table_FIRST.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def save_follow(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存LastVT集合', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for row in range(self.table_FIRST.rowCount()):
                    f.write(self.table_FIRST.verticalHeaderItem(row).text() + '\t')
                    for col in range(self.table_FOLLOW.columnCount()):
                        item = self.table_FOLLOW.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def save_analyze_table(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存算符优先分析表', '', 'Text Files (*.txt)')
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

    def save_analyze_process(self):
        self.tableStack.clear()
        self.tableStack.setHorizontalHeaderLabels(["符号栈", "缓冲区符号", "优先级", "动作"])
        filename1, _ = QFileDialog.getSaveFileName(self, '保存分析过程', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                for col in range(self.tableStack.columnCount()):
                    header_item = self.tableStack.horizontalHeaderItem(col)
                    if header_item is not None:
                        f.write(header_item.text() + '\t')
                    else:
                        f.write('\t')
                f.write('\n')
                for row in range(self.tableStack.rowCount()):
                    for col in range(self.tableStack.columnCount()):
                        item = self.tableStack.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')


'''if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OPGGrammarSolver()
    window.show()
    sys.exit(app.exec_())'''
