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
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/NFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit.show()

    def nfa_to_dfa(self):
        self.dfa, self.final_states, self.input_symbols = self.my_object.nfa_to_dfa(self.nfa)
        f = open("DFA.txt")
        text = f.read()
        f.close()
        text1 = "DFA:\n" + text
        self.plainTextEdit_3.appendPlainText(text1)
        self.textEdit_2.clear()
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/DFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit_2.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit_2.show()

    def dfa_to_mfa(self):
        self.mfa, self.final_states = self.my_object.dfa_to_mfa(self.dfa, self.final_states, self.input_symbols)
        f = open("MFA.txt")
        text = f.read()
        f.close()
        text1 = "MFA:\n" + text
        self.plainTextEdit_3.appendPlainText(text1)
        self.textEdit_3.clear()
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./Reg_Graph/MFA.gv.png')
        # 在QTextEdit中插入图片
        cursor = self.textEdit_3.textCursor()
        cursor.insertImage(image_format)
        # 显示
        self.textEdit_3.show()

    # 全部展示
    def show_all(self):
        self.reg_to_nfa()
        self.nfa_to_dfa()
        self.dfa_to_mfa()


    def Lexical_Analysis(self):
        code = self.plainTextEdit_2.toPlainText()  # 获取用户输入代码
        result = REG.Lexical_Analysis(code, self.mfa, self.final_states)
        self.plainTextEdit_3.clear()
        print(result)
        text = "识别结果:\n"
        for value in result:
            text += value + "\n"
        self.plainTextEdit_3.appendPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    mainwindow = REG_MainWindow()
    # MainWindow = QMainWindow()  # 创建主窗口
    # ui = interface.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.resize(700, 800)
    # MainWindow.move(1100, 75)
    # 窗口宽高
    mainwindow.resize(850, 600)
    # 窗口左上角与屏幕左上角的相对坐标
    # mainwindow.move(1100, 75)
    mainwindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
