# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from LR_UI import Ui_MainWindow_LR
from PyQt5.QtWidgets import QFileDialog, QMainWindow


class MyDesiger_LR(Ui_MainWindow_LR, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_LR, self).__init__(parent)
        self.setWindowTitle("LR分析")
        self.setupUi(self)
        # 设置响应槽
        self.pushButton_1.clicked.connect(self.open_text)

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



app = QApplication(sys.argv)
LL_window = MyDesiger_LR()
LL_window.show()
sys.exit(app.exec_())
