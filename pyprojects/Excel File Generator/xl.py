from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
import subprocess, os, platform, re, time

timestr = time.strftime("%Y%m%d-%H%M%S")
wb = Workbook()
ws1 = wb.active
ws1.title = "range names"




rows = [ ['Name', 'Device', 'Item Description', 'Item Serial #', 'IN', 'OUT', 'STAY IN']]

for row in rows:
	ws1.append
	
frozen_row = ws1['A2']
ws1.freeze_panes = frozen_row

wb.save(timestr + 'empty_book.xlsx')