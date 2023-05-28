# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tt.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSplitter, QTreeWidget
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(843, 643)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # 颜色搭配：https://www.xiaohongshu.com/explore/6237ce1c000000000102a35f
        # http://www.360doc.com/content/09/0731/11/59625_4571056.shtml
        MainWindow.setStyleSheet('QWidget{background-color:%s}' % QColor("#006699").name())
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5F5").name())
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5F5").name())
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5F5").name())

        self.treeView = QtWidgets.QTreeView(self.centralwidget)

        self.treeView.setObjectName("treeView")
        self.treeView.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5F5").name())
        self.tree = QTreeWidget(self.centralwidget)
        self.tree.setStyleSheet('QWidget{background-color:%s}' % QColor("#F5F5F5").name())

        self.splitter2 = QSplitter(Qt.Vertical)
        # self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.textEdit_3)
        self.splitter2.addWidget(self.textEdit_2)

        self.splitter3 = QSplitter(Qt.Vertical)
        self.splitter3.addWidget(self.tree)
        self.splitter3.addWidget(self.treeView)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.splitter3)
        # self.splitter1.addWidget(self.tree)
        self.splitter1.addWidget(self.textEdit)
        # self.splitter1.addWidget(self.textEdit_2)
        self.splitter1.addWidget(self.splitter2)

        # self.splitter3=QSplitter(Qt.Vertical)
        # self.splitter3.addWidget(self.tree)
        # self.splitter3.addWidget(self.splitter1)

        self.gridLayout.addWidget(self.splitter1, 0, 1, 0, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 843, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")
        self.menu_cifa = QtWidgets.QMenu(self.menubar)
        self.menu_cifa.setObjectName("menu_cifa")
        self.menu_yufa = QtWidgets.QMenu(self.menubar)
        self.menu_yufa.setObjectName("menu_yufa")
        self.menu_Quaternion = QtWidgets.QMenu(self.menubar)
        self.menu_Quaternion.setObjectName("menu_Quaternion")
        self.menu_O = QtWidgets.QMenu(self.menubar)
        self.menu_O.setObjectName("menu_O")
        self.menu_H = QtWidgets.QMenu(self.menubar)
        self.menu_H.setObjectName("menu_H")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOPEN = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ICON/2931141_archive_folder_storage_data_files.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOPEN.setIcon(icon)
        self.actionOPEN.setObjectName("actionOPEN")
        self.actionSAVE = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("ICON/2931167_documents_doc_document_sheet_file_text_archive.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSAVE.setIcon(icon1)
        self.actionSAVE.setObjectName("actionSAVE")
        self.actionCLOSE = QtWidgets.QAction(MainWindow)
        self.actionCLOSE.setObjectName("actionCLOSE")
        self.actionSAVE_ANOTHER = QtWidgets.QAction(MainWindow)
        self.actionSAVE_ANOTHER.setObjectName("actionSAVE_ANOTHER")
        self.actionundo = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ICON/2931166_left_arrow_back_undo_navigation.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionundo.setIcon(icon2)
        self.actionundo.setObjectName("actionundo")
        self.actionredo = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ICON/2931165_navigation_forward_redo_arrow_right.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionredo.setIcon(icon3)
        self.actionredo.setObjectName("actionredo")
        self.actioncut = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap("ICON/2931169_hair_scissor_cut_clippers_shear_scissors_saloon.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncut.setIcon(icon4)
        self.actioncut.setObjectName("actioncut")
        self.actioncopy = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ICON/2931153_clipboard_duplicate_copy_clone_multiply.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncopy.setIcon(icon5)
        self.actioncopy.setObjectName("actioncopy")
        self.actionpaste = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ICON/9958201.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionpaste.setIcon(icon6)
        self.actionpaste.setObjectName("actionpaste")
        self.actiondelete = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("ICON/2931168_garbage_trash_bin_delete_remove.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondelete.setIcon(icon7)
        self.actiondelete.setObjectName("actiondelete")
        self.actionselect_all = QtWidgets.QAction(MainWindow)
        self.actionselect_all.setObjectName("actionselect_all")
        self.actionstate_transition = QtWidgets.QAction(MainWindow)
        self.actionstate_transition.setObjectName("actionstate_transition")
        self.actionPLY = QtWidgets.QAction(MainWindow)
        self.actionPLY.setObjectName("actionPLY")
        self.actionfrom_up_to_down = QtWidgets.QAction(MainWindow)
        self.actionfrom_up_to_down.setObjectName("actionfrom_up_to_down")
        self.actionfrom_down_to_up = QtWidgets.QAction(MainWindow)
        self.actionfrom_down_to_up.setObjectName("actionfrom_down_to_up")
        self.action_middle_code = QtWidgets.QAction(MainWindow)
        self.action_middle_code.setObjectName("action_middle_code")
        self.actionup_start = QtWidgets.QAction(MainWindow)
        self.actionup_start.setObjectName("actionup_start")
        self.actionHELP_CHM = QtWidgets.QAction(MainWindow)
        self.actionHELP_CHM.setObjectName("actionHELP_CHM")
        self.actionitalic = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("ICON/9022896_text_italic_duotone_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionitalic.setIcon(icon8)
        self.actionitalic.setObjectName("actionitalic")
        self.actionbold = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("ICON/8666793_bold_text_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbold.setIcon(icon9)
        self.actionbold.setObjectName("actionbold")
        self.actionincrease_font = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("ICON/6137851_format_increase_text_edit_editor_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionincrease_font.setIcon(icon10)
        self.actionincrease_font.setObjectName("actionincrease_font")
        self.actiondecrease_font = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("ICON/6137854_decrease_document_text_edit_editor_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actiondecrease_font.setIcon(icon11)
        self.actiondecrease_font.setObjectName("actiondecrease_font")
        self.actionunderline = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("ICON/9057157_format_color_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionunderline.setIcon(icon12)
        self.actionunderline.setObjectName("actionunderline")
        self.actiongreen_font = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("ICON/312566_green_m&m_chocolate_color_colour_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actiongreen_font.setIcon(icon13)
        self.actiongreen_font.setObjectName("actiongreen_font")
        self.actionred_font = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("ICON/312570_m&m_red_chocolate_color_colour_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionred_font.setIcon(icon14)
        self.actionred_font.setObjectName("actionred_font")
        self.actionpurple_font = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("ICON/312571_m&m_purple_chocolate_color_colour_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionpurple_font.setIcon(icon15)
        self.actionpurple_font.setObjectName("actionpurple_font")
        self.actionorange_font = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("ICON/312580_m&m_orange_chocolate_color_colour_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionorange_font.setIcon(icon16)
        self.actionorange_font.setObjectName("actionorange_font")
        self.actionblue_font = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("ICON/312581_blue_m&m_chocolate_color_colour_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionblue_font.setIcon(icon17)
        self.actionblue_font.setObjectName("actionblue_font")
        self.actionNFA_DFA = QtWidgets.QAction(MainWindow)
        self.actionNFA_DFA.setObjectName("actionNFA_DFA")
        self.actionLL1 = QtWidgets.QAction(MainWindow)
        self.actionLL1.setObjectName("actionLL1")
        self.actionsuanfu_first = QtWidgets.QAction(MainWindow)
        self.actionsuanfu_first.setObjectName("actionsuanfu_first")
        self.actionDAG = QtWidgets.QAction(MainWindow)
        self.actionDAG.setObjectName("actionDAG")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionhuibian_code = QtWidgets.QAction(MainWindow)
        self.actionhuibian_code.setObjectName("actionhuibian_code")
        self.menu.addAction(self.actionOPEN)
        self.menu.addAction(self.actionSAVE)
        self.menu.addAction(self.actionCLOSE)
        self.menu.addAction(self.actionSAVE_ANOTHER)
        self.menuedit.addAction(self.actionundo)
        self.menuedit.addAction(self.actionredo)
        self.menuedit.addAction(self.actioncut)
        self.menuedit.addAction(self.actioncopy)
        self.menuedit.addAction(self.actionpaste)
        self.menuedit.addAction(self.actiondelete)
        self.menuedit.addAction(self.actionselect_all)
        self.menu_cifa.addAction(self.actionstate_transition)
        self.menu_cifa.addAction(self.actionPLY)
        self.menu_cifa.addAction(self.actionNFA_DFA)
        self.menu_yufa.addAction(self.actionfrom_up_to_down)
        self.menu_yufa.addAction(self.actionfrom_down_to_up)
        self.menu_yufa.addAction(self.actionLL1)
        self.menu_yufa.addAction(self.actionsuanfu_first)
        self.menu_Quaternion.addAction(self.action_middle_code)
        self.menu_Quaternion.addAction(self.actionDAG)
        self.menu_O.addAction(self.actionhuibian_code)
        self.menu_H.addAction(self.actionHELP_CHM)
        self.menu_H.addAction(self.action)
        self.menu_2.addAction(self.actionitalic)
        self.menu_2.addAction(self.actionbold)
        self.menu_2.addAction(self.actionincrease_font)
        self.menu_2.addAction(self.actiondecrease_font)
        self.menu_2.addAction(self.actionunderline)
        self.menu_2.addAction(self.actiongreen_font)
        self.menu_2.addAction(self.actionred_font)
        self.menu_2.addAction(self.actionpurple_font)
        self.menu_2.addAction(self.actionorange_font)
        self.menu_2.addAction(self.actionblue_font)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_cifa.menuAction())
        self.menubar.addAction(self.menu_yufa.menuAction())
        self.menubar.addAction(self.menu_Quaternion.menuAction())
        self.menubar.addAction(self.menu_O.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())
        self.toolBar.addAction(self.actionOPEN)
        self.toolBar.addAction(self.actionSAVE)
        self.toolBar.addAction(self.actionundo)
        self.toolBar.addAction(self.actionredo)
        self.toolBar.addAction(self.actioncut)
        self.toolBar.addAction(self.actioncopy)
        self.toolBar.addAction(self.actionpaste)
        self.toolBar.addAction(self.actiondelete)
        self.toolBar.addAction(self.actionitalic)
        self.toolBar.addAction(self.actionbold)
        self.toolBar.addAction(self.actionincrease_font)
        self.toolBar.addAction(self.actiondecrease_font)
        self.toolBar.addAction(self.actionunderline)
        self.toolBar.addAction(self.actiongreen_font)
        self.toolBar.addAction(self.actionred_font)
        self.toolBar.addAction(self.actionpurple_font)
        self.toolBar.addAction(self.actionorange_font)
        self.toolBar.addAction(self.actionblue_font)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件(F)"))
        self.menuedit.setTitle(_translate("MainWindow", "编辑(E)"))
        self.menu_cifa.setTitle(_translate("MainWindow", "词法分析(W)"))
        self.menu_yufa.setTitle(_translate("MainWindow", "语法分析(P)"))
        self.menu_Quaternion.setTitle(_translate("MainWindow", "中间代码(M)"))
        self.menu_O.setTitle(_translate("MainWindow", "目标代码生成(O)"))
        self.menu_H.setTitle(_translate("MainWindow", "帮助(H)"))
        self.menu_2.setTitle(_translate("MainWindow", "视图(V)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOPEN.setText(_translate("MainWindow", "打开"))
        self.actionOPEN.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSAVE.setText(_translate("MainWindow", "保存"))
        self.actionSAVE.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionCLOSE.setText(_translate("MainWindow", "关闭"))
        self.actionSAVE_ANOTHER.setText(_translate("MainWindow", "另存为"))
        self.actionundo.setText(_translate("MainWindow", "undo"))
        self.actionundo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionredo.setText(_translate("MainWindow", "redo"))
        self.actionredo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actioncut.setText(_translate("MainWindow", "cut"))
        self.actioncopy.setText(_translate("MainWindow", "copy"))
        self.actioncopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionpaste.setText(_translate("MainWindow", "paste"))
        self.actionpaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actiondelete.setText(_translate("MainWindow", "delete"))
        self.actiondelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionselect_all.setText(_translate("MainWindow", "select_all"))
        self.actiondelete.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionstate_transition.setText(_translate("MainWindow", "手动词法分析(递归下降)"))
        self.actionPLY.setText(_translate("MainWindow", "自动词法分析(LR)"))
        self.actionfrom_up_to_down.setText(_translate("MainWindow", "递归下降语法分析"))
        self.actionfrom_down_to_up.setText(_translate("MainWindow", "LR语法分析"))
        self.action_middle_code.setText(_translate("MainWindow", "中间代码"))
        self.actionup_start.setText(_translate("MainWindow", "自上而下"))
        self.actionHELP_CHM.setText(_translate("MainWindow", "HELP_CHM"))
        self.actionitalic.setText(_translate("MainWindow", "斜体"))
        self.actionitalic.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionbold.setText(_translate("MainWindow", "加粗"))
        self.actionbold.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionincrease_font.setText(_translate("MainWindow", "增大字号"))
        self.actionincrease_font.setShortcut(_translate("MainWindow", "Ctrl+]"))
        self.actiondecrease_font.setText(_translate("MainWindow", "减小字号"))
        self.actiondecrease_font.setShortcut(_translate("MainWindow", "Ctrl+["))
        self.actionunderline.setText(_translate("MainWindow", "下划线"))
        self.actionunderline.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.actiongreen_font.setText(_translate("MainWindow", "绿色字体"))
        self.actionred_font.setText(_translate("MainWindow", "红色字体"))
        self.actionpurple_font.setText(_translate("MainWindow", "紫色字体"))
        self.actionorange_font.setText(_translate("MainWindow", "橙色字体"))
        self.actionblue_font.setText(_translate("MainWindow", "蓝色字体"))
        self.actionNFA_DFA.setText(_translate("MainWindow", "NFA_DFA"))
        self.actionLL1.setText(_translate("MainWindow", "LL1预测分析"))
        self.actionsuanfu_first.setText(_translate("MainWindow", "算符优先分析"))
        self.actionDAG.setText(_translate("MainWindow", "DAG优化"))
        self.action.setText(_translate("MainWindow", "关于"))
        self.actionhuibian_code.setText(_translate("MainWindow", "目标代码"))
