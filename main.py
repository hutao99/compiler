import sys
import os

import chardet

import LR
from PyQt5.QtGui import QIcon, QPainter, QFont, QTextCursor, QPalette, QBrush, QPixmap, QTextOption, QFontMetrics
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QSize, QPoint, QFile, QIODevice, QTextStream, QTimer
from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtWidgets import QWidget
from Analyzer import Analyzer, AnalyzerLex
from TargetCode import TargetCode


class QTextEditWithLineNum(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont('Consolas', 13, 2)
        font_metrics = QFontMetrics(font)
        self.setFont(font)
        self.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        self.lineNumberArea = LineNumPaint(self)
        self.document().blockCountChanged.connect(self.update_line_num_width)
        self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.update)
        self.textChanged.connect(self.lineNumberArea.update)
        self.cursorPositionChanged.connect(self.lineNumberArea.update)
        self.update_line_num_width()
        self.setWordWrapMode(QTextOption.WordWrap)
        #self.setIndentationWidth(font_metrics.width(' ') * 4)

    def lineNumberAreaWidth(self):
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().width('9') * d_count + 5
        return _width

    def update_line_num_width(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        # 获取首个可见文本块
        first_visible_block_number = self.cursorForPosition(
            QPoint(0, 1)).blockNumber()
        # 从首个文本块开始处理
        blockNumber = first_visible_block_number
        block = self.document().findBlockByNumber(blockNumber)
        top = self.viewport().geometry().top()
        if blockNumber == 0:
            additional_margin = int(self.document().documentMargin(
            ) - 1 - self.verticalScrollBar().sliderPosition())
        else:
            prev_block = self.document().findBlockByNumber(blockNumber - 1)
            additional_margin = int(self.document().documentLayout().blockBoundingRect(
                prev_block).bottom()) - self.verticalScrollBar().sliderPosition()
        top += additional_margin
        bottom = top + \
            int(self.document().documentLayout().blockBoundingRect(block).height())
        last_block_number = self.cursorForPosition(
            QPoint(0, self.height() - 1)).blockNumber()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(),
                                 height, Qt.AlignCenter, number)
            block = block.next()
            top = bottom
            bottom = top + \
                int(self.document().documentLayout(
                ).blockBoundingRect(block).height())
            blockNumber += 1


class LineNumPaint(QWidget):
    def __init__(self, q_edit):
        super().__init__(q_edit)
        self.q_edit_line_num = q_edit

    def sizeHint(self):
        return QSize(self.q_edit_line_num.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.q_edit_line_num.lineNumberAreaPaintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.init_ui()
        self.back_stack = list()
        self.forward_stack = list()
        self.flag = 1  # 在撤销与恢复时保证文本改变时不执行操作
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
        # keyboard.hook(lambda x:print(x))

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        # pixmap = QPixmap("./image/6.jpg")  # 背景图
        # painter.drawPixmap(self.rect(), pixmap)

    def init_ui(self):
        CenterWidget = QWidget()

        self.setCentralWidget(CenterWidget)
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        width = int(0.5 * self.screenwidth)
        height = int(3 / 5 * width)
        self.resize(width, height)

        self.edit = QTextEditWithLineNum(self)  # 带行号的文本框

        QHBox = QHBoxLayout()
        CenterWidget.setLayout(QHBox)
        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu("文件(F)")
        # 新建
        act4 = QAction('新建', self)
        act4.triggered.connect(self.saveAS1)
        file_menu.addAction(act4)
        # 打开
        act1 = QAction('打开', self)
        act1.triggered.connect(self.OpenFile)
        file_menu.addAction(act1)
        # 保存
        act2 = QAction('保存', self)
        act2.triggered.connect(self.save)
        file_menu.addAction(act2)
        # 另存为
        act3 = QAction('另存为', self)
        act3.triggered.connect(self.saveAS)
        file_menu.addAction(act3)

        exit_menu = menu.addMenu("编辑(E)")
        exit_menu.addAction("复制")
        exit_menu.addAction("粘贴")
        exit_menu.addAction("剪切")
        # 撤销
        act5 = QAction('撤销', self)
        act5.triggered.connect(self.Undo)
        exit_menu.addAction(act5)
        # 恢复
        act6 = QAction('恢复', self)
        act6.triggered.connect(self.Redo)
        exit_menu.addAction(act6)
        # 词法分析
        morphology = menu.addMenu("词法分析(W)")
        act8 = QAction('词法分析自动(W)', self)
        act8.triggered.connect(self.LexicalAnalysis)
        morphology.addAction(act8)
        act9 = QAction('词法分析手动(W)', self)
        act9.triggered.connect(self.LexicalAnalysis1)
        morphology.addAction(act9)

        # 语法分析
        grammar = menu.addMenu("语法分析(P)")
        act10 = QAction('语法分析(P)', self)
        act10.triggered.connect(self.SyntaxAnalyzer)
        grammar.addAction(act10)
        act11 = QAction('语义分析(P)', self)
        act11.triggered.connect(self.SemanticAnalyzer)
        grammar.addAction(act11)

        # 中间代码
        middle = menu.addMenu("中间代码(M)")
        act12 = QAction('中间代码', self)
        act12.triggered.connect(self.genMiddleCode)
        middle.addAction(act12)

        target = menu.addMenu("目标代码生成(O)")
        act13 = QAction('目标代码', self)
        act13.triggered.connect(self.getTargetCode)
        target.addAction(act13)

        examine = menu.addMenu("查看(V)")

        help = menu.addMenu("帮助(H)")
        act7 = QAction('帮助', self)
        act7.triggered.connect(self.openchm)
        help.addAction(act7)
        help.addAction("关于Compiler(A)")

        btn = self.addToolBar('File')
        new = QAction(QIcon('image/新建.png'), 'new', self)
        new.triggered.connect(self.saveAS1)
        btn.addAction(new)
        open = QAction(QIcon('image/文件夹.png'), 'open', self)
        open.triggered.connect(self.OpenFile)
        btn.addAction(open)
        save = QAction(QIcon('image/保存.png'), 'save', self)
        save.triggered.connect(self.save)
        btn.addAction(save)
        undo = QAction(QIcon('image/撤销.png'), 'undo', self)
        undo.triggered.connect(self.Undo)
        btn.addAction(undo)
        redo = QAction(QIcon('image/恢复.png'), 'redo', self)
        redo.triggered.connect(self.Redo)
        btn.addAction(redo)

        self.edit.setHorizontalScrollBarPolicy(2)  # 上下和左右滚动都开启
        self.edit.setLineWrapMode(0)  # 文本框不自动换行
        self.edit.textChanged.connect(self.on_edit_textChanged)
        self.edit.setStyleSheet("background: rgb(200,200,255,60)")  # 设置透明
        self.edit.setTabStopWidth(40)  # 设置tab键为4个空格的大小
        QHBox.addWidget(self.edit)

        QVBox = QVBoxLayout()

        self.display1 = QTextEdit(self)
        Bold = QFont('Microsoft YaHei', 12, QFont.Bold)
        self.display1.setFont(Bold)  # 设置字体的粗细、大小、类型
        QVBox.addWidget(self.display1)
        self.display1.setHorizontalScrollBarPolicy(2)  # 同上
        self.display1.setLineWrapMode(0)
        self.display1.setFocusPolicy(QtCore.Qt.NoFocus)  # 文本框不允许编辑
        self.display1.setStyleSheet("background-color: rgb(150,200,200,60);")

        self.display2 = QTextEdit(self)
        self.display2.setFont(Bold)  # 设置字体的粗细、大小、类型
        QVBox.addWidget(self.display2)
        self.display2.setHorizontalScrollBarPolicy(2)  # 同上
        self.display2.setLineWrapMode(0)
        self.display2.setFocusPolicy(QtCore.Qt.NoFocus)  # 文本框不允许编辑
        self.display2.setStyleSheet("background-color: rgb(230,200,200,60);")

        QVBox.setStretch(0, 3)  # 比例设置
        QVBox.setStretch(1, 2)
        QHBox.addLayout(QVBox)
        self.setLayout(QHBox)

        stauslabel = QStatusBar()  # 状态栏
        information = QLabel('状态栏')
        stauslabel.addPermanentWidget(information)
        self.setStatusBar(stauslabel)
        stauslabel.showMessage('行:' + str(self.edit.textCursor().blockNumber() + 1) +
                               '  列:' + str(self.edit.textCursor().columnNumber() + 1))
        self.edit.cursorPositionChanged.connect(lambda: stauslabel.showMessage(
            '行:' + str(self.edit.textCursor().blockNumber() + 1) + '  列:' + str(self.edit.textCursor().columnNumber() + 1)))  # 光标改变时响应
        self.move(int(self.screenwidth / 2 - width / 2),
                  int(self.screenheight / 2 - height / 2))

    def OpenFile(self):  # 打开文件
        path, ftype = QFileDialog.getOpenFileName(
            self, '打开文件', '', '文本文件 (*.txt)')
        if path:
            f = QFile(path)
            if not f.open(QIODevice.ReadOnly | QIODevice.Text):
                self.msgCritical('打开文件失败')
                return False
            f.close()
            self.path = path
            with open(path, 'rb') as f:
                data = f.read()
                result = chardet.detect(data)
                encoding = result['encoding']
            f = open(path, 'r', encoding=encoding)
            self.edit.setPlainText(f.read())
            f.close()  # 关闭文件
        self.setWindowTitle(self.path)

    def save(self):
        if self.path != None:
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write(self.edit.toPlainText())
        else:
            return self.saveAS()

    def saveAS(self):
        path, ftype = QFileDialog.getSaveFileName(
            self, '保存文件', '', '文本文件 (*.txt)')
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.edit.toPlainText())

    def saveAS1(self):
        path, ftype = QFileDialog.getSaveFileName(
            self, '新建文件', '', '文本文件 (*.txt)')
        if not path:
            return
        self.setWindowTitle(self.path)
        self.edit.setText('')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('')

    def Undo(self):  # 撤销
        self.flag = 0
        if len(self.forward_stack) == 0:
            self.flag = 1
            return
        if len(self.forward_stack) == 1:
            text = ''
        else:
            text = self.forward_stack[-2]
        text1 = self.forward_stack.pop(-1)
        self.back_stack.append(text1)
        self.edit.setText(text)
        self.flag = 1

    def Redo(self):  # 恢复
        self.flag = 0
        if len(self.back_stack) == 0:
            self.flag = 1
            return
        text = self.back_stack.pop(-1)
        self.forward_stack.append(text)
        self.edit.setText(text)
        self.flag = 1

    def on_edit_textChanged(self):  # 文本改变时触发
        if self.flag == 0:
            return
        text = self.edit.toPlainText()
        # print(text)
        self.forward_stack.append(text)
        self.back_stack.clear()
        # print(len(self.forward_stack))

    def openchm(self):
        os.startfile("操作手册.chm")

    def LexicalAnalysis(self):  # 词法分析相应函数,自动
        self.display1.clear()
        self.display2.clear()
        lex = AnalyzerLex()
        data = self.edit.toPlainText()[1:]
        lex.input(data+'\n')
        while True:
            tok = lex.token()
            if not tok:
                break
            self.display1.append("值:{:<15}行:{:<10}列:{:<10}类型:{:<20}\n".format(
                tok.value, tok.lineno, lex.find_column(tok.lexer.lexdata, tok), tok.type))
        for i in lex.error:
            self.display2.append(
                ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))

    def LexicalAnalysis1(self):  # 词法分析相应函数,手动
        self.display1.clear()
        self.display2.clear()
        analyzer = Analyzer()
        analyzer.Lexical(self.edit.toPlainText()+'\0')
        for i in analyzer.record:
            print(i)
            self.display1.append(
                "值:{:<15}行:{:<10}列:{:<10}类型:{:<20}\n".format(i[0], i[1], i[2], i[3]))
        for i in analyzer.errors:
            print(i)
            self.display2.append(
                ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))

    def SyntaxAnalyzer(self):  # 语法分析
        self.display1.clear()
        self.display2.clear()
        lex = AnalyzerLex()
        lex.input(self.edit.toPlainText())
        tokens = []
        while True:
            tok = lex.token()
            if not tok:
                break
            tokens.append([tok.type, tok.value, tok.lineno,
                          lex.find_column(tok.lexer.lexdata, tok)])
        tokens.append(['keyword', '#'])
        # print(tokens)
        self.LR.ControlProgram(tokens)
        self.display1.append(self.LR.PrintParseTree())
        errors = []
        errors.extend(lex.error)
        errors.extend(self.LR.errors)
        errors = sorted(errors, key=lambda x: (x[0], x[1]))
        for i in errors:
            print(i)
            self.display2.append(
                ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))

    def SemanticAnalyzer(self):  # 语义分析
        self.display1.clear()
        self.display2.clear()
        lex = AnalyzerLex()
        lex.input(self.edit.toPlainText())
        tokens = []
        while True:
            tok = lex.token()
            if not tok:
                break
            tokens.append([tok.type, tok.value, tok.lineno,
                          lex.find_column(tok.lexer.lexdata, tok)])
        tokens.append(['keyword', '#'])
        # print(tokens)
        self.LR.ControlProgram(tokens)
        self.display1.append('常量表:')
        for i in self.LR.ConstantTable:
            self.display1.append(i + ": ")
            for j in self.LR.ConstantTable[i]:
                self.display1.append(str(vars(j)))

        self.display1.append('变量表:')
        for i in self.LR.VariableTable:
            self.display1.append(i+": ")
            for j in self.LR.VariableTable[i]:
                self.display1.append(str(vars(j)))

        self.display1.append('函数表:')
        for i in self.LR.FunctionTable:
            self.display1.append(i + ": ")
            self.display1.append(str(vars(self.LR.FunctionTable[i])))

        errors = []
        errors.extend(lex.error)
        errors.extend(self.LR.errors)
        errors = sorted(errors, key=lambda x: (x[0], x[1]))
        for i in errors:
            self.display2.append(
                ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))

        warning = sorted(self.LR.warning, key=lambda x: (x[0], x[1]))
        for i in warning:
            self.display2.append(
                ("行:{:<5}列:{:<5}warnings:{:<20}\n".format(i[0], i[1], i[2])))

    def genMiddleCode(self):
        self.display1.clear()
        self.display2.clear()
        lex = AnalyzerLex()
        lex.input(self.edit.toPlainText())
        tokens = []
        while True:
            tok = lex.token()
            if not tok:
                break
            tokens.append([tok.type, tok.value, tok.lineno,
                          lex.find_column(tok.lexer.lexdata, tok)])
        tokens.append(['keyword', '#'])
        self.LR.ControlProgram(tokens)
        if len(self.LR.errors) == 0 and len(lex.error) == 0:
            self.LR.IntermediateCodeGenerator(tokens)
            getcode = self.LR.code
            for i in range(len(getcode)):
                self.display1.append(str(i)+':'+str(getcode[i]))
        else:
            errors = []
            errors.extend(lex.error)
            errors.extend(self.LR.errors)
            errors = sorted(errors, key=lambda x: (x[0], x[1]))
            for i in errors:
                self.display2.append(
                    ("行:{:<5}列:{:<5}error:{:<20}\n".format(i[0], i[1], i[2])))

    def getTargetCode(self):
        MiddleCode = self.LR.code
        var = self.LR.VariableTable
        con = self.LR.ConstantTable
        fun = self.LR.FunctionTable
        p = TargetCode()
        tcode = p.GetTargetCode(MiddleCode, var, con, fun)
        self.display1.clear()
        self.display2.clear()
        self.display1.append(tcode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
