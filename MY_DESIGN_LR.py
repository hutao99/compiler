# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

from LR_UI import Ui_MainWindow_LR
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import LR_use_interface
from Analyzer import AnalyzerLex

class MyDesiger_LR(Ui_MainWindow_LR, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_LR, self).__init__(parent)
        self.LR = LR_use_interface.CLRParser()
        self.setWindowTitle("LR分析")
        self.setupUi(self)
        # 设置响应槽
        self.pushButton.clicked.connect(self.open_text)
        self.pushButton_1.clicked.connect(self.LR_image)
        self.pushButton_2.clicked.connect(self.LR_Table)
        self.pushButton_3.clicked.connect(self.LR_Analyse)

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/13LR分析测试用例',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.textEdit.clear()
            self.textEdit.setText(text)

    def LR_image(self):  # 画图
        text = self.textEdit.toPlainText()
        if len(text) != 0:
            self.LR.input(text)
            self.LR.Action_and_GoTo_Table()
            self.LR.draw_graphic()
            s = ''
            for i in range(1, len(self.LR.reduction)):
                s += 'r' + str(i) + '->' + self.LR.reduction[i] + '\n'

            self.textEdit_2.setText(s)

    def LR_Table(self):
        text = self.textEdit.toPlainText()
        if len(text) != 0:
            self.LR.input(text)
            self.LR.Action_and_GoTo_Table()
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
            self.tableStack.setColumnCount(len(terminal))  # 设置列数
            self.tableStack.setRowCount(row_count)  # 设置行数
            idx = {item: index for index, item in enumerate(terminal)}
            self.tableStack.setHorizontalHeaderLabels(terminal)
            for i in range(row_count):
                item1 = QtWidgets.QTableWidgetItem(str(i))
                self.tableStack.setVerticalHeaderItem(i, item1)
                for j in self.LR.parsing_table[i]:
                    item = QtWidgets.QTableWidgetItem(self.LR.parsing_table[i][j])
                    self.tableStack.setItem(i, idx[j], item)

    def LR_Analyse(self):
        self.tableStack1.clear()
        text = self.textEdit_3.toPlainText()
        if len(text) != 0:
            lex = AnalyzerLex()
            t = [[], [], [], []]
            if len(text) != 0:
                lex.input(text)
                tokens = []
                while True:
                    tok = lex.token()
                    if not tok:
                        break
                    tokens.append([tok.type, tok.value, tok.lineno,lex.find_column(tok.lexer.lexdata, tok)])
                tokens.append(['keyword', '#'])
                t[0], t[1], t[2], t[3], result = self.LR.ControlProgram(tokens)
                self.tableStack1.setColumnCount(4)  # 设置列数
                self.tableStack1.setRowCount(len(t[0])+1)  # 设置行数
                self.tableStack1.setHorizontalHeaderLabels(['状态栈', '符号栈', '剩余符号', '动作'])
            for i in range(len(t[0])):
                for j in range(4):
                    if len(t[j]) == i:
                        item = QtWidgets.QTableWidgetItem('错误')
                        self.tableStack1.setItem(len(t[0]), 0, item)
                        break
                    p = str(t[j][i])
                    if j == 3 and str(t[j][i]).isdigit():
                        p = 'goto ' + p
                    item = QtWidgets.QTableWidgetItem(p)
                    self.tableStack1.setItem(i, j, item)
