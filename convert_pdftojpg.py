#!/usr/bin/python3

import os
from pdf2image import convert_from_path
import pytesseract
import time
import utils


chemin = os.getcwd()

def pdftotext(pdf_path,num_pages=18):
    # use pdf2image to keep the pages in memory
    pages = convert_from_path(pdf_path,500,first_page=0,last_page=num_pages)
    docs=[]
    ## Iterate through each page saving the text and page number
    for i,page in enumerate(pages):
        d = {}
        text = pytesseract.image_to_string(page,config='--oem 3  --psm 6',lang='fra')
        d['page'] = i+1 ## index from 0
        d['text'] = text
        ## cerate list of dictionaries

        pdf_file = pdf_path[:-4]



        docs.append(d)

        print("\n\n\n")
        print("###############################################")
        print("########### IMAGE_TO_BOXES  ####################")
        print("###############################################")
        print("\n\n\n")
        start_time=time.time()
        pytess_result = pytesseract.image_to_boxes(page,lang='fra',config=" --oem 3 --psm 6",output_type=pytesseract.Output.DICT)
        print(pytess_result)
        utils.display_total_time(start_time)
        print("###############################################")
        print("\n\n\n")
        print("\n\n\n")
        print("###############################################")
        print("########### IMAGE_TO_DATA  ####################")
        print("###############################################")
        start_time=time.time()
        pytess_data = pytesseract.image_to_data(page,lang='fra',config='--oem 3 --psm 6',output_type=pytesseract.Output.DICT)
        print(pytess_data)
        utils.display_total_time(start_time)


    print("Done")

    return docs

image_path = "/Users/morellatel/IdeaProjects/flask-test/static/images"

for pdf_file in os.listdir(chemin):
    if pdf_file.endswith(".pdf"):

        pages = convert_from_path(pdf_file,300)
        pdf_file = pdf_file[:-4]
        path_save = image_path+"/"+pdf_file

        for page in pages:
            page.save("%s-page%d.jpg"%(path_save,pages.index(page)),"JPEG")


docs=pdftotext("Bilans_sanguins.pdf",18)
print(docs)







