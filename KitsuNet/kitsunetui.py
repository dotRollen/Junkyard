# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(920, 508)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(920, 508))
        MainWindow.setMaximumSize(QtCore.QSize(920, 508))
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 921, 529))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(915, 520))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabConfigure = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabConfigure.sizePolicy().hasHeightForWidth())
        self.tabConfigure.setSizePolicy(sizePolicy)
        self.tabConfigure.setObjectName(_fromUtf8("tabConfigure"))
        self.btnRunConfigs = QtGui.QPushButton(self.tabConfigure)
        self.btnRunConfigs.setEnabled(True)
        self.btnRunConfigs.setGeometry(QtCore.QRect(700, 305, 201, 51))
        self.btnRunConfigs.setObjectName(_fromUtf8("btnRunConfigs"))
        self.tableTargets = QtGui.QTableWidget(self.tabConfigure)
        self.tableTargets.setEnabled(True)
        self.tableTargets.setGeometry(QtCore.QRect(0, 0, 907, 251))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableTargets.sizePolicy().hasHeightForWidth())
        self.tableTargets.setSizePolicy(sizePolicy)
        self.tableTargets.setObjectName(_fromUtf8("tableTargets"))
        self.tableTargets.setColumnCount(4)
        self.tableTargets.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableTargets.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableTargets.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableTargets.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableTargets.setHorizontalHeaderItem(3, item)
        self.tableTargets.horizontalHeader().setStretchLastSection(True)
        self.configProgress = QtGui.QProgressBar(self.tabConfigure)
        self.configProgress.setEnabled(False)
        self.configProgress.setGeometry(QtCore.QRect(701, 355, 199, 21))
        self.configProgress.setMaximum(0)
        self.configProgress.setProperty("value", 0)
        self.configProgress.setAlignment(QtCore.Qt.AlignCenter)
        self.configProgress.setOrientation(QtCore.Qt.Horizontal)
        self.configProgress.setInvertedAppearance(False)
        self.configProgress.setObjectName(_fromUtf8("configProgress"))
        self.groupBoxAddDevice = QtGui.QGroupBox(self.tabConfigure)
        self.groupBoxAddDevice.setGeometry(QtCore.QRect(0, 256, 691, 256))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxAddDevice.sizePolicy().hasHeightForWidth())
        self.groupBoxAddDevice.setSizePolicy(sizePolicy)
        self.groupBoxAddDevice.setMinimumSize(QtCore.QSize(691, 256))
        self.groupBoxAddDevice.setMaximumSize(QtCore.QSize(691, 256))
        self.groupBoxAddDevice.setAutoFillBackground(False)
        self.groupBoxAddDevice.setFlat(False)
        self.groupBoxAddDevice.setObjectName(_fromUtf8("groupBoxAddDevice"))
        self.formLayoutWidget = QtGui.QWidget(self.groupBoxAddDevice)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 671, 181))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout.setMargin(11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelSwitch = QtGui.QLabel(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSwitch.sizePolicy().hasHeightForWidth())
        self.labelSwitch.setSizePolicy(sizePolicy)
        self.labelSwitch.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelSwitch.setObjectName(_fromUtf8("labelSwitch"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelSwitch)
        self.comboSwitch = QtGui.QComboBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboSwitch.sizePolicy().hasHeightForWidth())
        self.comboSwitch.setSizePolicy(sizePolicy)
        self.comboSwitch.setObjectName(_fromUtf8("comboSwitch"))
        self.comboSwitch.addItem(_fromUtf8(""))
        self.comboSwitch.addItem(_fromUtf8(""))
        self.comboSwitch.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboSwitch)
        self.labelPort = QtGui.QLabel(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPort.sizePolicy().hasHeightForWidth())
        self.labelPort.setSizePolicy(sizePolicy)
        self.labelPort.setMinimumSize(QtCore.QSize(44, 0))
        self.labelPort.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPort.setObjectName(_fromUtf8("labelPort"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelPort)
        self.comboPort = QtGui.QComboBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboPort.sizePolicy().hasHeightForWidth())
        self.comboPort.setSizePolicy(sizePolicy)
        self.comboPort.setObjectName(_fromUtf8("comboPort"))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.comboPort.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboPort)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(2, QtGui.QFormLayout.LabelRole, spacerItem)
        self.chboxUpdate = QtGui.QCheckBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chboxUpdate.sizePolicy().hasHeightForWidth())
        self.chboxUpdate.setSizePolicy(sizePolicy)
        self.chboxUpdate.setObjectName(_fromUtf8("chboxUpdate"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.chboxUpdate)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(3, QtGui.QFormLayout.LabelRole, spacerItem1)
        self.chboxConfig = QtGui.QCheckBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chboxConfig.sizePolicy().hasHeightForWidth())
        self.chboxConfig.setSizePolicy(sizePolicy)
        self.chboxConfig.setObjectName(_fromUtf8("chboxConfig"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.chboxConfig)
        self.labelConfig = QtGui.QLabel(self.formLayoutWidget)
        self.labelConfig.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelConfig.sizePolicy().hasHeightForWidth())
        self.labelConfig.setSizePolicy(sizePolicy)
        self.labelConfig.setMinimumSize(QtCore.QSize(44, 0))
        self.labelConfig.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelConfig.setObjectName(_fromUtf8("labelConfig"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelConfig)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(5, QtGui.QFormLayout.LabelRole, spacerItem2)
        self.btnAddDevice = QtGui.QPushButton(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddDevice.sizePolicy().hasHeightForWidth())
        self.btnAddDevice.setSizePolicy(sizePolicy)
        self.btnAddDevice.setObjectName(_fromUtf8("btnAddDevice"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.btnAddDevice)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textboxConfigFile = QtGui.QLineEdit(self.formLayoutWidget)
        self.textboxConfigFile.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textboxConfigFile.sizePolicy().hasHeightForWidth())
        self.textboxConfigFile.setSizePolicy(sizePolicy)
        self.textboxConfigFile.setMinimumSize(QtCore.QSize(536, 20))
        self.textboxConfigFile.setObjectName(_fromUtf8("textboxConfigFile"))
        self.horizontalLayout.addWidget(self.textboxConfigFile)
        self.btnFilePicker = QtGui.QPushButton(self.formLayoutWidget)
        self.btnFilePicker.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFilePicker.sizePolicy().hasHeightForWidth())
        self.btnFilePicker.setSizePolicy(sizePolicy)
        self.btnFilePicker.setMinimumSize(QtCore.QSize(75, 20))
        self.btnFilePicker.setObjectName(_fromUtf8("btnFilePicker"))
        self.horizontalLayout.addWidget(self.btnFilePicker)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.btnRunConfigs.raise_()
        self.tableTargets.raise_()
        self.configProgress.raise_()
        self.groupBoxAddDevice.raise_()
        self.formLayoutWidget.raise_()
        self.verticalLayoutWidget.raise_()
        self.tabWidget.addTab(self.tabConfigure, _fromUtf8(""))
        self.tabTODO = QtGui.QWidget()
        self.tabTODO.setObjectName(_fromUtf8("tabTODO"))
        self.tabWidget.addTab(self.tabTODO, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "KitsuNet", None))
        self.btnRunConfigs.setText(_translate("MainWindow", "Run Configs", None))
        item = self.tableTargets.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Switch #", None))
        item = self.tableTargets.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Port #", None))
        item = self.tableTargets.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Update", None))
        item = self.tableTargets.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Config", None))
        self.configProgress.setFormat(_translate("MainWindow", "%v/%m", None))
        self.groupBoxAddDevice.setTitle(_translate("MainWindow", "Add Devices", None))
        self.labelSwitch.setText(_translate("MainWindow", "Switch #:", None))
        self.comboSwitch.setItemText(0, _translate("MainWindow", "1", None))
        self.comboSwitch.setItemText(1, _translate("MainWindow", "2", None))
        self.comboSwitch.setItemText(2, _translate("MainWindow", "3", None))
        self.labelPort.setText(_translate("MainWindow", "Port #:", None))
        self.comboPort.setItemText(0, _translate("MainWindow", "1", None))
        self.comboPort.setItemText(1, _translate("MainWindow", "2", None))
        self.comboPort.setItemText(2, _translate("MainWindow", "3", None))
        self.comboPort.setItemText(3, _translate("MainWindow", "4", None))
        self.comboPort.setItemText(4, _translate("MainWindow", "5", None))
        self.comboPort.setItemText(5, _translate("MainWindow", "6", None))
        self.comboPort.setItemText(6, _translate("MainWindow", "7", None))
        self.comboPort.setItemText(7, _translate("MainWindow", "8", None))
        self.comboPort.setItemText(8, _translate("MainWindow", "9", None))
        self.comboPort.setItemText(9, _translate("MainWindow", "10", None))
        self.comboPort.setItemText(10, _translate("MainWindow", "11", None))
        self.comboPort.setItemText(11, _translate("MainWindow", "12", None))
        self.comboPort.setItemText(12, _translate("MainWindow", "13", None))
        self.comboPort.setItemText(13, _translate("MainWindow", "14", None))
        self.comboPort.setItemText(14, _translate("MainWindow", "15", None))
        self.comboPort.setItemText(15, _translate("MainWindow", "16", None))
        self.comboPort.setItemText(16, _translate("MainWindow", "17", None))
        self.comboPort.setItemText(17, _translate("MainWindow", "18", None))
        self.comboPort.setItemText(18, _translate("MainWindow", "19", None))
        self.comboPort.setItemText(19, _translate("MainWindow", "20", None))
        self.comboPort.setItemText(20, _translate("MainWindow", "21", None))
        self.comboPort.setItemText(21, _translate("MainWindow", "22", None))
        self.comboPort.setItemText(22, _translate("MainWindow", "23", None))
        self.comboPort.setItemText(23, _translate("MainWindow", "24", None))
        self.chboxUpdate.setText(_translate("MainWindow", "Update ROMMON/IOS", None))
        self.chboxConfig.setText(_translate("MainWindow", "Send Configuration", None))
        self.labelConfig.setText(_translate("MainWindow", "Config:", None))
        self.btnAddDevice.setText(_translate("MainWindow", "Add Device", None))
        self.btnFilePicker.setText(_translate("MainWindow", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfigure), _translate("MainWindow", "Configure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTODO), _translate("MainWindow", "TODO", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
