import os
import sys
import webbrowser

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QModelIndex, QSettings, QDateTime, Qt
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel, QApplication

from MY_DESIGN_DAG import MyDesiger_DAG, MyDialog
from MY_DESIGN_LL1 import LL1GrammarSolver
from suanfu_final import OPGGrammarSolver
from LR1_surface import LR1GrammarSolver
from LR0_surface import LR0GrammarSolver

from show import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Laxer1 import LexicalAnalysis

from Grammar import recDesc_analysis
from ObjectCode1 import solve
import ObjectCode1
# LR
import LR
from Analyzer import AnalyzerLex

from create_DAG import create_DAG, optimize, Partition_Basic_Block, all_basic_optimize
# REG
from REG_control import REG_MainWindow


class DetailUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(DetailUI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('编译器')
        self.tree_view = self.treeView

        self.model = QDirModel()  # 显示文件系统
        # self.model.setRootPath(self.data_path)
        self.tree_view.setModel(self.model)
        # self.tree_view.setRootIndex(self.model.index(self.data_path))
        self.tree_view.setHeaderHidden(True)  # 不显示表头
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        # self.doubleClicked.connect(self.file_name)  # 双击文件打开
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        self.app_data = QSettings('config.ini', QSettings.IniFormat)
        self.app_data.setIniCodec('UTF-8')  # 设置ini文件编码为 UTF-8
        self.file_path = ""
        self.folder_path_set = []
        self.recent_folders()
        # 定义计数器变量
        self.font_size_count = 0
        # 文件的打开，保存，另存为，关闭
        self.actionOPEN.triggered.connect(self.open_text)
        self.actionSAVE.triggered.connect(self.save_text)
        self.actionSAVE_ANOTHER.triggered.connect(self.onFileSaveAs)
        self.actionCLOSE.triggered.connect(self.close)
        '''
        ("undo", "&撤销(&U)..."), ("redo", "&恢复(&R)..."),
                           ("cut", "剪切(&T)"), ("copy", "复制(&C)"), ("paste", "粘贴(&P)"), ("delete", "删除(&L)")
                           , ("select_all", "全选(&A)")
        '''
        self.actionundo.triggered.connect(self.textEdit.undo)
        self.actionredo.triggered.connect(self.textEdit.redo)
        self.actioncut.triggered.connect(self.textEdit.cut)
        self.actioncopy.triggered.connect(self.textEdit.copy)
        self.actionpaste.triggered.connect(self.textEdit.paste)
        self.actiondelete.triggered.connect(self.onEditDelete)
        self.actionselect_all.triggered.connect(self.textEdit.selectAll)
        '''
        字体:增大字号，减小字号，加粗，斜体
        '''
        self.actionincrease_font.triggered.connect(self.on_increase_font_size_clicked)
        self.actiondecrease_font.triggered.connect(self.on_decrease_font_size_clicked)
        self.actionbold.triggered.connect(self.on_bold_clicked)
        self.actionunderline.triggered.connect(self.on_underline_clicked)
        self.actionitalic.triggered.connect(self.on_italic_clicked)
        self.actionred_font.triggered.connect(self.set_red_font)
        self.actionblue_font.triggered.connect(self.set_blue_font)
        self.actiongreen_font.triggered.connect(self.set_green_font)
        self.actionorange_font.triggered.connect(self.set_orange_font)
        self.actionpurple_font.triggered.connect(self.set_purple_font)

        '''
        LL1预测分析
        '''
        self.recursive_or_lr_flag = 0  # 为1表示使用递归下降 为2表示使用lr
        self.actionLL1.triggered.connect(self.LL1_analyze)
        self.actionstate_transition.triggered.connect(self.Manual_lexical_analysis)  # 递归下降手动词法分析
        self.actionfrom_up_to_down.triggered.connect(self.Manual_grammar_analysis)  # 语法分析
        self.action_basic_block.triggered.connect(self.Basic_Block)  # 基本块划分
        self.actionDAG.triggered.connect(self.DAG_optimization)  # DAG优化
        self.action_middle_code.triggered.connect(self.middle_analysis)  # 中间代码
        self.actionhuibian_code.triggered.connect(self.Object_analysis)  # 目标代码
        """
        算符优先
        """
        self.actionsuanfu_first.triggered.connect(self.suanfu)
        """
        REG正则表达式转换
        """
        self.actionNFA_DFA.triggered.connect(self.REG_transform)

        '''
        DAG
        '''
        self.actionDAG_.triggered.connect(self.DAG_analyze)

        """
        LR(1)分析
        """
        # 初始化LR分析
        self.LR = LR.CLRParser()
        f = open('文法修改.txt', 'r', encoding='utf-8')
        f1 = open('文法修改1.txt', 'r', encoding='utf-8')
        self.LR.input(f.read())
        lr1 = LR.CLRParser()
        lr1.input(f1.read())
        lr1.Action_and_GoTo_Table()
        self.LR.Action_and_GoTo_Table()
        self.LR.parsing_table1 = lr1.parsing_table
        self.LR.reduction1 = lr1.reduction
        self.actionPLY.triggered.connect(self.LexicalAnalysis)  # 词法分析
        # LR1自定义语法分析
        self.actionLR1.triggered.connect(self.LR1_analyze)
        # LR0语法分析
        self.actionLR0.triggered.connect(self.LR0_analyze)
        '''
        图片导出
        '''
        self.action_tree_pic.triggered.connect(self.save_tree)
        self.action_baseblock_pic.triggered.connect(self.save_base_block)
        self.action_DAG_pic.triggered.connect(self.save_DAG)

        '''
        对一些变量进行初始化
        '''
        self.siyuanshi = None
        self.basic_blocks = None
        self.split_flag = 0  # 是否划分四元式
        self.yh_flag = 0  # 是否进行优化
        self.file_path = None  # 用于保存当前打开的文件路径

        '''
        添加帮助文档和版权信息
        '''
        self.actionHELP_CHM.triggered.connect(self.searchHelp)
        self.action.triggered.connect(self.show_copyright)

    def recent_folders(self):
        try:
            # 添加根节点
            self.tree.setHeaderHidden(True)
            root = QTreeWidgetItem(self.tree)
            root.setText(0, "Recent Folders")

            list_ = self.app_data.value('list')

            print(list_)

            # 将最近打开的文件夹添加到QTreeWidget中
            recent_folders = list_
            for folder in recent_folders:
                item = QTreeWidgetItem(root)
                item.setText(0, os.path.basename(folder))
                item.setData(0, Qt.UserRole, folder)

            ''''''

            # 连接itemDoubleClicked信号到槽函数
            def on_item_clicked(item, column):
                # 获取双击的项目
                folder_path = item.data(0, Qt.UserRole)
                if not os.path.isdir(folder_path):
                    return

                # 显示目录下的内容
                sub_items = os.listdir(folder_path)
                for sub_item in sub_items:
                    sub_item_path = os.path.join(folder_path, sub_item)
                    sub_item_name = os.path.basename(sub_item_path)
                    sub_tree_item = QTreeWidgetItem(item)
                    sub_tree_item.setText(0, sub_item_name)
                    sub_tree_item.setData(0, Qt.UserRole, sub_item_path)
                    # 获取点击的项目

            def on_item_double_clicked(item, column):
                try:
                    # 获取双击的项目
                    folder_path = item.parent().data(0, Qt.UserRole)
                    file_name = item.text(0)
                    file_path = os.path.join(folder_path, file_name)
                    if not os.path.isfile(file_path):
                        return

                    # 获取文件的绝对路径
                    abs_file_path = os.path.abspath(file_path)
                    with open(abs_file_path, encoding=self.check_charset(abs_file_path)) as f:
                        str = f.read()
                        print(str)
                        self.textEdit.setText(str)
                    print(abs_file_path)
                except Exception as e:
                    print("Error: ", e)

            self.tree.itemDoubleClicked.connect(on_item_double_clicked)
            self.tree.itemClicked.connect(on_item_clicked)

            # 显示QTreeWidget
            self.tree.setWindowTitle("Recent Folders")
            self.tree.resize(640, 480)
            self.tree.show()
        except Exception as e:
            print("Error:", e)

    def getDir(self, index):  # 获取鼠标指向索引,还可以预览图
        self.FilePath = self.model.filePath(index)  # 获取鼠标点击指定路径
        self.index_rm = index  # index就是QModelIndex

    def on_tree_view_clicked(self, index: QModelIndex):
        self.file_path = self.model.filePath(index)

        if os.path.isfile(self.file_path):
            print(self.file_path)
            with open(self.file_path, encoding=self.check_charset(self.file_path)) as f:
                str = f.read()
                print(str)
                self.textEdit.setText(str)
        elif os.path.isdir(self.file_path):
            self.folder_path_set.append(self.file_path)
            self.folder_path_set = list(set(self.folder_path_set))
            print(self.file_path)

        self.save_info()
        self.init_info()

    def save_info(self):
        # 参考了https://blog.csdn.net/qq_38463737/article/details/107109046
        time = QDateTime.currentDateTime()  # 获取当前时间，并存储在self.qpp_data
        self.app_data.setValue('time', time.toString())  # 数据0：time.toString()为字符串类型
        print(self.file_path)
        print(type(self.file_path))
        self.app_data.setValue('self.last_path', self.file_path)  # 数据1：也是字符串类型
        list_ = self.folder_path_set  # 数据4：列表类型

        self.app_data.setValue('list', list_)

    def init_info(self):
        time = self.app_data.value('time')
        last_path = self.app_data.value('self.last_path')
        a = self.app_data.value('a')
        list_ = self.app_data.value('list')
        bool_ = self.app_data.value('bool')
        dict_ = self.app_data.value('dict')

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            print(file_path)
            with open(file_path, encoding=self.check_charset(file_path)) as f:
                str = f.read()
                # print(str)
                # 将文本框中的字体颜色设置为默认的黑色，防止出现第一次将文本标红时，第二次打开文本全部为红色的情况
                text_color = QColor(Qt.black)
                self.textEdit.setTextColor(text_color)
                self.textEdit.setText(str)
                self.file_path = file_path  # 保存当前打开的文件路径

    def save_text(self):
        text = self.textEdit.toPlainText()
        if text == '':
            QMessageBox.warning(self, '警告', '请在左上输入框输入代码或打开文件')
        else:
            # 弹出文件对话框，让用户选择要保存的文件路径和文件名
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)",
                                                       options=options)
            if file_name:
                # 如果用户选择了文件路径和文件名，则执行保存操作
                with open(file_name, 'w') as f:
                    f.write(self.textEdit.toPlainText())


    def onFileSaveAs(self):
        text = self.textEdit.toPlainText()
        if text == '':
            QMessageBox.warning(self, '警告', '请在左上输入框输入代码或打开文件')
        else:
            # 另存为…的时候，能定位到打开的文件路径，显示默认的文件名
            if self.file_path:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File", self.file_path,
                                                           "Text Files (*.txt);;All Files (*)")
            else:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, "w") as f:
                    f.write(self.text_edit.toPlainText())
                self.file_path = file_path  # 更新当前文件路径

    def closeEvent(self, event):
        # 保存设置
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("MainWindow/Geometry",
                              self.saveGeometry())
            settings.setValue("MainWindow/State",
                              self.saveState())
            settings.setValue("MessageSplitter",
                              self.textEdit.saveState())
            settings.setValue("MainSplitter",
                              self.splitter1.saveState())
        else:
            event.ignore()

    def okToContinue(self):
        return True

    def onEditDelete(self):
        tc = self.textEdit.textCursor()
        tc.removeSelectedText()

    def file_name(self, Qmodelidx):
        print(self.model.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.model.fileName(Qmodelidx))  # 输出文件名

    def increase_font(self):
        # 创建一个QFont对象，并设置初始字体大小为12
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)

        # 获取当前字体大小
        font_size = self.textEdit.fontPointSize()

        # 增大字体大小
        font_size += 2

        # 设置新的字体大小
        self.textEdit.setFontPointSize(font_size)

        # 将光标移动到文本末尾
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def on_increase_font_size_clicked(self):
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return
        font__size = 13
        # 获取当前字体大小，并增加2个点
        char_format = cursor.charFormat()
        # char_format = cursor.selectionCharFormat()
        font_size = char_format.fontPointSize()
        char_format.setFontPointSize(font__size + 3)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def on_decrease_font_size_clicked(self):
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return
        font__size = 13
        # 获取当前字体大小，并减小2个点
        char_format = cursor.charFormat()
        # char_format = cursor.selectionCharFormat()
        font_size = char_format.fontPointSize()
        char_format.setFontPointSize(font__size - 2)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def decrease_font(self):
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        # 获取当前字体大小
        font_size = self.textEdit.fontPointSize()

        # 增大字体大小2个点
        font_size -= 2

        # 设置新的字体大小
        self.textEdit.setFontPointSize(font_size)

        # 将光标移动到文本末尾
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def on_bold_clicked(self):
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return

        # 创建一个新的QTextCharFormat对象，并设置其字体为加粗
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def on_underline_clicked(self):
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return

        # 创建一个新的QTextCharFormat对象，并设置其下划线属性为True
        char_format = QTextCharFormat()
        char_format.setFontUnderline(True)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def on_italic_clicked(self):
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return

        # 创建一个新的QTextCharFormat对象，并设置其下划线属性为True
        char_format = QTextCharFormat()
        # 设置为斜体
        char_format.setFontItalic(True)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def set_red_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(Qt.red))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_green_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(Qt.green))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_blue_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(Qt.blue))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_orange_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(Qt.darkYellow))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_purple_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(Qt.magenta))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def LL1_analyze(self):
        self.LL_window = LL1GrammarSolver()
        self.LL_window.show()

    def DAG_analyze(self):
        self.DAG_window = MyDesiger_DAG()
        self.DAG_window.show()

    def LR1_analyze(self):
        self.LR_window = LR1GrammarSolver()
        self.LR_window.show()

    def LR0_analyze(self):
        self.LR0_window = LR0GrammarSolver()
        self.LR0_window.show()

    # 递归下降手动词法分析
    def Manual_lexical_analysis(self):
        self.recursive_or_lr_flag = 1
        text = self.textEdit.toPlainText()
        if text == '':
            QMessageBox.warning(self, '警告', '请在左上输入框输入代码或打开文件')
        try:
            a = LexicalAnalysis(text)
            self.wordlist, self.errorlist, self.lbword = a.print_out()
            self.textEdit_3.setText(self.wordlist)
            self.textEdit_2.setText(self.errorlist)

            # 初始化
            self.split_flag = 0
            self.yh_flag = 0
            self.siyuanshi = None
            self.basic_blocks = None

            # 对textEdit中的关键字进行处理
            self.change_keyword_color()
        except:
            QMessageBox.warning(self, '警告', '系统无法处理！')

    # 对textEdit中的关键字进行处理
    def change_keyword_color(self):
        text = self.textEdit.toPlainText()
        a = LexicalAnalysis(text)
        keywords = []
        for i in a.keyword_dist.keys():
            keywords.append(i)
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        while not cursor.atEnd():
            cursor.select(QTextCursor.WordUnderCursor)
            word = cursor.selectedText()
            if word in keywords:
                format = cursor.charFormat()
                format.setForeground(QColor("red"))
                cursor.setCharFormat(format)
            cursor.movePosition(QTextCursor.NextWord)

    # 递归下降语法分析
    def Manual_grammar_analysis(self):
        if self.recursive_or_lr_flag == 0:
            QMessageBox.warning(self, '警告', '请先进行词法分析！')
        else:
            if self.recursive_or_lr_flag == 1:
                if self.lbword == [] or self.lbword == None:
                    QMessageBox.warning(self, '警告', '请先进行词法分析！')
                else:
                    try:
                        file_object = open('文法.txt')
                        rda = recDesc_analysis(file_object)
                        self.fun_list, self.function_param_list, self.function_jubu_list, self.siyuanshi, self.yufa_Rrror, self.worrings_str, self.text1, self.text2 = rda.solve(
                            self.lbword)
                        if self.yufa_Rrror == '' and self.worrings_str == '':
                            text1 = ''
                        elif self.yufa_Rrror == '':
                            text1 = "语义错误：\n" + self.worrings_str
                        elif self.worrings_str == '':
                            text1 = "语法错误处理：\n" + self.yufa_Rrror
                        else:
                            text1 = "语法错误处理：\n" + self.yufa_Rrror + "语义错误：\n" + self.worrings_str
                        all_text = text1 + self.text1 + '\n' + self.text2 + '\n'
                        self.textEdit_2.setText(all_text)
                        # 设置图片路径
                        self.textEdit_3.clear()
                        image_format = QtGui.QTextImageFormat()
                        image_format.setName('./Syntax_Tree/tree.gv.png')

                        # 在QTextEdit中插入图片
                        cursor = self.textEdit_3.textCursor()
                        cursor.insertImage(image_format)

                        self.textEdit_3.show()



                    except:
                        QMessageBox.warning(self, '警告', '系统无法处理！')
            else:
                try:
                    # LR语法分析
                    text = self.textEdit.toPlainText()
                    if len(text) != 0:
                        lex = AnalyzerLex()
                        lex.input(text)
                        tokens = []
                        while True:
                            tok = lex.token()
                            if not tok:
                                break
                            tokens.append([tok.type, tok.value, tok.lineno,
                                           lex.find_column(tok.lexer.lexdata, tok)])
                        tokens.append(['keyword', '#'])
                        self.LR.ControlProgram(tokens)
                        self.LR.PrintParseTree()  # 画语法树图
                        # 设置图片路径
                        image_format = QtGui.QTextImageFormat()
                        image_format.setName('./Syntax_Tree/tree.gv.png')

                        # 在QTextEdit中插入图片
                        self.textEdit_3.setText('')
                        cursor = self.textEdit_3.textCursor()
                        cursor.insertImage(image_format)
                        self.textEdit_3.show()  # 语法树
                        self.siyuanshi = [['main', '', '', '']]
                        errors = []
                        errors.extend(lex.error)
                        errors.extend(self.LR.errors)
                        errors = sorted(errors, key=lambda x: (x[0], x[1]))
                        s = ''
                        s += '常量表:\n'
                        for i in self.LR.ConstantTable:
                            s += i + ": "
                            for j in self.LR.ConstantTable[i]:
                                s += str(vars(j)) + '\n'

                        s += '变量表:\n'
                        for i in self.LR.VariableTable:
                            s += i + ": "
                            for j in self.LR.VariableTable[i]:
                                s += str(vars(j)) + '\n'

                        s += '数组表:\n'
                        for i in self.LR.ArrayTable:
                            s += i + ": "
                            for j in self.LR.ArrayTable[i]:
                                s += str(vars(j)) + '\n'

                        s += '函数表:\n'
                        for i in self.LR.FunctionTable:
                            s += i + ": "
                            s += str(vars(self.LR.FunctionTable[i])) + '\n'
                        s += '\nerror %d\n' % len(errors)
                        for i in errors:  # 语法和语义错误
                            s += ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2]))
                        for i in self.LR.warning:
                            s += ("行:{:<5}列:{:<5}warnings:{:<20}\n".format(i[0], i[1], i[2]))
                        self.textEdit_2.setText(s)
                except Exception as e:
                    QMessageBox.warning(self, '警告', '系统无法处理！')

    def save_tree(self):
        if self.recursive_or_lr_flag == 0:
            QMessageBox.warning(self, '警告', '请先进行词法分析！')
        else:
            if self.siyuanshi == None or self.siyuanshi == []:
                QMessageBox.warning(self, '警告', '请先进行语法分析！')
            else:
                try:
                    dialog = MyDialog('./Syntax_Tree/tree.gv.png', self)
                    dialog.setModal(True)
                    dialog.exec_()
                except FileNotFoundError as e:
                    print('文件不存在：', e.filename)
                except Exception as e:
                    print('发生了异常：', e)

    # 中间代码
    def middle_analysis(self):
        self.yh_flag = 0
        if self.recursive_or_lr_flag == 0:
            QMessageBox.warning(self, '警告', '请先进行词法分析！')
        else:
            if self.recursive_or_lr_flag == 1:  # 递归下降中间代码
                if self.siyuanshi == None or self.siyuanshi == []:
                    QMessageBox.warning(self, '警告', '请先进行语法分析！')
                else:
                    text = ''
                    idx = 0
                    for quad in self.siyuanshi:
                        text += str(idx) + ':' + str(quad) + '\n'
                        idx += 1
                    self.textEdit_3.setText(text)
            else:  # LR中间代码
                try:
                    text = self.textEdit.toPlainText()
                    if len(text) != 0:
                        lex = AnalyzerLex()
                        lex.input(text)
                        tokens = []
                        while True:
                            tok = lex.token()
                            if not tok:
                                break
                            tokens.append([tok.type, tok.value, tok.lineno,
                                           lex.find_column(tok.lexer.lexdata, tok)])
                        tokens.append(['keyword', '#'])
                        self.LR.ControlProgram(tokens)
                        s = ''
                        if len(self.LR.errors) == 0 and len(lex.error) == 0:
                            self.LR.IntermediateCodeGenerator(tokens)
                            getcode = self.LR.code
                            for i in range(len(getcode)):
                                s += str(i) + ':' + str(getcode[i]) + '\n'
                            self.textEdit_3.setText(s)
                        else:
                            errors = []
                            errors.extend(lex.error)
                            errors.extend(self.LR.errors)
                            errors = sorted(errors, key=lambda x: (x[0], x[1]))
                            for i in errors:
                                s += ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])) + '\n'
                            self.textEdit_2.setText(s)
                except Exception as e:
                    QMessageBox.warning(self, '警告', '系统无法处理！')

    # 基本块划分
    def Basic_Block(self):
        s = self.textEdit_3.toPlainText()  # 获取四元式序列
        if s == '':
            QMessageBox.warning(self, '警告', '请先生成四元式！')
        else:
            try:
                codes = self.format_conversion(s)
                self.basic_blocks = Partition_Basic_Block(codes)
                # print('basic_blocks', self.basic_blocks)
                # 设置图片路径
                image_format = QtGui.QTextImageFormat()
                image_format.setName('./Basic_Block/basic_block.gv.png')

                # 在QTextEdit中插入图片
                self.textEdit_2.clear()
                cursor = self.textEdit_2.textCursor()
                cursor.insertImage(image_format)
                self.textEdit_2.show()
                self.split_flag = 1
            except:
                QMessageBox.warning(self, '警告', '系统错误！')

        # DAG优化

    def save_base_block(self):
        s = self.textEdit_3.toPlainText()  # 获取四元式序列
        if s == '':
            QMessageBox.warning(self, '警告', '请先生成四元式！')
        else:
            try:
                dialog = MyDialog('./Basic_Block/basic_block.gv.png', self)
                dialog.setModal(True)
                dialog.exec_()
            except FileNotFoundError as e:
                print('文件不存在：', e.filename)
            except Exception as e:
                print('发生了异常：', e)

    def DAG_optimization(self):
        if self.split_flag != 1:
            self.Basic_Block()  # 先生成四元式
        try:
            self.optimize_quaternion = all_basic_optimize(self.basic_blocks)
            text = ''
            idx = 0
            for i in self.optimize_quaternion:
                text += str(idx) + ':' + str(i) + '\n'
                idx += 1
            self.textEdit_2.setText(text)
            # print('optimize_quaternion', self.optimize_quaternion)
            self.yh_flag = 1
        except:
            QMessageBox.warning(self, '警告', '系统错误！')

    def save_DAG(self):
        try:
            dialog = MyDialog('./DAG/visible.gv.png', self)
            dialog.setModal(True)
            dialog.exec_()
        except FileNotFoundError as e:
            print('文件不存在：', e.filename)
        except Exception as e:
            print('发生了异常：', e)

    # 目标代码
    def Object_analysis(self):
        if self.recursive_or_lr_flag == 0:
            QMessageBox.warning(self, '警告', '请先进行词法分析！')
        else:
            if self.recursive_or_lr_flag == 1:  # 递归下降目标代码
                if self.siyuanshi == None or self.siyuanshi == []:
                    QMessageBox.warning(self, '警告', '请先生成中间代码!')
                else:
                    try:
                        if not self.yh_flag:
                            text = solve(self.function_param_list, self.function_jubu_list, self.siyuanshi, {}, [])
                        else:
                            text = ''
                            idx = 0
                            for i in self.optimize_quaternion:
                                text += str(idx) + ':' + str(i) + '\n'
                                idx += 1
                            self.textEdit_3.setText(text)
                            text = solve(self.function_param_list, self.function_jubu_list, self.optimize_quaternion,
                                         {}, [])
                        self.textEdit_2.setText(text)
                    except:
                        QMessageBox.warning(self, '警告', '系统无法处理！')
            else:  # LR目标代码
                try:
                    function_param_list = self.LR.function_param_list
                    function_jubu_list = self.LR.function_jubu_list
                    function_array_list = self.LR.function_array_list
                    global_array_list = self.LR.global_array_list
                    if not self.yh_flag:
                        MiddleCode = self.LR.code
                        for i in range(len(MiddleCode)):
                            for j in range(4):
                                if MiddleCode[i][j] == '':
                                    MiddleCode[i][j] = '_'
                        print('MiddleCode', MiddleCode)
                        if len(MiddleCode) != 0:
                            self.textEdit_2.setText(
                                ObjectCode1.solve(function_param_list, function_jubu_list, MiddleCode,
                                                  function_array_list,
                                                  global_array_list))
                    else:
                        text = ''
                        idx = 0
                        for i in self.optimize_quaternion:
                            text += str(idx) + ':' + str(i) + '\n'
                            idx += 1
                        print('self.optimize_quaternion', self.optimize_quaternion)
                        self.textEdit_3.setText(text)
                        self.textEdit_2.setText(
                            ObjectCode1.solve(function_param_list, function_jubu_list, self.optimize_quaternion,
                                              function_array_list,
                                              global_array_list))
                except:
                    QMessageBox.warning(self, '警告', '系统无法处理！')

    def REG_transform(self):
        self.reg_window = REG_MainWindow()
        self.reg_window.show()

    def suanfu(self):
        self.suanfu_window = OPGGrammarSolver()
        self.suanfu_window.show()

    def LexicalAnalysis(self):  # LR词法分析相应函数,自动
        try:
            # 对全局变量进行初始化
            self.split_flag = 0
            self.yh_flag = 0
            self.siyuanshi = None
            self.basic_blocks = None

            self.recursive_or_lr_flag = 2
            text = self.textEdit.toPlainText()
            lex = AnalyzerLex()
            lex.input(text + '\n')
            s = ''
            while True:
                tok = lex.token()
                if not tok:
                    break
                s += ("值:{:<15}行:{:<10}列:{:<10}类型:{:<20}\n".format(
                    tok.value, tok.lineno, lex.find_column(tok.lexer.lexdata, tok), tok.type))
            self.textEdit_3.setText(s)
            s = ''
            for i in lex.error:
                s += (
                    ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))
            self.textEdit_2.setText(s)
            # 对textEdit中的关键字进行处理
            self.change_keyword_color()
        except Exception as e:
            QMessageBox.warning(self, '警告', '系统出错')

    # 将文本框中的四元式转换
    def format_conversion(self, s):
        # print('s', s)
        # 去掉末尾的换行符
        s = s.strip()
        # 按照换行符分割成多个行字符串
        lines = s.split('\n')
        # 初始化结果列表
        result = []
        # 对于每个行字符串，手动将第一个元素转化为一个列表，并去掉第一个元素
        for line in lines:
            if line:
                l = line.split(':')
                lst = eval(l[1])
                lst = [elem if elem != '' else '_' for elem in lst]
                result.append(lst)
        # print('result', result)
        return result

    def searchHelp(self):
        webbrowser.open('编译器_final.chm')

    def show_copyright(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('版权信息')
        msg_box.setText('此版权归重庆理工大学2020级(陈瑞(12003990107)、郑伟(12003990615)、张世佳(12003990108)、谭舟行(12003990522))所有')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DetailUI()
    ex.show()
    sys.exit(app.exec_())
