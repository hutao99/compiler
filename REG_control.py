import os
import sys

import numpy as np
from PIL.Image import Image
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
import matplotlib.image as img
from matplotlib import pyplot as plt

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
        # 打开NFA或DFA文件
        self.action_13.triggered.connect(self.open_file2)
        # 按钮
        self.pushButton.clicked.connect(self.open_nfa)
        self.pushButton_2.clicked.connect(self.open_dfa)
        self.pushButton_3.clicked.connect(self.open_mfa)
        # 单独转换
        self.action_NFA_DFA.triggered.connect(self.nfa_to_dfa2)
        self.action_DFA_MFA_2.triggered.connect(self.dfa_to_mfa2)
        # 导出文件
        self.action_NFA_2.triggered.connect(self.save_nfa)
        self.action_DFA.triggered.connect(self.save_dfa)
        self.action_MFA.triggered.connect(self.save_mfa)
        self.action_11.triggered.connect(self.save_nfa_graph)
        self.action_DFA_2.triggered.connect(self.save_dfa_graph)
        self.action_MFA_2.triggered.connect(self.save_mfa_graph)
        self.action_12.triggered.connect(self.save_all)



        self.my_object = None
        self.nfa = []
        self.dfa = []
        self.mfa = []
        self.final_states = []
        self.input_symbols = []
        self.text = ""

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/03REG正则表达式转换测试用例/正则表达式及其对应测试用例/', '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.plainTextEdit.clear()
            self.plainTextEdit.setPlainText(text)

    def open_file1(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/03REG正则表达式转换测试用例/正则表达式及其对应测试用例/',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.plainTextEdit_2.clear()
            self.plainTextEdit_2.setPlainText(text)

    def open_file2(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开文件',
                                              './全部测试程序/03REG正则表达式转换测试用例/NFA和DFA/',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.plainTextEdit.clear()
            self.plainTextEdit.setPlainText(text)


    def reg_to_nfa(self):
        reg = self.plainTextEdit.toPlainText()  # 获取用户输入的正规式
        if reg == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        elif '#' in reg:
            QMessageBox.warning(self, '警告', '正规式中不能含有#')
        elif "状态" in reg or "节点" in reg:
            QMessageBox.warning(self, '警告', '请输入合法的正规式')
        else:
            try:
                my_dir = {}
                if '%' in reg:
                    setting = reg[reg.find('%') + 2: reg.rfind('%') - 1]
                    reg = reg[reg.rfind('%')+2:]
                    while True:
                        name = setting[0: setting.find('[')]
                        value = setting[setting.find('[') + 1: setting.find(']')]
                        value1 = []
                        for char in value:
                            if char != ',':
                                value1.append(char)
                        my_dir[name] = value1
                        if '\n' in setting:
                            setting = setting[setting.find('\n')+1: len(setting)]
                        else:
                            break
                self.text = reg
                if "\n" in reg:    # 多个正规式
                    text = reg.split("\n")
                    # 方法1 自己把每行的正规式套上一个（）合并成一个正规式
                    reg = ""
                    for index, value in enumerate(text):
                        if index < len(text) - 1:
                            reg += "(" + value + ")|"
                        else:
                            reg += "(" + value + ")"
                for key, value in my_dir.items():
                    while key in reg:
                        repalce = ""
                        for value2 in my_dir[key]:
                            repalce += value2 + "|"
                        repalce = "(" + repalce[0: len(repalce) - 1] + ")"
                        start = reg.find(key)
                        final_reg = reg[0: start]
                        final_reg += repalce
                        final_reg += reg[start + len(key):]
                        reg = final_reg

                self.my_object = REG.NfaDfaMfa(reg, my_dir)
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
            except:
                QMessageBox.warning(self, '警告', '系统无法处理')

    def nfa_to_dfa(self):
        nfa = self.plainTextEdit.toPlainText()
        if nfa == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        else:
            if len(self.nfa) == 0:
                QMessageBox.warning(self, '警告', '请先点击正规式转为NFA')
            else:
                try:
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
                except:
                    QMessageBox.warning(self, '警告', '系统无法处理')
    def dfa_to_mfa(self):
        dfa = self.plainTextEdit.toPlainText()
        if dfa == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        elif len(self.dfa) == 0:
            QMessageBox.warning(self, '警告', '请先点击NFA转DFA')
        else:
            try:
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
            except:
                QMessageBox.warning(self, '警告', '系统无法处理')

    # 全部展示
    def show_all(self):
        code = self.plainTextEdit.toPlainText()
        if code == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        else:
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
        if code == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        else:
            if len(self.mfa) == 0:
                QMessageBox.warning(self, '警告', '请先输入正规式进行一键三连')
            else:
                try:
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
                except:
                    QMessageBox.warning(self, '警告', '系统无法处理')

    def nfa_to_dfa2(self):
        nfa = self.plainTextEdit.toPlainText()
        if nfa == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        else:
            if "状态" not in nfa or "节点" not in nfa:
                QMessageBox.warning(self, '警告', '请输入正确的NFA形式')
            else:
                try:
                    final_nfa = []
                    nfa = nfa.split("\n")
                    for index, value in enumerate(nfa):
                        if "状态" in value or "节点" in value:
                            continue
                        else:
                            arc = []
                            for value1 in value:
                                if value1 not in ['\t', ' ']:
                                    if value1.isdigit():
                                        arc.append(int(value1))
                                    else:
                                        arc.append(value1)
                            if len(arc) > 0:
                                final_nfa.append(arc)
                    my_object = REG.NfaDfaMfa("",{})
                    dfa, final_states, input_symbols = my_object.nfa_to_dfa(final_nfa)
                    f = open("DFA.txt")
                    text = f.read()
                    f.close()
                    text1 = "DFA:" + text
                    self.plainTextEdit_3.clear()
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
                except:
                    QMessageBox.warning(self, '警告', '系统无法处理')
    def dfa_to_mfa2(self):
        dfa = self.plainTextEdit.toPlainText()
        if dfa == '':
            QMessageBox.warning(self, '警告', '请在输入框输入代码或打开文件')
        else:
            if "状态" not in dfa or "节点" not in dfa:
                QMessageBox.warning(self, '警告', '请输入正确的DFA形式')
            else:
                try:
                    final_dfa = []
                    final_states = []
                    input_symbols = []
                    dfa = dfa.split("\n")
                    print(dfa)
                    for index, value in enumerate(dfa):
                        if "状态" in value or "初始节点" in value:
                            continue
                        elif "终结节点" in value:
                            for state in value:
                                if state.isdigit():
                                    final_states.append(int(state))
                        else:
                            arc = []
                            for value1 in value:
                                if value1 not in ['\t', ' ']:
                                    if value1.isdigit():
                                        arc.append(int(value1))
                                    else:
                                        arc.append(value1)
                                        if value1 != 'ε':
                                            input_symbols.append(value1)
                            if len(arc) > 0:
                                final_dfa.append(arc)
                    my_object = REG.NfaDfaMfa("",{})
                    mfa, final_states = my_object.dfa_to_mfa(final_dfa, final_states, input_symbols)
                    f = open("MFA.txt")
                    text = f.read()
                    f.close()
                    text1 = "MFA:" + text
                    self.plainTextEdit_3.clear()
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
                except:
                    QMessageBox.warning(self, '警告', '系统无法处理')

    def save_nfa(self):
        filename = 'NFA.txt'
        self.file_save_as(filename)

    def save_dfa(self):
        filename = 'DFA.txt'
        self.file_save_as(filename)

    def save_mfa(self):
        filename = 'MFA.txt'
        self.file_save_as(filename)

    def save_nfa_graph(self):
        filename = './Reg_Graph/NFA.gv.png'
        image = cv2.imread(filename)
        if image is None:
            QMessageBox.warning(self, '警告', '请先生成对应图片')
        else:
            # 获取保存路径
            path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '所有文件 (*.png)')
            if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
                """
                原因：cv2读取彩色图片通道顺序为B、G、R，PIL显示图片是R、G、B顺序，因此读出来图片颜色会改变，需要对图像通道进行调序。
                """
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path, image)

    def save_dfa_graph(self):
        filename = './Reg_Graph/DFA.gv.png'
        image = cv2.imread(filename)
        if image is None:
            QMessageBox.warning(self, '警告', '请先生成对应图片')
        else:
            # 获取保存路径
            path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '所有文件 (*.png)')
            if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
                """
                原因：cv2读取彩色图片通道顺序为B、G、R，PIL显示图片是R、G、B顺序，因此读出来图片颜色会改变，需要对图像通道进行调序。
                """
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path, image)

    def save_mfa_graph(self):
        filename = './Reg_Graph/MFA.gv.png'
        image = cv2.imread(filename)
        if image is None:
            QMessageBox.warning(self, '警告', '请先生成对应图片')
        else:
            # 获取保存路径
            path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '所有文件 (*.png)')
            if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
                """
                原因：cv2读取彩色图片通道顺序为B、G、R，PIL显示图片是R、G、B顺序，因此读出来图片颜色会改变，需要对图像通道进行调序。
                """
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path, image)

    def save_all(self):
        if cv2.imread('./Reg_Graph/NFA.gv.png') is None or cv2.imread('./Reg_Graph/DFA.gv.png') is None or cv2.imread(
                './Reg_Graph/MFA.gv.png') is None:
            QMessageBox.warning(self, '警告', '请先生成全部状态转换图')
        elif not os.path.exists('NFA.txt') or not os.path.exists('DFA.txt') or not os.path.exists('MFA.txt'):
            QMessageBox.warning(self, '警告', '请先生成全部文件')
        else:
            path, _ = QFileDialog.getSaveFileName(self, '保存文件', '')
            if os.path.exists(path):
                QMessageBox.warning(self, '警告', '该文件夹已存在')
            elif path != '':   # 解决未选择文件卡死的问题:
                os.mkdir(path)
                path1 = path + '/NFA.txt'
                text = str(open("MFA.txt").read())  # 从文件中读入数据并强转为字符串类型
                with open(path1, 'w') as f:
                    f.write(text)

                filename = './Reg_Graph/NFA.gv.png'
                path1 = path + '/NFA.gv.png'
                image = cv2.imread(filename)
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path1, image)

                path1 = path + '/DFA.txt'
                text = str(open("DFA.txt").read())  # 从文件中读入数据并强转为字符串类型
                with open(path1, 'w') as f:
                    f.write(text)

                filename = './Reg_Graph/DFA.gv.png'
                path1 = path + '/DFA.gv.png'
                image = cv2.imread(filename)
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path1, image)

                path1 = path + '/MFA.txt'
                text = str(open("MFA.txt").read())  # 从文件中读入数据并强转为字符串类型
                with open(path1, 'w') as f:
                    f.write(text)

                filename = './Reg_Graph/MFA.gv.png'
                path1 = path + '/MFA.gv.png'
                image = cv2.imread(filename)
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                img.imsave(path1, image)

    def file_save_as(self, filename):
        if os.path.exists(filename):
            path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '所有文件 (*.txt)')
            if not path:
                return
            if path != '':   # 解决未选择文件卡死的问题
                self.savePath(path, filename)
        else:
            QMessageBox.warning(self, '警告', '请先生成对应文件')

    def savePath(self, path, filename):
        text = str(open(filename).read())  # 从文件中读入数据并强转为字符串类型
        with open(path, 'w') as f:
            f.write(text)
    def closeEvent(self, event):
        # 弹出消息框
        reply = QMessageBox.question(self, '确认', '确定要退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    mainwindow = REG_MainWindow()
    # 窗口宽高
    mainwindow.resize(1033, 837)
    # 窗口左上角与屏幕左上角的相对坐标
    # mainwindow.move(1100, 75)
    mainwindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出
