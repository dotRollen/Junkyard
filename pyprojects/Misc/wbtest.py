from openpyxl import load_workbook

wb = load_workbook('SHI_Device_Log_09-26-16.xlsx')

print wb.get_sheet_names()
