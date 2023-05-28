
import os
import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QModelIndex, QSettings, QDateTime, Qt
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel

from MY_DESIGN_LL1 import MyDesiger_LL
from show import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DetailUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(DetailUI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('编译器')
        self.tree_view = self.treeView
        '''
         self.sample_type = self.treeView

        self.sample_type.setHeaderHidden(True)  # 不显示表头
        self.sample_type.setColumnHidden(1, False)  # 不显示行头
        self.Dirmodel = QFileSystemModel()
        self.Dirmodel.setRootPath(QDir.currentPath())

        # self.Dirmodel.setFilter(QDir.Dirs)#内容过滤，只显示文件夹
        self.sample_type.setModel(self.Dirmodel)
        self.sample_type.setRootIndex(self.Dirmodel.index(fileDir))  #
        self.sample_type.setColumnHidden(1, True)
        self.sample_type.setColumnHidden(2, True)
        self.sample_type.setColumnHidden(3, True)  # 隐藏不需要的列
        '''
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

        self.actionLL1.triggered.connect(self.LL1_analyze)

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
        '''
         a = 1  # 数据3：数值类型
        print(list_)
        bool_ = True  # 数据:5：布尔类型
        dict_ = {'a': 'abc', 'b': 2}  # 数据6：字典类型

        '''
        self.app_data.setValue('list', list_)

    def init_info(self):
        time = self.app_data.value('time')
        last_path = self.app_data.value('self.last_path')
        a = self.app_data.value('a')
        list_ = self.app_data.value('list')
        bool_ = self.app_data.value('bool')
        dict_ = self.app_data.value('dict')
        print(time)  # 输出数据的值
        print(type(time))  # 输出数据类型
        print(last_path)
        print(type(last_path))
        print(a)
        print(type(a))

        print(list_)
        print(type(list_))
        print(bool_)
        print(type(bool_))
        print(dict_)
        print(type(dict_))

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            print(fname[0])
            with open(fname[0], encoding=self.check_charset(fname[0])) as f:
                str = f.read()
                print(str)
                self.textEdit.setText(str)

    def save_text(self):
        choice = QMessageBox.question(self, "Question", "Do you want to save it?",
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            with open('save text.txt', 'w') as f:
                f.write(self.textEdit.toPlainText())
            self.close()
        elif choice == QMessageBox.No:
            self.close()

    def onFileSaveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '文本文件 (*.txt)')
        if not path:
            return
        self._saveToPath(path)

    def _saveToPath(self, path):
        text = self.textEdit.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            print(str(e))
        else:
            self.path = path

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
        # tc.select(QtGui.QTextCursor.BlockUnderCursor) 这样删除一行
        tc.removeSelectedText()

    def file_name(self, Qmodelidx):
        print(self.model.filePath(Qmodelidx))  # 输出文件的地址。
        print(self.model.fileName(Qmodelidx))  # 输出文件名

    def increase_font(self):
        # 创建一个QFont对象，并设置初始字体大小为12
        font = QFont()
        font.setPointSize(12)
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
        font.setPointSize(10)
        self.textEdit.setFont(font)
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return
        font__size = 10
        # 获取当前字体大小，并增加2个点
        char_format = cursor.charFormat()
        # char_format = cursor.selectionCharFormat()
        font_size = char_format.fontPointSize()
        print('909090000')
        print(font_size)
        char_format.setFontPointSize(font__size + 3)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def on_decrease_font_size_clicked(self):
        font = QFont()
        font.setPointSize(10)
        self.textEdit.setFont(font)
        # 获取当前选中的文本
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        # 如果没有选中文本，则返回
        if not selected_text:
            return
        font__size = 10
        # 获取当前字体大小，并增加2个点
        char_format = cursor.charFormat()
        # char_format = cursor.selectionCharFormat()
        font_size = char_format.fontPointSize()
        print('909090000')
        print(font_size)
        char_format.setFontPointSize(font__size - 2)

        # 将选中的文本应用新的格式
        cursor.mergeCharFormat(char_format)

    def decrease_font(self):
        font = QFont()
        font.setPointSize(12)
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
            format.setForeground(QtGui.QBrush(QtCore.Qt.red))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_green_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(QtCore.Qt.green))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_blue_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(QtCore.Qt.blue))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_orange_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(QtCore.Qt.darkYellow))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def set_purple_font(self):
        selected_text = self.textEdit.textCursor().selectedText()
        if selected_text:
            format = QtGui.QTextCharFormat()
            format.setForeground(QtGui.QBrush(QtCore.Qt.magenta))
            cursor = self.textEdit.textCursor()
            cursor.insertText(selected_text, format)

    def LL1_analyze(self):
        self.LL_window = MyDesiger_LL()
        self.LL_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DetailUI()
    ex.show()
    sys.exit(app.exec_())