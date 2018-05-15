import sys
from cx_Freeze import setup, Executable
includes = ["sip","re","atexit","PyQt4.QtCore","PyQt4.QtGui","openpyxl","openpyxl.workbook","os", "sys","subprocess","platform","time","json"] 
exe = Executable(
	script = "Prinv_v01.py",
	base = "Win32GUI"
	)
 
setup(
	name = 'Process Inventory',
    version = '0.1',
    description = 'Process inventory data',
	options = {"build_exe": {"includes": includes}},
	executables = [exe]
	)
