from pytesseract import Output
import pytesseract
import cv2
from PIL import Image
import numpy as np


filename = 'example-page-1.tif'

#################################################################################################################

img1 = np.array(Image.open(filename))
img1 = cv2.imread(filename)

# some preprocessing steps
# Use of OpenCV Library
# Using Normalization , thresholding and image blur

norm_img = np.zeros((img1.shape[0],img1.shape[1]))

img1 = cv2.normalize(img1,norm_img,0,255,cv2.NORM_MINMAX)
img1 = cv2.threshold(img1,100,255,cv2.THRESH_BINARY)[1]
img1 = cv2.GaussianBlur(img1,(1,1),0)


texte = pytesseract.image_to_string(img1,config='--oem 3 --psm 6')
print("Texte extrait : ",texte)

####################################################################################################################
image = cv2.imread(filename)

rgb = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


#results = pytesseract.image_to_data(image)

results = pytesseract.image_to_data(rgb , output_type=Output.DICT)


print(results)

print("\n\n\n")

print(results["text"])

for i in range(0,len(results["text"])):
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]

    text = results["text"][i]

    conf = int(results["conf"][i])

    # we specify the confidence value to 70
    if conf > 70:

        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV , then draw a bounding box around the text along with the text itsef
        text = " ".join([c if ord(c) < 128 else "" for c in text]).strip()
        cv2.rectangle(image,(x,y),(x + w , y+h),(0,255,0),2)
        #cv2.putText(image,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,200),2)

        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow("Image ",image)

        #cv2.waitKey(0)




