import cv2
import pytesseract

try:
    from PIL import Image
except ImportError:
    import Image

pytesseract.pytesseract.tesseract_cmd=r'/usr/local/bin/tesseract'


def ocr_core(img):
    text = pytesseract.image_to_string(img,lang='eng')
    return  text

img = cv2.imread("invoice-image.jpeg")

# get grayscale image
def get_grayscale(image):
    return  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


# Noise removal
def remove_noise(image):
    return  cv2.medianBlur(image,5)

# thresholding

def threshold(image):
    return cv2.threshold(image,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

img  = get_grayscale(img)
img = threshold(img)
img = remove_noise(img)

print(ocr_core(img))

mon_texte_extrait = pytesseract.image_to_string(Image.open("invoice-image.jpeg"),lang='eng',config="--oem 3 --psm 6")
print("#"*10+" RÉSULTAT EXTRACTION "+"#"*10)
print(mon_texte_extrait)
print("#"*40)
print("\n\n\n")
print("#"*15+" FOR ORIENTATION AND SCRIPT DETECTION "+"#"*15)

print(pytesseract.image_to_osd(Image.open("invoice-image.jpeg")))
print("#"*50)
print("\n\n\n")

print("#"*15+" BOX BOUNDARIES AROUND ELEMENT "+"#"*15)
print(pytesseract.image_to_boxes(Image.open("invoice-image.jpeg")))
print("#"*50)