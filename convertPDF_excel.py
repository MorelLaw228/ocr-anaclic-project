#!/usr/bin/python3

import os
import ocrmypdf
import requests
import pdfplumber

# Fonction pour télécharger un fichier à partir d'un URL
def download_file(url):
    local_filename = url.split('/')[-1]

    with requests.get(url) as r:
        assert r.status_code == 200 , f'error , status code is : {r.status_code}'
        with open(local_filename,'wb') as f:
            f.write(r.content)


    return local_filename


# application
invoice = "https://bit.ly/2UJgUpO"
invoice_pdf = download_file(invoice)

analyse_pdf = 'example-page-1.pdf'
with pdfplumber.open('example-page-1.pdf') as pdf:
    page  = pdf.pages[0]

    texte = page.extract_text()
    print(texte)


os.system(f'ocrmypdf  {analyse_pdf}  output.pdf')

with pdfplumber.open('output.pdf') as pdf:
    page  = pdf.pages[0]

    texte = page.extract_text()
    print(texte)

lines =texte.split('\n')
print(lines)