import PyPDF2

pdfFileObj = open('C:\Users\enunez2\Documents\scripts\pyprojects\SHI Performance\S46871555-Sterling Construction.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pdfwriter = PyPDF2.PdfFileWriter()

print pdfReader.getNumPages()

pdfwriter.addBlankPagepdfReader()

print pdfReader.getNumPages()

# pageObj = pdfReader.getPage(0)

# dict = pdfReader.getFormTextFields()

# print dict['bios_change']


