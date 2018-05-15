########## Examples


############## Using method instead of Qt functions 

import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("PyQT Tuts!")
		self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
		self.home()

	def home(self):
		btn = QtGui.QPushButton("Quit", self) 
		btn.clicked.connect(self.close_application)
		btn.resize(100,100)
		btn.move(100,100)
		self.show()
	 
	def close_application(self):
		print("whoooaaa so custom!!")
		sys.exit()
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
	
	

# Open Folder or File
# import subprocess
# subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
# subprocess.Popen('explorer "C:\path\of\folder"')