import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui, QtCore, QtWidgets

from REG_interface import Ui_MainWindow
import REG


class REG_MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.action_6.triggered.connect(self.reg_to_nfa)
        self.actionNFA_DFA_2.triggered.connect(self.nfa_to_dfa)
        self.actionDFA_MFA_2.triggered.connect(self.dfa_to_mfa)
        self.action_8.triggered.connect(self.show_all)
        # 词法分析
        self.action_9.triggered.connect(self.Lexical_Analysis)
        # 打开正规式文件
        self.action_7.triggered.connect(self.open_file)
        # 打开待输入符号串文件
        self.action_10.triggered.connect(self.open_file1)
        # 按钮
        self.pushButton.clicked.connect(self.open_nfa)
        self.pushButton_2.clicked.connect(self.open_dfa)
        self.pushButton_3.clicked.connect(self.open_mfa)

        self.my_object = None
        self.nfa = []
        self.dfa = []
        self.mfa = []
        self.final_states = []
        self.input_symbols = []

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/10REG正则表达式转换', '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.plainTextEdit.clear()
            self.plainTextEdit.setPlainText(text)

    def open_file1(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/10REG正则表达式转换',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.plainTextEdit_2.clear()
            self.plainTextEdit_2.setPlainText(text)

    def reg_to_nfa(self):
        reg = self.plainTextEdit.toPlainText()  # 获取用户输入的正规式
        if "\n" in reg:    # 多个正规式
            text = reg.split("\n")
            # 方法1 自己把每行的正规式套上一个（）合并成一个正规式
            reg = ""
            for index, value in enumerate(text):
                print(value)
                if index < len(text) - 1:
                    reg += "(" + value + ")|"
                else:
                    reg += "(" + value + ")"

        self.my_object = REG.NfaDfaMfa(reg)
        self.nfa = self.my_object.reg_to_nfa()
        self.plainTextEdit_3.clear()
        f = open("NFA.txt")
        text = f.read()
        f.close()
        text1 = "NFA:\n" + text
        self.plainTextEdit_3.appendPlainText(text1)
        self.textEdit.clear()
        self.textEdit.append("NFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/NFA.gv.png')
        # 在TextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()

    def nfa_to_dfa(self):
        nfa = self.plainTextEdit.toPlainText()
        if "起始状态" in nfa:
            final_nfa = []
            nfa = nfa.split("\n")
            for index, value in enumerate(nfa):
                if index < 1:   # 跳过 起始状态 接收状态 结束状态这一行
                    continue
                else:
                    arc = []
                    for value1 in value:
                        if value1 != '\t':
                            if value1.isdigit():
                                arc.append(int(value1))
                            else:
                                arc.append(value1)
                    if len(arc) > 0:
                        final_nfa.append(arc)
            my_object = REG.NfaDfaMfa("")
            dfa, final_states, input_symbols = my_object.nfa_to_dfa(final_nfa)

        self.dfa, self.final_states, self.input_symbols = self.my_object.nfa_to_dfa(self.nfa)
        f = open("DFA.txt")
        text = f.read()
        f.close()
        text1 = "DFA:\n" + text
        self.plainTextEdit_3.appendPlainText(text1)
        self.textEdit.clear()
        self.textEdit.append("DFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/DFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()

    def dfa_to_mfa(self):
        self.mfa, self.final_states = self.my_object.dfa_to_mfa(self.dfa, self.final_states, self.input_symbols)
        f = open("MFA.txt")
        text = f.read()
        f.close()
        text1 = "MFA:\n" + text
        self.plainTextEdit_3.appendPlainText(text1)
        self.textEdit.clear()
        self.textEdit.append("MFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/MFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()

    # 全部展示
    def show_all(self):
        self.reg_to_nfa()
        self.nfa_to_dfa()
        self.dfa_to_mfa()

    def open_nfa(self):
        self.textEdit.clear()
        self.textEdit.append("NFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/NFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()
    def open_dfa(self):
        self.textEdit.clear()
        self.textEdit.append("DFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/DFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()
    def open_mfa(self):
        self.textEdit.clear()
        self.textEdit.append("MFA:\n")
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/MFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()

    def Lexical_Analysis(self):
        code = self.plainTextEdit_2.toPlainText()  # 获取用户输入代码
        result = REG.Lexical_Analysis(code, self.mfa, self.final_states)
        self.plainTextEdit_3.clear()
        print(result)
        text1 = "符合输入正规式的单词:\n"
        text2 = "不符合输入正规式的单词:\n"
        for value in result:
            if value[len(value)-4: len(value)] == "识别成功":
                text1 += value[0: len(value)-4] + "\n"
            elif value[len(value)-4: len(value)] == "识别错误":
                text2 += value[0: len(value)-4] + "\n"
        self.plainTextEdit_3.appendPlainText(text1)
        self.plainTextEdit_3.appendPlainText(text2)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    mainwindow = REG_MainWindow()
    # 窗口宽高
    mainwindow.resize(1033, 837)
    # 窗口左上角与屏幕左上角的相对坐标
    # mainwindow.move(1100, 75)
    mainwindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
