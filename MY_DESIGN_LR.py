# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

from LR_UI import Ui_MainWindow_LR
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import LR
from Analyzer import AnalyzerLex

class MyDesiger_LR(Ui_MainWindow_LR, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_LR, self).__init__(parent)
        self.LR = LR.CLRParser()
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
            # 设置图片路径
            image_format = QtGui.QTextImageFormat()
            image_format.setName('./LR_Digraph/LR_Digraph.gv.png')

            # 在QTextEdit中插入图片
            self.textEdit_2.clear()
            cursor = self.textEdit_2.textCursor()
            cursor.insertImage(image_format)

            self.textEdit_2.show()

    def LR_Table(self):
        row_count = len(self.LR.parsing_table)
        col_count = max(len(v) for v in self.LR.parsing_table.values())

        # 非终结符
        non_terminal = list(self.LR.first.keys())
        # 终结符
        terminal = set()
        for i in self.LR.direction:
            if i[1] not in non_terminal:
                terminal.add(i[1])
        terminal = list(terminal)
        terminal.append('#')

        self.tableStack.setColumnCount(col_count+2)  # 设置列数
        self.tableStack.setRowCount(row_count)  # 设置行数
        print(self.LR.parsing_table)
        terminal.extend(non_terminal)  # 融合
        print(terminal)
        idx = {item: index for index, item in enumerate(terminal)}
        self.tableStack.setHorizontalHeaderLabels(terminal)
        for i in range(row_count):
            for j in self.LR.parsing_table[i]:
                t = self.LR.parsing_table[i][j]
                if t.isdigit():
                    t = str(int(t)+1)
                item = QtWidgets.QTableWidgetItem(t)
                self.tableStack.setItem(i, idx[j], item)

    def LR_Analyse(self):
        '''text = self.textEdit.toPlainText()
        lex.input(text)
        tokens = []
        while True:
            tok = lex.token()
            if not tok:
                break
            tokens.append([tok.type, tok.value, tok.lineno,
                           lex.find_column(tok.lexer.lexdata, tok)])
        tokens.append(['keyword', '#'])
        self.LR.ControlProgram(tokens)'''
        self.tableStack1.setColumnCount(2)  # 设置列数
        self.tableStack1.setRowCount(2)  # 设置行数
