import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from LL_UI import Ui_MainWindow_LL
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from TABLE import LL


# 在基本LL1界面的基础上进行完善，添加了槽函数
class MyDesiger_LL(Ui_MainWindow_LL, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_LL, self).__init__(parent)
        self.setWindowTitle("LL(1)预测分析")
        self.setupUi(self)
        # 设置响应槽
        self.pushButton_1.clicked.connect(self.open_text)
        self.pushButton_2.clicked.connect(self.onClick_create_first_follow_analyze_table)
        self.pushButton.clicked.connect(self.onClick_analyze_stack)

    def onClick_analyze_stack(self):
        STACK = ['#']  # 输入栈
        STACK_INPUT = []  # 剩余输入串
        test = LL()
        # 对LL1输入文法的格式进行处理，考虑到两个非终结符之间没有空格的情况
        text = self.textEdit_2.toPlainText()
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
        print(grammar)
        test.input(grammar)
        print(test.first)
        print(test.last)
        print(test.flag)
        begin_ch = test.begin
        SELECT = test.predict_table_
        # 获取输入串并加入‘#’结束标志
        layer_stack = 1
        # 先设置 table层数为1 后 动态增加
        self.tableStack.setRowCount(layer_stack)
        # 获取 输入串 输入框中的句子 并且保存在 STACK_INPUT 列表中

        for word in self.textEdit.toPlainText():
            STACK_INPUT.append(word)
        # 很重要
        STACK_INPUT.append('#')
        STACK.append(begin_ch)
        test.analysis(STACK_INPUT)
        print(test.flag)
        if test.flag == 0:

            # 打印分析栈表 的第一行 ，初始化的默认行
            # 打印输入串
            str_w = ''
            for word in STACK_INPUT:
                str_w += word
            item1 = QtWidgets.QTableWidgetItem(str_w)
            self.tableStack.setItem(0, 1, item1)
            str_w = ''
            # 打印输入栈
            for word in STACK:
                str_w += word
            item1 = QtWidgets.QTableWidgetItem(str_w)
            # 动作 初始化
            self.tableStack.setItem(0, 0, item1)

            # 后续LL(1)文法分析栈表的实现 分两个部分①输入串顶不为‘#’（还没到输入串结束符） ②输入串为‘#’（到输入串结束符）
            while STACK_INPUT[0] != '#':
                # 层数增加一层
                layer_stack = layer_stack + 1
                self.tableStack.setRowCount(layer_stack)

                # 如果符号栈的栈顶为大写字符（即非终结符）则执行下面的操作 符号出栈入栈 并打印相关表信息
                if STACK[-1].isupper():

                    # 获得预测分析表中，的数据，利用 M[S][VT]矩阵调用操作类型
                    str = SELECT[STACK[-1]][STACK_INPUT[0]].split("->")[1].strip()
                    print(str)
                    item1 = QtWidgets.QTableWidgetItem(SELECT[STACK[-1]][STACK_INPUT[0]])
                    self.tableStack.setItem(layer_stack - 1, 2, item1)
                    print(SELECT[STACK[-1]][STACK_INPUT[0]])

                    # 如果 符号栈顶的动作不是是 S -> $ 则符号栈 出栈 入栈（逆序）
                    if str != '$':
                        ##逆置
                        STACK.remove(STACK[-1])
                        for word in str[::-1]:
                            STACK.append(word)
                        # print(STACK)
                        # 在表中显示动作
                        item1 = QtWidgets.QTableWidgetItem("POP,PUSH(" + str + ")")
                        self.tableStack.setItem(layer_stack - 1, 3, item1)

                    # 如果 符号栈顶的动作是 S -> ε 则符号栈 则直接出栈
                    else:
                        STACK.remove(STACK[-1])
                        # 在表中显示动作
                        item1 = QtWidgets.QTableWidgetItem("POP")
                        self.tableStack.setItem(layer_stack - 1, 3, item1)

                    # 在表中显示符号栈，剩余输入串
                    str_w = ''
                    for word in STACK:
                        str_w += word
                    item1 = QtWidgets.QTableWidgetItem(str_w)
                    self.tableStack.setItem(layer_stack - 1, 0, item1)
                    str_w = ''
                    for word in STACK_INPUT:
                        str_w += word
                    item1 = QtWidgets.QTableWidgetItem(str_w)
                    self.tableStack.setItem(layer_stack - 1, 1, item1)
                # 如果符号栈栈顶是 终结符（非大写） ，则比较符号栈栈顶 和 剩余输入串的第一个元素是否相同相同则都出栈
                else:
                    if STACK[-1] == STACK_INPUT[0]:
                        STACK.remove(STACK[-1])
                        STACK_INPUT.remove(STACK_INPUT[0])

                        str_w = ''
                        for word in STACK:
                            str_w += word
                        item1 = QtWidgets.QTableWidgetItem(str_w)
                        self.tableStack.setItem(layer_stack - 1, 0, item1)
                        str_w = ''
                        for word in STACK_INPUT:
                            str_w += word
                        item1 = QtWidgets.QTableWidgetItem(str_w)
                        self.tableStack.setItem(layer_stack - 1, 1, item1)

                        item1 = QtWidgets.QTableWidgetItem("GET_NEXT()")
                        self.tableStack.setItem(layer_stack - 1, 3, item1)
            #  剩余输入串已经到#
            while STACK[-1] != '#':
                layer_stack = layer_stack + 1
                self.tableStack.setRowCount(layer_stack)
                # 如果分析表中的动作是 S->$ 则 打印 该表达式
                if SELECT[STACK[-1]][STACK_INPUT[0]][-1] == '$':
                    item1 = QtWidgets.QTableWidgetItem(SELECT[STACK[-1]][STACK_INPUT[0]])
                    self.tableStack.setItem(layer_stack - 1, 2, item1)
                STACK.remove(STACK[-1])
                # print(STACK)
                # 显示信息
                str_w = ''
                for word in STACK:
                    str_w += word
                item1 = QtWidgets.QTableWidgetItem(str_w)
                self.tableStack.setItem(layer_stack - 1, 0, item1)
                str_w = ''
                for word in STACK_INPUT:
                    str_w += word
                item1 = QtWidgets.QTableWidgetItem(str_w)
                self.tableStack.setItem(layer_stack - 1, 1, item1)

                item1 = QtWidgets.QTableWidgetItem("POP")
                self.tableStack.setItem(layer_stack - 1, 3, item1)
        elif test.flag == 1:
            # 打印分析栈表 的第一行 ，初始化的默认行
            # 打印输入串
            str_w = ''
            for word in STACK_INPUT:
                str_w += word
            item1 = QtWidgets.QTableWidgetItem(str_w)
            self.tableStack.setItem(0, 1, item1)
            str_w = ''
            # 打印输入栈
            for word in STACK:
                str_w += word
            item1 = QtWidgets.QTableWidgetItem(str_w)
            # 动作 初始化
            self.tableStack.setItem(0, 0, item1)
            item1 = QtWidgets.QTableWidgetItem("抱歉，您所输入的字符串不符合文法")
            self.tableStack.setItem(0, 2, item1)

    def onClick_create_first_follow_analyze_table(self):
        # 获得所输入框输入的文法
        test = LL()
        # 对LL1输入文法的格式进行处理，考虑到两个非终结符之间没有空格的情况
        text = self.textEdit_2.toPlainText()
        grammar=self.textEdit_2.toPlainText()
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
        print(grammar)
        test.input(grammar)
        print(test.first)
        print(test.last)
        FIRST = test.first
        FOLLOW = test.last
        VT = test.vt
        VN = test.vn
        SELECT = test.predict_table_
        # 将字典的内容写入 QTextEdit 控件
        text_first = 'FIRST集合如下：\n'
        for key, value in FIRST.items():
            text_first += '{}: {}\n'.format(key, value)
        # 界面显示 first集
        self.textFirst_set.setPlainText(text_first)
        text_follow = 'FOLLOW集合如下：\n'
        for key, value in FOLLOW.items():
            text_follow += '{}: {}\n'.format(key, value)
        # 界面显示 first集
        self.textFollow_set.setPlainText(text_follow)

        # 设置预测分析表的列数 len(VT)+2 终结符的数量加2,2 为第一列非终结符占一列，最后#占一列
        self.tableAnalyze.setColumnCount(len(VT) + 2)
        layer_analyze = 1
        # 设置预测分析表的层数
        self.tableAnalyze.setRowCount(layer_analyze)
        VT_1 = VT[:]
        VT_1.append('#')

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

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        try:
            # fname = QFileDialog.getOpenFileName(None, 'Open file')
            fname = QFileDialog.getOpenFileName(self, 'Open file')
            if fname[0]:
                print(fname[0])
                with open(fname[0], encoding=self.check_charset(fname[0])) as f:
                    str = f.read()
                    print(str)
                    self.textEdit_2.setText(str)
        except Exception as e:
            print("Error: ", e)


# app = QApplication(sys.argv)
# LL_window = MyDesiger_LL()
# LL_window.show()
# sys.exit(app.exec_())
