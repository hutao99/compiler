import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from REG_interface import Ui_MainWindow_REG
import REG


class REG_MainWindow(Ui_MainWindow_REG, QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow_REG, self).__init__(parent)
        self.setupUi(self)
        self.action_NFA.triggered.connect(self.reg_to_nfa)
        self.actionNFA_DFA.triggered.connect(self.nfa_to_dfa)
        self.actionDFA_MFA.triggered.connect(self.dfa_to_mfa)
        self.action_6.triggered.connect(self.Lexical_Analysis)
        self.action_7.triggered.connect(self.show_all)

        self.my_object = None
        self.nfa = []
        self.dfa = []
        self.mfa = []
        self.final_states = []
        self.input_symbols = []

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
        self.plainTextEdit_2.clear()
        f = open("NFA.txt")
        text = f.read()
        f.close()
        self.plainTextEdit_2.appendPlainText(text)

    def nfa_to_dfa(self):
        self.dfa, self.final_states, self.input_symbols = self.my_object.nfa_to_dfa(self.nfa)
        self.plainTextEdit_3.clear()
        f = open("DFA.txt")
        text = f.read()
        f.close()
        self.plainTextEdit_3.appendPlainText(text)

    def dfa_to_mfa(self):
        self.mfa, self.final_states = self.my_object.dfa_to_mfa(self.dfa, self.final_states, self.input_symbols)
        self.plainTextEdit_4.clear()
        f = open("MFA.txt")
        text = f.read()
        f.close()
        self.plainTextEdit_4.appendPlainText(text)

    # 全部展示
    def show_all(self):
        self.reg_to_nfa()
        self.nfa_to_dfa()
        self.dfa_to_mfa()


    def Lexical_Analysis(self):
        code = self.plainTextEdit.toPlainText()  # 获取用户输入代码
        result = REG.Lexical_Analysis(code, self.mfa, self.final_states)
        self.plainTextEdit_2.clear()
        print(result)
        text = ""
        for value in result:
            text += value + "\n"
        self.plainTextEdit_2.appendPlainText(text)

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
