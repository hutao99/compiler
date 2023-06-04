import sys
import Analyzer

from collection import FirstVTAndLastVT

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from suanfu_fist_ui import Ui_MainWindow_LL
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from TABLE import Predictive_Analysis

STACK = ['#']  # 输入栈

STACK_INPUT = []  # 剩余输入串

sentences = []


# 算符优先分析的进一步完善，添加了槽函数等
class MyDesiger_suanfu(Ui_MainWindow_LL, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_suanfu, self).__init__(parent)
        self.setWindowTitle("算符优先分析")
        self.setupUi(self)
        # 设置响应槽（信号源 conect 槽）
        self.pushButton_1.clicked.connect(self.open_text)
        self.pushButton_2.clicked.connect(self.grammar_analyse)
        self.pushButton.clicked.connect(self.onClick_analyze_stack)

    def onClick_analyze_stack(self):
        data = self.textEdit_2.toPlainText()
        g = FirstVTAndLastVT()
        g.input(data)
        sequence1, precedence_table1 = g.Table()
        sentences.clear()
        # 获得所输入框待分析的代码
        code = self.textEdit.toPlainText()
        print(code)
        lex = Analyzer.AnalyzerLex()
        lex.input(code)
        expression = [['', '#']]
        while True:
            tok = lex.token()
            if not tok:
                break
            expression.append([tok.type, tok.value])
        expression.append(['', '#'])
        stack_total, info = g.OP(sequence1, precedence_table1, expression)
        self.tableStack.setRowCount(len(stack_total) + 1)  # 设置层数
        # print(stack_total)
        layer = -1
        for stack in stack_total:
            print(stack)
            mystr = ""
            for value in stack:
                mystr += value
            print(mystr)
            item1 = QtWidgets.QTableWidgetItem(mystr)
            self.tableStack.setItem(layer, 1, item1)
            layer += 1
        print(info)
        item1 = QtWidgets.QTableWidgetItem(info)
        self.tableStack.setItem(layer, 1, item1)

    def grammar_analyse(self):
        data = self.textEdit_2.toPlainText()
        g = FirstVTAndLastVT()
        g.input(data)
        first_vt = 'FIRSTVT集合如下：\n'
        for key, value in g.first.items():
            first_vt += '{}: {}\n'.format(key, value)
        # 界面显示 first集
        self.textFirst_set.setPlainText(first_vt)

        # print(g.first)
        # print(g.last)
        text_followvt = 'LASTVT集合如下：\n'
        for key, value in g.last.items():
            text_followvt += '{}: {}\n'.format(key, value)

        self.textFollow_set.setPlainText(text_followvt)
        sequence1, precedence_table1 = g.Table()
        row = []
        for key, value in sequence1.items():
            row.append(key)
        # print(row)
        self.tableAnalyze.setColumnCount(len(row)+1)  # 设置列数
        self.tableAnalyze.setRowCount(len(row)+1)  # 设置行数

        for index, value in enumerate(row):
            self.tableAnalyze.setColumnWidth(index, 70)
            item = QtWidgets.QTableWidgetItem(value)
            self.tableAnalyze.setItem(0, index + 1, item)

        for i in range(len(row)):
            item1 = QtWidgets.QTableWidgetItem(row[i])
            self.tableAnalyze.setItem(i + 1, 0, item1)
            size = 1
            for relationship in precedence_table1[sequence1[row[i]]]:
                item1 = QtWidgets.QTableWidgetItem(relationship)
                self.tableAnalyze.setItem(i + 1, size, item1)
                size += 1

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/12OPG算符优先分析测试用例',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.textEdit_2.setText(text)

# app = QApplication(sys.argv)
# LL_window = MyDesiger_suanfu()
# LL_window.show()
# sys.exit(app.exec_())
