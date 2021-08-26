#!/usr/bin/python3

import pandas as pd
import numpy as np
import cv2
import pytesseract
import pyocr
import pyocr.builders
import os
from PIL import Image
from pdf2image import convert_from_bytes
import layoutparser as lp

custom_config = r'--oem 3 --psm 6'

from matplotlib import pyplot as plt

# load raw image
img = cv2.imread("/Users/morellatel/IdeaProjects/flask-test/static/images/Bilans_sanguins-page0.jpg",0)

# Display raw image
plt.imshow(img)
plt.show()

############ SHARPEN IMAGE ##############################################
def sharpen_image(im):
    kernel = np.ones((3,3),np.float32)/90
    im = cv2.filter2D(im,-1,kernel)

    return im

# call SHARPEN FUNCTION
img_sharpen = sharpen_image(img)

# DISPLAY SHARPENED IMAGE
plt.imshow(img_sharpen)
plt.show()


# IMAGE THRESHOLDING ##################
# Apply Image Thresholding
img_thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

# INVERT THE IMAGE , 255 is the maximum value
img_thresh = 255-img_thresh

# Display image
plt.imshow(img_thresh)
plt.show()


######### TEXT ALIGNMENT IN THE IMAGE ########################################
def align_text(im):
    coords = np.column_stack(np.where(img_thresh > 0))

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    h,w = im.shape

    center = (w //2 , h//2)
    M = cv2.getRotationMatrix2D(center,angle,1.0)
    rotated = cv2.warpAffine(img_thresh,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)

    return rotated

# align image text
img = align_text(img)

# Display rotated and aligned image
plt.imshow(img)
plt.show()

# SPLIT IMAGE INTO ROWS
########## Split text into rows #############################

# Find sum of column values , row-wise
a = np.sum(img==255,axis=1)

rows = []
seg = []

for i in range(len(a)):
    if a[i] > 0:
        seg.append(i)

    if (a[i] == 0) & (len(seg) >=5):
        rows.append(seg)
        seg = []
    if len(seg) > 0:
        rows.append(seg)
# Number of row segments
len(rows)

# PRINT FEW OF THEM
plt.imshow(img[rows[0][0]:rows[0][-1],:])
plt.show()

# CONVERTING IMAGE TO TEXT
#for i in range(len(rows)):
#    print(pytesseract.image_to_string(img[rows[i][0]:rows[i][-1],:],config=custom_config,lang='fra'))


path_image='/Users/morellatel/IdeaProjects/flask-test/static/images/'
chemin_image='/Users/morellatel/IdeaProjects/flask-test/static/images'
files_in_dir = os.listdir(path_image)
print(files_in_dir)
# Extract texte  from image using PyOCR
image_txt = []
tools = pyocr.get_available_tools()[0]
lang=tools.get_available_languages()[0]
for name in files_in_dir:
    nom_sortie = path_image+"/"+name
    txt=tools.image_to_string(Image.open(nom_sortie),
                              lang=lang,builder=pyocr.builders.TextBuilder())
    #txt=' '.join(txt.replace('-\n','').replace('\n','\n').split())
    print(txt)

    output_dir = '/Users/morellatel/IdeaProjects/flask-test/output'
    filename=name[:-4]
    nom_fichier=output_dir+'/'+filename+'.txt'
    fichier = open(nom_fichier,"w")
    fichier.write(txt)
    fichier.close()

    image_txt.append(txt)

print(image_txt)

print("\n\n\n")
images = convert_from_bytes(open('Bilans_sanguins.pdf', 'rb').read())

print(images)
print("\n\n\n")

model = lp.Detectron2LayoutModel(
    config_path ='lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config', # In model catalog
    label_map   = {0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}, # In model`label_map`
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8] # Optional
)
#loop through each page
for image in images:
    ocr_agent = lp.ocr.TesseractAgent()

    image = np.array(image)

    layout = model.detect(image)
text_blocks = lp.Layout([b for b in layout if b.type == 'Text']) #loop through each text box on page.

for block in text_blocks:
    segment_image = (block
                     .pad(left=5, right=5, top=5, bottom=5)
                     .crop_image(image))
    text = ocr_agent.detect(segment_image)
    block.set(text=text, inplace=True)


for i, txt in enumerate(text_blocks.get_texts()):
    my_file = open(output_dir+'/'+i+'.txt',"a+")
    my_file.write(txt)