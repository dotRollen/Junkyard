import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

filename = sys.argv[1]
fp = open(filename, 'rb')

parser = PDFParser(fp)
doc = PDFDocument(parser)
fields = resolve1(doc.catalog['AcroForm'])['Fields']
for i in fields:
    field = resolve1(i)
    names, values = field.get('T'), field.get('V')
    dict_fields = {}

