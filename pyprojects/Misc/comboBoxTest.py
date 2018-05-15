# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/nas/projects/development/pipeline/utilities/testWindow/ui/comboBoxTest.ui'
#
# Created: Wed Jun 11 15:36:21 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(821, 259)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(130, 70, 611, 80))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.comboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
		self.comboBox.setObjectName("comboBox")
		self.horizontalLayout.addWidget(self.comboBox)
		spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.comboBox_2 = QtGui.QComboBox(self.horizontalLayoutWidget)
		self.comboBox_2.setObjectName("comboBox_2")
		self.horizontalLayout.addWidget(self.comboBox_2)
		spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem2)
		self.comboBox_3 = QtGui.QComboBox(self.horizontalLayoutWidget)
		self.comboBox_3.setObjectName("comboBox_3")
		self.horizontalLayout.addWidget(self.comboBox_3)
		spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem3)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 26))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.comboBox.addItem("1")
		self.comboBox.addItem("2")
		self.comboBox.addItem("3")
		
		self.comboBox_2.addItem("a")
		self.comboBox_2.addItem("b")
		self.comboBox_2.addItem("c")

		self.comboBox_3.addItem("V")
		self.comboBox_3.addItem("VI")
		self.comboBox_3.addItem("VII")
		
		self.retranslateUi(MainWindow)
		QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.abcdef)
		QtCore.QObject.connect(self.comboBox_2, QtCore.SIGNAL("currentIndexChanged(int)"), self.ghhijkl)
		
		
#		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
		
	def abcdef(self):
		print "in abcdef ..."
		if self.comboBox.currentText() == "1":
			self.comboBox_2.setCurrentIndex(2)
		if self.comboBox.currentText() == "3":
			self.comboBox_2.setCurrentIndex(1)
		if self.comboBox.currentText() == "2":
			self.comboBox_2.setCurrentIndex(3)


		
	def ghhijkl(self):
		print "in ghijkl ..."
		if self.comboBox_2.currentText() == "c":
			self.comboBox_3.setCurrentIndex(2)
		if self.comboBox_2.currentText() == "a":
			self.comboBox_3.setCurrentIndex(1)
		if self.comboBox_2.currentText() == "b":
			self.comboBox_3.setCurrentIndex(3)


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

