import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QLabel

from DAG_UI import Ui_MainWindow_DAG
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from create_DAG import create_DAG, optimize, DAG_draw  # DAG模型
from PyQt5 import QtGui, QtCore, QtWidgets

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.label = QLabel(self)
        self.pixmap = QPixmap('./DAG/visible.gv.png')
        self.label.setPixmap(self.pixmap)
        self.setWindowTitle('分析图')
        self.resize(self.pixmap.width(), self.pixmap.height())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '保存图片', '是否要保存图片？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            file_name, _ = QFileDialog.getSaveFileName(self, '保存图片', '', 'Images (*.png *.xpm *.jpg)')
            if file_name:
                self.pixmap.save(file_name)
        event.accept()

class MyDesiger_DAG(Ui_MainWindow_DAG, QMainWindow):
    def __init__(self, parent=None):
        super(MyDesiger_DAG, self).__init__(parent)
        self.setWindowTitle("DAG优化")
        self.setupUi(self)
        # 设置响应槽
        self.pushButton.clicked.connect(self.open_text)
        self.pushButton_1.clicked.connect(self.DAG_optimal)
        self.pushButton_2.clicked.connect(self.show_image)

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
        try:
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
        except:
            QMessageBox.warning(self, '警告', '系统无法处理！')

    def check_charset(self, file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(1000)
            charset = chardet.detect(data)['encoding']
        return charset

    def open_text(self):
        # 定义打开文件夹目录的函数
        path, _ = QFileDialog.getOpenFileName(self, '打开文件', './全部测试程序/14DAG测试用例',
                                              '文本文件 (*.txt)')
        if path != '':  # 选择了文件就读,否则不读，解决未选择文件卡死的问题
            with open(path, 'r', encoding="utf-8") as f:
                text = f.read()
            f.close()
            self.textEdit.clear()
            self.textEdit.setText(text)
    def show_image(self):
        '''
        :return:显示图片
        '''
        dialog = MyDialog(self)
        dialog.setModal(True)
        dialog.exec_()

# app = QApplication(sys.argv)
# LL_window = MyDesiger_DAG()
# LL_window.show()
# sys.exit(app.exec_())
