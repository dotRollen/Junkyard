from PyQt4 import QtGui
import core_gui, timesheet


def clear():

	chkout_drpmn_device.setCurrentIndex(-1)
	chkout_new_name_in.clear()
	chkout_new_serial_in.clear()
	chkout_new_asset_in.clear()
	chkout_new_descr_in.clear()
	chkin_drpmn_name.setCurrentIndex(-1)
	chkin_reg_device_in.clear()
	chkin_reg_serial_in.clear()
	chkin_reg_asset_in.clear()
	chkin_reg_descr_in.clear()
	chkout_drpmn_name.setCurrentIndex(-1)
	chkout_reg_device_in.clear()
	chkout_reg_serial_in.clear()
	chkout_reg_asset_in.clear()
	chkout_reg_descr_in.clear()
	chkin_drpmn_device.setCurrentIndex(-1)
	chkin_new_serial_in.clear()
	chkin_new_asset_in.clear()
	chkin_new_descr_in.clear()
	chkin_new_name_in.clear()

def new_submit_chkin():

	chkin_new_name_text = str(chkin_new_name_in.displayText())
	chkin_new_device_text = str(chkin_drpmn_device.currentText())
	chkin_new_serial_text = str(chkin_new_serial_in.displayText())
	chkin_new_asset_text = str(chkin_new_asset_in.displayText())
	chkin_new_descr_text = str(chkin_new_descr_in.displayText())
	chkin_ndata = ( chkin_new_name_text, chkin_new_device_text, 
					chkin_new_descr_text, chkin_new_serial_text, 
					chkin_new_asset_text, time.strftime("%m/%d/%y %I:%M - %p") )
	matching_row_nbr = None
	log_name = None
	logged_in = True

	for rowNum in range(2, ws1.max_row + 1 ):

		log_name = ws1.cell(row=rowNum,column=1).value

	if log_name == chkin_new_name_text and chkin_new_serial_text > "" and chkin_new_asset_text > "":

		for rowNum in range(2, ws1.max_row + 1 ):
			log_name = ws1.cell(row=rowNum,column=1).value
			log_device = ws1.cell(row=rowNum,column=2).value
			log_serial = ws1.cell(row=rowNum,column=4).value
			log_asset = ws1.cell(row=rowNum,column=5).value

			if log_name == chkin_new_name_text and chkin_new_device_text == log_device and chkin_new_serial_text == log_serial and chkin_new_asset_text == log_asset:
				matching_row_nbr = rowNum
				break

			else:
				logged_in = False

		if matching_row_nbr is not None:
			ws1.cell(row=matching_row_nbr, column=6).value = str(time.strftime("%m/%d/%y %I:%M - %p"))
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check In - UPDATE SUCCESSFUL", chkin_new_device_text + " has been succesfully checked in by " + chkin_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
			clear()

		elif logged_in == False: 
			ws1.append(chkin_ndata)
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check In - DEVICE ADDED SUCCESSFULLY", chkin_new_device_text + " has been succesfully checked in by " + chkin_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ". Other additional devices have been recently logged with this name. Please make sure all devices are accounted for.")
			clear()
		else:
			print "pizza time"

	elif len(chkin_new_name_text) == "" or chkin_new_serial_text == "" or chkin_new_asset_text == "":
		QtGui.QMessageBox.about(centralwidget, "Device Check In - INCOMPLETE!","Required: Visitor/Employee name, devie, serial and asset tag. Please make sure all the information is filled in.")

	else:
		ws1.append(chkin_ndata)
		wb.save(filename = active_workbook)
		QtGui.QMessageBox.about(centralwidget, "Device Check In - COMPLETE", chkin_new_device_text + " has been succesfully checked in by " + chkin_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
		clear()

def chkin_reg_autofill(self, currentIndex):

	if currentIndex >= -1: 

		chkin_reg_device_in.setText(var[currentIndex][0])
		chkin_reg_serial_in.setText(var[currentIndex][1])
		chkin_reg_asset_in.setText(var[currentIndex][2])
		chkin_reg_descr_in.setText(var[currentIndex][3])
	
def reg_submit_chkin(self):

	chkin_reg_name_text = str(chkin_drpmn_name.currentText())
	chkin_reg_device_text = str(chkin_reg_device_in.displayText())
	chkin_reg_serial_text = str(chkin_reg_serial_in.displayText())
	chkin_reg_asset_text = str(chkin_reg_asset_in.displayText())
	chkin_reg_descr_text = str(chkin_reg_descr_in.displayText())
	chkin_rdata = ( chkin_reg_name_text, chkin_reg_device_text, chkin_reg_descr_text, 
					chkin_reg_serial_text, chkin_reg_asset_text, time.strftime("%m/%d/%y %I:%M - %p") )
	matching_row_nbr = None
	log_name = None
	logged_in = True

	for rowNum in range(2, ws1.max_row + 1 ):

		log_name = ws1.cell(row=rowNum,column=1).value

	if log_name == chkin_reg_name_text and chkin_reg_serial_text > "" and chkin_reg_asset_text > "":

		for rowNum in range(2, ws1.max_row + 1 ):

			log_name = ws1.cell(row=rowNum,column=1).value
			log_device = ws1.cell(row=rowNum,column=2).value
			log_serial = ws1.cell(row=rowNum,column=4).value
			log_asset = ws1.cell(row=rowNum,column=5).value

			if log_name == chkin_reg_name_text and chkin_reg_device_text == log_device and chkin_reg_serial_text == log_serial and chkin_reg_asset_text == log_asset:

				matching_row_nbr = rowNum
				
				break
			else:

				logged_in = False

		if matching_row_nbr is not None:

			ws1.cell(row=matching_row_nbr, column=6).value = str(time.strftime("%m/%d/%y %I:%M - %p"))
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check In - UPDATE SUCCESSFUL", chkin_reg_device_text + " has been succesfully checked in by " + chkin_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
			clear()

		elif logged_in == False: 

			ws1.append(chkin_rdata)
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check In - DEVICE ADDED SUCCESSFULLY", chkin_reg_device_text + " has been succesfully checked in by " + chkin_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ". Other additional devices have been recently logged with this name. Please make sure all devices are accounted for.")
			clear()

	elif len(chkin_reg_name_text) == "" or chkin_reg_serial_text == "" or chkin_reg_asset_text == "":

		QtGui.QMessageBox.about(centralwidget, "Device Check In - INCOMPLETE!","Required: Visitor/Employee name, devie, serial and asset tag. Please make sure all the information is filled in.")

	else:

		ws1.append(chkin_rdata)
		wb.save(filename = active_workbook)
		QtGui.QMessageBox.about(centralwidget, "Device Check In - COMPLETE", chkin_reg_device_text + " has been succesfully checked in by " + chkin_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
		clear()
	
def new_submit_chkout(self):

	chkout_new_name_text = str(chkout_new_name_in.displayText())
	chkout_new_device_text = str(chkout_drpmn_device.currentText())
	chkout_new_serial_text = str(chkout_new_serial_in.displayText())
	chkout_new_asset_text = str(chkout_new_asset_in.displayText())
	chkout_new_descr_text = str(chkout_new_descr_in.displayText())
	chkout_ndata = ( chkout_new_name_text, chkout_new_device_text, chkout_new_descr_text,
		chkout_new_serial_text, chkout_new_asset_text, '', time.strftime("%m/%d/%y %I:%M - %p"))
	matching_row_nbr = None
	log_name = None
	logged_in = True

	for rowNum in range(2, ws1.max_row + 1 ):

		log_name = ws1.cell(row=rowNum,column=1).value

	if log_name == chkout_new_name_text and chkout_new_serial_text > "" and chkout_new_asset_text > "":

		for rowNum in range(2, ws1.max_row + 1 ):

			log_name = ws1.cell(row=rowNum,column=1).value
			log_device = ws1.cell(row=rowNum,column=2).value
			log_serial = ws1.cell(row=rowNum,column=4).value
			log_asset = ws1.cell(row=rowNum,column=5).value

			if log_name == chkout_new_name_text and chkout_new_device_text == log_device and chkout_new_serial_text == log_serial and chkout_new_asset_text == log_asset:

				matching_row_nbr = rowNum
				break

			else:

				logged_in = False

		if matching_row_nbr is not None:

			ws1.cell(row=matching_row_nbr, column=7).value = str(time.strftime("%m/%d/%y %I:%M - %p"))
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check Out - UPDATE SUCCESSFUL", chkout_new_device_text + " has been succesfully checked out by " + chkout_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
			clear()

		elif logged_in == False: 

			ws1.append(chkout_ndata)
			wb.save(filename = active_workbook)
			QtGui.QMessageBox.about(centralwidget, "Device Check Out - DEVICE ADDED SUCCESSFULLY", chkout_new_device_text + " has been succesfully checked out by " + chkout_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ". Other additional devices have been recently logged with this name. Please make sure all devices are accounted for.")
			clear()

	elif len(chkout_new_name_text) == "" or chkout_new_serial_text == "" or chkout_new_asset_text == "":


		QtGui.QMessageBox.about(centralwidget, "Device Check Out - INCOMPLETE!","Required: Visitor/Employee name, devie, serial and asset tag. Please make sure all the information is filled in.")
	else:

		ws1.append(chkout_ndata)
		wb.save(filename = active_workbook)
		QtGui.QMessageBox.about(centralwidget, "Device Check Out - COMPLETE", chkout_new_device_text + " has been succesfully checked out by " + chkout_new_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
		clear()

def chkout_reg_autofill(self, currentIndex):

	if currentIndex >= -1: 

		chkout_reg_device_in.setText(var[currentIndex][0])
		chkout_reg_serial_in.setText(var[currentIndex][1])
		chkout_reg_asset_in.setText(var[currentIndex][2])
		chkout_reg_descr_in.setText(var[currentIndex][3])

def reg_submit_chkout(self):

	# chkout_reg_name_text = str(chkout_drpmn_name.currentText())
	# chkout_reg_device_text = str(chkout_reg_device_in.displayText())
	# chkout_reg_serial_text = str(chkout_reg_serial_in.displayText())
	# chkout_reg_asset_text = str(chkout_reg_asset_in.displayText())
	# chkout_reg_descr_text = str(chkout_reg_descr_in.displayText())
	# chkout_rdata = ( chkout_reg_name_text, chkout_reg_device_text, chkout_reg_descr_text, 
	# 				chkout_reg_serial_text, chkout_reg_asset_text, '', time.strftime("%m/%d/%y %I:%M - %p") )
	# matching_row_nbr = None
	# log_name = None
	# logged_in = True

	# for rowNum in range(2, ws1.max_row + 1 ):

	# 	log_name = ws1.cell(row=rowNum,column=1).value
	# 	log_device = ws1.cell(row=rowNum,column=2).value

	# if log_name == chkout_reg_name_text and chkout_reg_serial_text > "" and chkout_reg_asset_text > "":

	# 	for rowNum in range(2, ws1.max_row + 1 ):

	# 		log_name = ws1.cell(row=rowNum,column=1).value
	# 		log_device = ws1.cell(row=rowNum,column=2).value
	# 		log_serial = ws1.cell(row=rowNum,column=4).value
	# 		log_asset = ws1.cell(row=rowNum,column=5).value

	# 		if log_name == chkout_reg_name_text and chkout_reg_device_text == log_device and chkout_reg_serial_text == log_serial and chkout_reg_asset_text == log_asset:

	# 			matching_row_nbr = rowNum
	# 			break

	# 		else:
	# 			logged_in = False

	# 	if matching_row_nbr is not None:

	# 		ws1.cell(row=matching_row_nbr, column=7).value = str(time.strftime("%m/%d/%y %I:%M - %p"))
	# 		wb.save(filename = active_workbook)
	# 		QtGui.QMessageBox.about(centralwidget, "Device Check Out - UPDATE SUCCESSFUL", chkout_reg_device_text + " has been succesfully checked out by " + chkout_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
	# 		clear()

	# 	elif logged_in == False: 

	# 		ws1.append(chkout_rdata)
	# 		wb.save(filename = active_workbook)
	# 		QtGui.QMessageBox.about(centralwidget, "Device Check Out - DEVICE ADDED SUCCESSFULLY", chkout_reg_device_text + " has been succesfully checked out by " + chkout_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ". Other additional devices have been recently logged with this name. Please make sure all devices are accounted for.")
	clear()

	elif len(chkout_reg_name_text) == "" or chkout_reg_device_text == "" or chkout_reg_serial_text == "" or chkout_reg_asset_text == "":

		QtGui.QMessageBox.about(centralwidget, "Device Check Out - INCOMPLETE!","Required: Visitor/Employee name, devie, serial and asset tag. Please make sure all the information is filled in.")
		
	else:

		ws1.append(chkout_rdata)
		wb.save(filename = active_workbook)
		QtGui.QMessageBox.about(centralwidget, "Device Check Out - COMPLETE", chkout_reg_device_text + " has been succesfully checked out by " + chkout_reg_name_text + " on " + time.strftime("%m/%d/%y %I:%M - %p") + ".")
		clear()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = GUI.Ui_SHICheckIn()
	window.show()
	sys.exit(app.exec_())



# self.chkin_drpmn_device.setItemText(0, _translate("SHICheckIn", "HP Laptop", None))
# self.chkin_drpmn_device.addItem(_fromUtf8(""))

# self.chkin_drpmn_name.setItemText(0, _translate("SHICheckIn", "Abdellah Maarouf", None))
# self.chkin_drpmn_name.addItem(_fromUtf8(""))

# self.chkout_drpmn_name.setItemText(0, _translate("SHICheckIn", "Abdellah Maarouf", None))
# self.chkout_drpmn_name.addItem(_fromUtf8(""))

# self.chkout_drpmn_device.setItemText(0, _translate("SHICheckIn", "HP Laptop", None))
# self.chkout_drpmn_device.addItem(_fromUtf8(""))

