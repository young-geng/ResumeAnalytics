from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def pdf_to_text(s):
	infile = StringIO(s)
	output = StringIO()
	manager = PDFResourceManager()
	converter = TextConverter(manager, output, laparams=LAParams())
	interpreter = PDFPageInterpreter(manager, converter)
	pagenums = set()

	for page in PDFPage.get_pages(infile, pagenums):
		interpreter.process_page(page)

	infile.close()
	converter.close()
	text = output.getvalue()
	output.close()

	return text

if __name__ == '__main__':
	pdf = open('test.pdf').read()
	print pdf_to_text(pdf)


