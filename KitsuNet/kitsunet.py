from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys, time

import kitsunetui, kitsunetutils

"""
class DeviceTask(object):
    def __init__(self, opengear_num, opengear_port, do_update, do_config, config_file=None):
        self.opengear_num = opengear_num
        self.opengear_port = opengear_port
        self.do_update = do_update
        self.do_config = do_config
        self.config_file = config_file
"""

class KitsuNetApp(QtGui.QMainWindow, kitsunetui.Ui_MainWindow):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.devices = []

        self.configProgress.hide()
        self.btnFilePicker.clicked.connect(self.browse_folder)
        self.btnAddDevice.clicked.connect(self.add_device)
        self.btnRunConfigs.clicked.connect(self.run_configs)
        self.chboxConfig.stateChanged.connect(self.state_changed)

    def state_changed(self, int):
        self.textboxConfigFile.setEnabled(self.chboxConfig.isChecked())
        self.btnFilePicker.setEnabled(self.chboxConfig.isChecked())

    def browse_folder(self):
        config_file = QtGui.QFileDialog.getOpenFileName(self, "Choose config file")
        if config_file:
            self.textboxConfigFile.setText(config_file)

    def add_device(self):
        switch = self.comboSwitch.currentText()
        port = self.comboPort.currentText()
        config_file = self.textboxConfigFile.text()
        do_update = self.chboxUpdate.isChecked()
        do_config = self.chboxConfig.isChecked()

        # If config is checked but no config file, error.
        if self.chboxConfig.isChecked() and not config_file:
            QtGui.QMessageBox.critical(self, "No Configuration Chosen",
                                        "You must choose a configuration file.",
                                        QtGui.QMessageBox.Ok)
 
        # Else add device to the list
        else:
            self.devices.append((str(switch), str(port), do_update, do_config, str(config_file)))

            row = self.tableTargets.rowCount()
            self.tableTargets.insertRow(row)
            self.tableTargets.setItem(row , 0, QtGui.QTableWidgetItem('OpenGear{}'.format(switch)))
            self.tableTargets.setItem(row , 1, QtGui.QTableWidgetItem(port))
            self.tableTargets.setItem(row , 2, QtGui.QTableWidgetItem(str(do_update)))
            if config_file:
                self.tableTargets.setItem(row , 3, QtGui.QTableWidgetItem(config_file.split('/')[-1]))
            else:
                self.tableTargets.setItem(row , 3, QtGui.QTableWidgetItem('No configuration'))

            self.textboxConfigFile.clear()
                

    def run_configs(self):
        if len(self.devices) > 0:
            print self.devices
            self.configProgress.show()            
            self.configProgress.setEnabled(True)
            self.configProgress.setMaximum(len(self.devices))
            self.configProgress.setValue(0)           

            self.run_thread = kitsunetutils.run_configs_thread(self.devices)
            self.connect(self.run_thread, SIGNAL("device_finished"), self.device_finished)
            self.connect(self.run_thread, SIGNAL("finished()"), self.run_configs_done)
            self.run_thread.start()
            self.btnAddDevice.setEnabled(False)
            self.btnRunConfigs.setEnabled(False)
            self.tableTargets.setEnabled(False)

    def device_finished(self, device_result):
        print device_result
        self.configProgress.setValue(self.configProgress.value()+1)

    def run_configs_done(self):
        self.devices = []
        self.tableTargets.setRowCount(0)
        self.btnAddDevice.setEnabled(True)
        self.btnRunConfigs.setEnabled(True)
        self.configProgress.setEnabled(False)
        self.tableTargets.setEnabled(True)
        QtGui.QMessageBox.information(self, "Done!", "Device configuration complete!")


def main():
    app = QtGui.QApplication(sys.argv)
    form = KitsuNetApp()               
    form.show()                       
    app.exec_()                       


if __name__ == '__main__':            
    main()                            