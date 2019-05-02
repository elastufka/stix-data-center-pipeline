# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(956, 763)
        MainWindow.setMaximumSize(QtCore.QSize(323232, 323232))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/images/app.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_4)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter_3 = QtWidgets.QSplitter(self.tab)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.listView = QtWidgets.QListView(self.splitter_2)
        self.listView.setMinimumSize(QtCore.QSize(0, 500))
        self.listView.setMaximumSize(QtCore.QSize(450, 16777215))
        self.listView.setObjectName("listView")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableWidget = QtWidgets.QTableWidget(self.splitter)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 2000))
        self.tableWidget.setBaseSize(QtCore.QSize(0, 200))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setHighlightSections(True)
        self.horizontalLayout_2.addWidget(self.splitter_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.xaxisComboBox = QtWidgets.QComboBox(self.tab_2)
        self.xaxisComboBox.setObjectName("xaxisComboBox")
        self.xaxisComboBox.addItem("")
        self.xaxisComboBox.addItem("")
        self.xaxisComboBox.addItem("")
        self.gridLayout.addWidget(self.xaxisComboBox, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.comboBox.setModelColumn(0)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.paramNameEdit = QtWidgets.QLineEdit(self.tab_2)
        self.paramNameEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.paramNameEdit.setObjectName("paramNameEdit")
        self.gridLayout.addWidget(self.paramNameEdit, 0, 3, 1, 1)
        self.plotButton = QtWidgets.QPushButton(self.tab_2)
        self.plotButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.plotButton.setObjectName("plotButton")
        self.gridLayout.addWidget(self.plotButton, 0, 10, 1, 1)
        self.savePlotButton = QtWidgets.QPushButton(self.tab_2)
        self.savePlotButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.savePlotButton.setObjectName("savePlotButton")
        self.gridLayout.addWidget(self.savePlotButton, 0, 11, 1, 1)
        self.descLabel = QtWidgets.QLabel(self.tab_2)
        self.descLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.descLabel.setMaximumSize(QtCore.QSize(0, 16777215))
        self.descLabel.setText("")
        self.descLabel.setObjectName("descLabel")
        self.gridLayout.addWidget(self.descLabel, 0, 6, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 7, 1, 1)
        self.styleEdit = QtWidgets.QLineEdit(self.tab_2)
        self.styleEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.styleEdit.setObjectName("styleEdit")
        self.gridLayout.addWidget(self.styleEdit, 0, 8, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 9, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.dockWidget_2 = QtWidgets.QDockWidget(self.splitter_4)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget_2 = QtWidgets.QListWidget(self.dockWidgetContents_2)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout_3.addWidget(self.listWidget_2)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        self.horizontalLayout_4.addWidget(self.splitter_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuAction = QtWidgets.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menu_Tools = QtWidgets.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        self.actionPrevious.setMenuRole(QtWidgets.QAction.AboutQtRole)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionSet_IDB = QtWidgets.QAction(MainWindow)
        self.actionSet_IDB.setObjectName("actionSet_IDB")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLog = QtWidgets.QAction(MainWindow)
        self.actionLog.setObjectName("actionLog")
        self.action_Plot = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/images/graph.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Plot.setIcon(icon1)
        self.action_Plot.setObjectName("action_Plot")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/images/paste.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon2)
        self.actionPaste.setObjectName("actionPaste")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addAction(self.actionExit)
        self.menu_Help.addAction(self.actionAbout)
        self.menuAction.addAction(self.actionPrevious)
        self.menuAction.addAction(self.actionNext)
        self.menuAction.addAction(self.actionLog)
        self.menuSetting.addAction(self.actionSet_IDB)
        self.menu_Tools.addAction(self.action_Plot)
        self.menu_Tools.addAction(self.actionPaste)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPrevious)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Plot)
        self.toolBar.addAction(self.actionPaste)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "STIX data parser and viewer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Packets"))
        self.tab_2.setToolTip(_translate("MainWindow", "plot parameters\n"
""))
        self.xaxisComboBox.setItemText(0, _translate("MainWindow", "Parameter order as X"))
        self.xaxisComboBox.setItemText(1, _translate("MainWindow", "Timestamps as X"))
        self.xaxisComboBox.setItemText(2, _translate("MainWindow", "Histogram"))
        self.label_4.setText(_translate("MainWindow", "Type:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "the same packet"))
        self.comboBox.setItemText(1, _translate("MainWindow", "all packets"))
        self.label_2.setText(_translate("MainWindow", "In"))
        self.plotButton.setText(_translate("MainWindow", "Plot"))
        self.savePlotButton.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Data source:"))
        self.label_3.setText(_translate("MainWindow", "Curve Style:"))
        self.styleEdit.setText(_translate("MainWindow", "o-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Plot"))
        self.dockWidget_2.setWindowTitle(_translate("MainWindow", "Log"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuAction.setTitle(_translate("MainWindow", "&View"))
        self.menuSetting.setTitle(_translate("MainWindow", "&Settings"))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionSet_IDB.setText(_translate("MainWindow", "Set &IDB"))
        self.actionSave.setText(_translate("MainWindow", "Sa&ve"))
        self.actionLog.setText(_translate("MainWindow", "Show Log"))
        self.action_Plot.setText(_translate("MainWindow", "&Plot"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setToolTip(_translate("MainWindow", "Read raw data from the clipboard"))

import mainwindow_rc5
