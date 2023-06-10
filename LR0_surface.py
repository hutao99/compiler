from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QPushButton, QLabel, QDialog, \
    QHBoxLayout, QScrollArea, QSizePolicy, QComboBox


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox
import sys
import LR0_use_interface

# lr0界面


def grammar_cut(grammar):
    non_terminals = set()
    terminals = set()
    print(grammar.split('\n'))
    for line in grammar.split('\n'):
        if line == '':
            continue
        print(line)
        lhs, rhs = line.split(':')
        lhs = lhs.replace(" ", "")
        non_terminals.add(lhs)
        for symbol in rhs:
            if symbol.isalpha() and symbol.islower():
                terminals.add(symbol)

    # 为每个符号添加空格
    for symbol in non_terminals.union(terminals):
        grammar = grammar.replace(symbol, f" {symbol} ")
    return grammar, non_terminals, terminals


class LR0GrammarSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个选项卡窗口部件
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.setWindowTitle("LR0分析")
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.tabWidget.resize(800, 600)

        # 控制选项的变量
        self.chose_mode = '系统分词模式'

        # LR1class实例化
        self.LR = LR0_use_interface.CLRParser()

        # 创建第一个选项卡
        self.tab1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab1, "LR状态信息")
        self.tab1.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

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

        # 创建第二个选项卡
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, "LR分析表")
        self.tab2.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 创建第三个选项卡
        self.tab3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab3, "测试案例")
        self.tab3.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 创建第四个选项卡
        self.tab4 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab4, "分析图")
        self.tab4.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 在分析图 tab 中添加 QLabel 和 QPixmap
        self.label = QLabel(self.tab4)
        pixmap = QPixmap('LR0_Digraph\LR_Digraph.gv.png')
        # label.setPixmap(pixmap)

        # 将 QLabel 放在 QVBoxLayout 中，并将 QVBoxLayout 设置为 self.tab4 的布局
        layout = QVBoxLayout(self.tab4)
        layout.addWidget(self.label)

        # 创建按钮，用于触发显示图片的操作
        button = QPushButton('显示图片', self.tab4)
        button_save = QPushButton('保存图片', self.tab4)
        button.clicked.connect(self.show_image)
        layout.addWidget(button)
        layout.addWidget(button_save)
        button_save.clicked.connect(lambda: self.save_image(pixmap))


        layout1 = QtWidgets.QGridLayout()

        # 导入LR文法的按钮
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
        self.pushButton.setText("LR文法分析")
        self.pushButton.setStyleSheet("QPushButton {text-align:left;}")
        self.pushButton.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())

        # 导入LR复杂文法的按钮
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
        self.pushButton_.setText("导入LR文法")
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
        self.pushButton_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_2.setText("显示状态信息")
        self.pushButton_2.clicked.connect(self.get_state)

        # 显示LR文法的内容
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        # 显示状态信息
        self.textEdit_state = QtWidgets.QTextEdit()
        self.textEdit_state.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.textEdit_state.setFont(font)
        self.textEdit_state.setObjectName("textEdit")

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
        self.pushButton_3_.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3_.setText("保存状态信息")

        # 将文法导入按钮和显示文法的文本框垂直布局
        buttonSplitter = QtWidgets.QSplitter(Qt.Vertical)
        buttonSplitter.addWidget(self.mode_combo)
        buttonSplitter.addWidget(self.pushButton_)
        buttonSplitter.addWidget(self.textEdit)
        buttonSplitter.addWidget(self.pushButton)

        # 将FIRST和FOLLOW集合求解按钮和显示的表格布局垂直布局
        textEditSplitter = QtWidgets.QSplitter(Qt.Vertical)
        textEditSplitter.addWidget(self.pushButton_2)
        textEditSplitter.addWidget(self.textEdit_state)
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

        # self.pushButton.clicked.connect(self.open_text)
        self.pushButton_.clicked.connect(self.open_text)
        # 显示状态信息
        # self.pushButton_2.clicked.connect(self.save_first)
        # 保存状态信息
        self.pushButton_3_.clicked.connect(self.save_state)

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
        self.pushButton_3.setText("LR分析表")
        self.pushButton_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3.clicked.connect(self.LR_Table)

        # 显示LR分析表的内容
        self.tableAnalyze = QtWidgets.QTableWidget()
        self.tableAnalyze.setObjectName("tableAnalyze")
        self.tableAnalyze.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        # 隐藏分析表的横纵表头
        #self.tableAnalyze.verticalHeader().setVisible(False)  # 隐藏垂直表头
        #self.tableAnalyze.horizontalHeader().setVisible(False)  # 隐藏水平表头

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
        self.pushButton_3__.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3__.setText("保存LR分析表")

        # 规约式
        self.pushButton_3__Statutory = QtWidgets.QPushButton()
        self.pushButton_3__Statutory.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3__Statutory.setFont(font)
        self.pushButton_3__Statutory.setObjectName("pushButton_3")
        self.pushButton_3__Statutory.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3__Statutory.setText("规约式")

        # 显示规约式的内容
        self.tableStatutory = QtWidgets.QTextEdit()
        self.tableStatutory.setObjectName("tableStatutory")
        self.tableStatutory.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        # 保存规约式
        self.pushButton_3__Statutory_ = QtWidgets.QPushButton()
        self.pushButton_3__Statutory_.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3__Statutory_.setFont(font)
        self.pushButton_3__Statutory_.setObjectName("pushButton_3__Statutory_")
        self.pushButton_3__Statutory_.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_3__Statutory_.setText("保存规约式")

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.pushButton_3)
        self.splitter2.addWidget(self.tableAnalyze)
        self.splitter2.addWidget(self.pushButton_3__)

        self.splitter2_ = QSplitter(Qt.Vertical)
        self.splitter2_.addWidget(self.pushButton_3__Statutory)
        self.splitter2_.addWidget(self.tableStatutory)
        self.splitter2_.addWidget(self.pushButton_3__Statutory_)

        self.splitter2__ = QSplitter(Qt.Horizontal)
        self.splitter2__.addWidget(self.splitter2)
        self.splitter2__.addWidget(self.splitter2_)

        layout2.addWidget(self.splitter2__)

        self.tab2.setLayout(layout2)
        size = self.pushButton_2.minimumSizeHint()
        self.pushButton_3.setFixedHeight(size.height())
        self.pushButton_3__.setFixedHeight(size.height())
        self.pushButton_3__Statutory.setFixedHeight(size.height())
        self.pushButton_3__Statutory_.setFixedHeight(size.height())

        # 显示LR分析表
        # self.pushButton_3.clicked.connect(self.analyze_table)
        # 保存LR分析表
        self.pushButton_3__.clicked.connect(self.save_analyze_table)
        # 显示规约式
        # self.pushButton_3__Statutory.clicked.connect(self.analyze_table)
        # 保存规约式
        self.pushButton_3__Statutory_.clicked.connect(self.save_reduction)

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
        self.pushButton_4.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_4.setText("分析过程")
        self.pushButton_4.clicked.connect(self.LR_Analyse)

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
        self.pushButton_5.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_5.setText("打开测试案例或手动输入")

        # 显示分析过程
        self.tableStack = QtWidgets.QTableWidget()
        self.tableStack.setObjectName("tableStack")
        self.tableStack.setStyleSheet('QWidget{background-color:%s}' % QColor("#FFFFFF").name())

        self.tableStack.setColumnCount(4)

        # 设置tablewidget 栈分析表的表头
        self.tableStack.setHorizontalHeaderLabels(['状态栈', '符号栈', '剩余符号', '动作'])
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
        self.pushButton_5_.setStyleSheet('QWidget{background-color:%s}' % QColor("#CCCCCC").name())
        self.pushButton_5_.setText("保存LR分析过程")

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
        # 保存LR分析过程
        self.pushButton_5_.clicked.connect(self.save_analyze_process)

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
    def on_mode_changed(self, index):
        # 处理用户选择的模式
        mode = self.mode_combo.currentText()
        self.chose_mode = mode
        print("当前模式：", mode)

    def show_image(self):
        '''
        :return:显示图片
        '''
         # 创建 QDialog，并将它设置为模态对话框
        '''dialog = QDialog(self)
        dialog.setModal(True)
        # 在 QDialog 中添加 QLabel 和 QPixmap
        label = QLabel(dialog)'''
        grammar = self.textEdit.toPlainText()
        if len(grammar) != 0:
            try:
                grammar = grammar.replace('->', ':')
                if self.chose_mode == '系统分词模式':
                    grammar, non_terminals, terminals = grammar_cut(grammar)
                self.LR.input(grammar)
                self.LR.Action_and_GoTo_Table()
                self.LR.draw_graphic()
                pixmap = QPixmap('LR0_Digraph\LR_Digraph.gv.png')
                self.label.setPixmap(pixmap)
            except Exception as e:
                QMessageBox.warning(self, '警告', '系统出错')
                print("Error: ", e)
        # 调整 QDialog 的大小，并显示它
        '''dialog.setWindowTitle('分析图')
        dialog.resize(pixmap.width(), pixmap.height())
        dialog.show()'''

    def save_image(self, pixmap):
        # 弹出文件对话框，让用户选择保存的文件名和路径
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getSaveFileName(self, "保存图片", "", "JPEG (*.jpg);;PNG (*.png)", options=options)
        # 如果用户选择了文件名和路径，则保存图片到本地
        if file_name:
            # 从过滤器中获取文件类型后缀
            file_types = ('JPEG (*.jpg)', 'PNG (*.png)')
            file_exts = ('.jpg', '.png')
            idx = file_types.index(selected_filter)
            file_ext = file_exts[idx]
            if not file_name.endswith(file_ext):
                file_name += file_ext

            pixmap.save(file_name)

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

    def LR_image(self):  # 画图
        grammar = self.textEdit.toPlainText()
        if len(grammar) != 0:
            try:
                grammar = grammar.replace('->', ':')
                if self.chose_mode == '系统分词模式':
                    grammar, non_terminals, terminals = grammar_cut(grammar)
                self.LR.input(grammar)
                self.LR.Action_and_GoTo_Table()
                self.LR.draw_graphic()
            except Exception as e:
                QMessageBox.warning(self, '警告', '系统出错')
                print("Error: ", e)

    def LR_Table(self):
        self.tableAnalyze.clear()
        grammar = self.textEdit.toPlainText()
        if len(grammar) != 0:
            try:
                grammar = grammar.replace('->', ':')
                if self.chose_mode == '系统分词模式':
                    grammar, non_terminals, terminals = grammar_cut(grammar)
                self.LR.input(grammar)
                is_lr = self.LR.Action_and_GoTo_Table()
                if not is_lr:
                    QMessageBox.warning(self, '警告', '该文法不为lr(0)文法，请谨慎使用')
                row_count = len(self.LR.parsing_table)
                # 非终结符
                non_terminal = list(self.LR.first.keys())
                # 终结符
                terminal = set()
                for i in self.LR.direction:
                    if i[1] not in non_terminal:
                        terminal.add(i[1])
                terminal = list(terminal)
                terminal.append('#')
                terminal.extend(non_terminal)  # 融合
                print(terminal)
                self.tableAnalyze.setColumnCount(len(terminal))  # 设置列数
                self.tableAnalyze.setRowCount(row_count)  # 设置行数
                idx = {item: index for index, item in enumerate(terminal)}
                self.tableAnalyze.setHorizontalHeaderLabels(terminal)
                print(self.LR.parsing_table)
                for i in range(row_count):
                    item1 = QtWidgets.QTableWidgetItem(str(i))
                    self.tableAnalyze.setVerticalHeaderItem(i, item1)
                    for j in self.LR.parsing_table[i]:
                        item = QtWidgets.QTableWidgetItem(self.LR.parsing_table[i][j])
                        self.tableAnalyze.setItem(i, idx[j], item)
                s = ''
                for i in range(0, len(self.LR.reduction)):
                    s += 'r' + str(i) + '->' + self.LR.reduction[i] + '\n'
                self.tableStatutory.setText(s)
            except Exception as e:
                QMessageBox.warning(self, '警告', '系统出错')
                print("Error: ", e)

    def LR_Analyse(self):
        self.tableStack.clear()
        self.tableStack.setHorizontalHeaderLabels(['状态栈', '符号栈', '剩余符号', '动作'])
        grammar = self.textEdit.toPlainText()
        text = self.textEdit_1.toPlainText()
        if len(self.LR.parsing_table) != 0:
            try:
                grammar = grammar.replace('->', ':')
                if self.chose_mode == '系统分词模式':
                    grammar, non_terminals, terminals = grammar_cut(grammar)
                    for symbol in non_terminals.union(terminals):
                        text = text.replace(symbol, f" {symbol} ")
                self.LR.input(grammar)
                is_lr, lab = self.LR.Action_and_GoTo_Table()
                if not is_lr:
                    QMessageBox.warning(self, '警告', '该文法不为lr(0)文法，请谨慎使用')
                t = [[], [], [], []]
                t[0], t[1], t[2], t[3], result = self.LR.ControlProgram(text.split())
                self.tableStack.setRowCount(len(t[0])+1)  # 设置行数
                self.tableStack.setHorizontalHeaderLabels(['状态栈', '符号栈', '剩余符号', '动作'])
                for i in range(len(t[0])):
                    for j in range(4):
                        if len(t[j]) == i:
                            item = QtWidgets.QTableWidgetItem('错误')
                            self.tableStack.setItem(len(t[0]), 0, item)
                            break
                        p = str(t[j][i])
                        if j == 3 and str(t[j][i]).isdigit():
                            p = 'goto ' + p
                        item = QtWidgets.QTableWidgetItem(p)
                        self.tableStack.setItem(i, j, item)
            except Exception as e:
                QMessageBox.warning(self, '警告', '系统出错')
                print("Error: ", e)

    def get_state(self):
        try:
            grammar = self.textEdit.toPlainText()
            grammar = grammar.replace('->', ':')
            if self.chose_mode == '系统分词模式':
                grammar, non_terminals, terminals = grammar_cut(grammar)
            self.LR.input(grammar)
            is_lr, lab = self.LR.Action_and_GoTo_Table()
            if not is_lr:
                QMessageBox.warning(self, '警告', '该文法不为lr(0)文法，请谨慎使用')
            self.textEdit_state.setText(lab)
        except Exception as e:
            QMessageBox.warning(self, '警告', '系统出错')

    def save_state(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存状态集合', '', 'Text Files (*.txt)')
        text = self.textEdit_state.toPlainText()
        if filename1:
            with open(filename1, 'w') as f:
                f.write(text)

    def save_analyze_table(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存LR1分析表', '', 'Text Files (*.txt)')
        if filename1:
            with open(filename1, 'w') as f:
                f.write('\t')
                for col in range(self.tableAnalyze.columnCount()):
                    header_item = self.tableAnalyze.horizontalHeaderItem(col)
                    if header_item is not None:
                        f.write(header_item.text() + '\t')
                    else:
                        f.write('\t')
                f.write('\n')
                for row in range(self.tableAnalyze.rowCount()):
                    f.write(self.tableAnalyze.verticalHeaderItem(row).text() + '\t')
                    for col in range(self.tableAnalyze.columnCount()):
                        item = self.tableAnalyze.item(row, col)
                        if item is not None:
                            f.write(item.text() + '\t')
                        else:
                            f.write('\t')
                    f.write('\n')

    def save_reduction(self):
        filename1, _ = QFileDialog.getSaveFileName(self, '保存LR1分析表', '', 'Text Files (*.txt)')
        if filename1:
            text = self.tableStatutory.toPlainText()
            with open(filename1, 'w') as f:
                f.write(text)

    def save_analyze_process(self):
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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = LR0GrammarSolver()
#     window.show()
#     sys.exit(app.exec_())
