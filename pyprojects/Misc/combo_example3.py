import sys
from PyQt4.QtGui import *

item_2 = ['cheese','pepperoni']

class Widget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle("Tut #12")
		
		# Widgets
		vbox = QVBoxLayout(self)
		hbox = QHBoxLayout()
		
		self.combo = QComboBox()
		list = ['item_1', 'item_2', 'item_3']
		
		# for item in list:
		self.combo.blockSignals(True)
		self.combo.clear()
		self.combo.addItems(sorted(list))
		self.combo.setCurrentIndex(-1)
		self.combo.blockSignals(False)
		# self.combo.setCurrentIndex(intLastSavedState1)
		self.line = QLineEdit()
		self.labelCombo= QLabel('')
		self.labelLine = QLabel('')
		
		hbox.addWidget(self.labelCombo)
		hbox.addWidget(self.labelLine)
		
		vbox.addWidget(self.combo)
		vbox.addWidget(self.line)
		vbox.addLayout(hbox)
		
		# Connection
		self.connect(self.combo, self.SIGNAL("currentIndexChanged(const QString&)"), self.line)

	def user_information(self):
		user = self.combo.currentText()
		print user
		
	def chkout_reg_autofill(self):
		self.line.setText(user_information)

		
app = QApplication([])
w = Widget()
w.show()
sys.exit(app.exec_())