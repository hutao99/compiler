import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from DAG_UI import Ui_MainWindow_DAG
from PyQt5.QtWidgets import QFileDialog, QMainWindow


class MyDesiger_DAG(Ui_MainWindow_DAG, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_DAG, self).__init__(parent)
        self.setWindowTitle("DAG优化")
        self.setupUi(self)
        # 设置响应槽（信号源 conect 槽）
        self.pushButton.clicked.connect(self.open_text)

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


app = QApplication(sys.argv)
LL_window = MyDesiger_DAG()
LL_window.show()
sys.exit(app.exec_())
