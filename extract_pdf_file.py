
import PyPDF2
from PyPDF2 import PdfFileReader,PdfFileWriter
import datetime


def print_time():
    parser = datetime.datetime.now()
    return  str(parser.strftime("%H:%M:%S"))

def print_date():
    parser = datetime.datetime.now()
    return str(parser.strftime("%d-%m-%Y"))

pdf_document = "Bilans_sanguins.pdf"

pdf = PdfFileReader(pdf_document)

for page in range(pdf.getNumPages()):
    pdf_writer = PyPDF2.PdfFileWriter()
    current_page = pdf.getPage(page)
    pdf_writer.addPage(current_page)

    outputFinalName  = "example-page-{}.pdf".format(page + 1)

    with open(outputFinalName,"wb") as out:
        pdf_writer.write(out)

        print(outputFinalName,"Créé le  ",print_date(),"à : ",print_time())
