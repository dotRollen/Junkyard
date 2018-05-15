import sys
from cx_Freeze import setup, Executable
includes = ["sip","re","atexit","PyQt4.QtCore","PyQt4.QtGui","openpyxl","openpyxl.workbook","os", "sys","subprocess","platform","time","json"]
includefiles = ['shilogo.jpg', 'Security.png']
exe = Executable(
	script = "Checkin_v072.py",
	base = "Win32GUI"
	)
 
setup(
	name = 'Checkin/Checkout',
    version = '0.72',
    description = 'SHI Security check in and out of visitor and employee devices.',
	options = {"build_exe": {"includes": includes,'include_files':includefiles}},
	executables = [exe]
	)
