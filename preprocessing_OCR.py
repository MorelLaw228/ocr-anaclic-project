import cv2
from matplotlib import pyplot as plt
import numpy as np

# THIS SCRIPT IS INSPIRED FROM THE FOLLOWING YOUTUBE VIDEO : https://www.youtube.com/watch?v=ADV-AjAXHdc&t=494s


# PREPROCESSING IMAGES FOR OCR TO GET BETTER RESULT
# We will use OPENCV

# 1.Inverted Images
# 2.Rescaling
# 3.Binarization + Conversion of an image to black and white
# 4.Noise removal => Removing noise in poor image
# 5.Dilation and Erosion
# 6.Rotation/Deskewing => which can be result for bad scans
# 7. Removing borders
# 8. Missing borders => How to add borders to get better result
# 9. Transparency / Alpha Channel

# Opening Image
print("#"*15 + ' OPENING IMAGE '+"#"*15)
image_file = "images/example-image.jpg"
img = cv2.imread(image_file)
# For IMAGE SHOW
cv2.imshow("Original image",img)
cv2.waitKey(0)


# Function to display an image
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()


# 1.INVERTED IMAGE
print("#"*15 + ' INVERTED IMAGE '+"#"*15)
# Work better for OpenCV VERSION 4
inverted_image = cv2.bitwise(img)
inverted_image_path = "temp/inverted.jpg"
cv2.imwrite(inverted_image_path,inverted_image)

# 2. RESCALING IMAGE


# 3. BINARIZATION
def grayscale(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# call the grayscale function
gray_image = grayscale(img)
cv2.imwrite("temp/gray.jpg",gray_image)

# Show the grayscale image
display("temp/gray.jpg")
# To handle image threshold and it's black and white
# 127 and 255 are better values of parameters in cv2.threshold() function
thresh,im_bw = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
# bw for black and white image
cv2.imwrite("temp/bw_image.jpg",im_bw)
# Display bw image
display("temp/bw_image.jpg")


# 4. NOISE REMOVAL
# Noise is pixel that don't corresponding to text , ...etc...
def noise_removal(image):
    kernel = np.ones((1,1),np.uint8)
    image = cv2.dilate(image,kernel,iterations=1)
    kernel = np.ones((1,1),np.uint8)
    image = cv2.erode(image,kernel,iterations=1)
    image = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
    image = cv2.medianBlur(image,3)

    return (image)
# Call noise_removal  function
# We give as input of this function the black and white image we obtain previously
no_noise = noise_removal(im_bw)
cv2.imwrite("temp/no_noise.jpg",no_noise)

# To display no_noise image
display("temp/no_noise.jpg")

# DILATION AND EROSION
# We use it to adjust the font size
def thin_font(image):
    # Invert our image
    image = cv2.bitwise_not(image)
    # We can play with the parameters to have better result as (2,2) or number of iteratiosn
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image,kernel,iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


eroded_image = thin_font(no_noise)
cv2.imwrite("temp/eroded_image.jpg",eroded_image)
display("temp/eroded_image.jpg")

def thick_font(image):
    # Invert our image
    image = cv2.bitwise_not(image)
    # We can play with the parameters to have better result as (2,2) or number of iteratiosn
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

dilated_image = thick_font(no_noise)
cv2.imwrite("temp/dilated_image",dilated_image)
display("temp/dilated_image.jpg")

# ROTATION AND DESKEWING
# We use it when we have deskew image or rotated pdf or image
# We use for this a new image which is rotated
new = cv2.imread("images/rotated_image.jpg")
display("images/rotated_image.jpg")

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print(len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new)
cv2.imwrite("temp/rotated_fixed.jpg",fixed)
display("temp/rotated_fixed.jpg")


# REMOVING BORDERS
# We will use the no_noise image obtained previously
# We will display it first
display("temp/no_noise.jpg")

def remove_borders(image):
    _,contours,hierachy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours,key=lambda x:cv2.contourArea(x))
    cnt = cntSorted[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = image[y:y+h,x:x+w]
    return (crop)

no_borders = remove_borders(no_noise)
cv2.imwrite("temp/no_borders.jpg",no_borders)
display("temp/no_borders.jpg")

# MISSING BORDERS
# We will deal now with image which has missing borders
color = [255,255,255]
top,bottom,left,right = [150]*4
image_with_border = cv2.copyMakeBorder(no_borders,top,bottom,left,right,cv2.BORDER_CONSTANT,value=color)
cv2.imwrite("temp/image_with_borders.jpg",image_with_border)
display("temp/image_with_borders.jpg")









