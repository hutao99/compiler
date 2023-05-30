import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from DAG_UI import Ui_MainWindow_DAG
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from create_DAG import create_DAG, optimize, DAG_draw  # DAG模型
from PyQt5 import QtGui, QtCore, QtWidgets


class MyDesiger_DAG(Ui_MainWindow_DAG, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_DAG, self).__init__(parent)
        self.setWindowTitle("DAG优化")
        self.setupUi(self)
        # 设置响应槽
        self.pushButton.clicked.connect(self.open_text)
        self.pushButton_1.clicked.connect(self.DAG_optimal)

    def DAG_optimal(self):
        s = self.textEdit.toPlainText()
        if s == '':
            QMessageBox.warning(self, '警告', '请输入需要生成DAG的四元式！')
            return
        # code 四元式列表
        if s[0] == '(':
            lst = [tuple(x.strip() for x in line.strip("()").split(",")) for line in s.splitlines()]
            code = [tuple(x.strip() for x in _[1:-1].split(',')) for _ in s.split("\n")]
        else:
            code = [tuple(x.strip() for x in _.split(',')) for _ in s.split("\n")]
        DAG = create_DAG(code)
        codes = optimize(DAG)
        info = '\n'.join(["(" + ','.join(c) + ")" for c in codes])
        self.textEdit_3.setText(info)
        DAG_draw(DAG)
        # 设置图片路径
        image_format = QtGui.QTextImageFormat()
        image_format.setName('./DAG/visible.gv.png')
        # 在QTextEdit中插入图片
        self.textEdit_2.clear()
        cursor = self.textEdit_2.textCursor()
        cursor.insertImage(image_format)

        self.textEdit_2.show()

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
                    self.textEdit.setText(str)
        except Exception as e:
            print("Error: ", e)


# app = QApplication(sys.argv)
# LL_window = MyDesiger_DAG()
# LL_window.show()
# sys.exit(app.exec_())
