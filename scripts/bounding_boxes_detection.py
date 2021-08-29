import pytesseract
import cv2

image = cv2.imread("invoice-image.jpeg")
base_image = image.copy()

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imwrite("invoice_image_gray.png",gray)

blur = cv2.GaussianBlur(gray,(7,7),0)
cv2.imwrite("invoice_image_blur.png",blur)


thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("invoice_image_thresh.png",thresh)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,13))
cv2.imwrite("invoice_image_kernel.png",kernel)

dilate = cv2.dilate(thresh,kernel,iterations=1)
cv2.imwrite("invoice_image_dilate.png",dilate)

# Get contours
cnts = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# organize contours from LEFT to RIGHT
cnts = sorted(cnts,key=lambda x:cv2.boundingRect(x)[0])
for c in cnts:
    x ,y ,w,h = cv2.boundingRect(c)
    # Pour ne garder que les contours de grande hauteur et pas les petites
    #if h >200 and w > 20 :
       # roi = image[y:y+h,x:x+h]
        #cv2.imwrite("invoice_image_roi.png",roi)
        # Draw rectangles around image
        #cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),2)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
cv2.imwrite("invoice_image_bblox.png",image)
