
import cv2
# Load the image
img1 = cv2.imread('hw4_radiograph_1.jpg',0)
img2 = cv2.imread('hw4_radiograph_2.jpg',0)
# Apply Otsu method
ret, thres = cv2.threshold(img1,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, thres1 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Apply adaptive threshold
th3 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2)
th4 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2)
# Display the result
img1 = cv2.resize(img1, (300, 200))
img2 = cv2.resize(img2, (300, 500))
thres = cv2.resize(thres, (300, 200))
thres1 = cv2.resize(thres1, (300, 500))
th3 = cv2.resize(th3, (300, 200))
th4 = cv2.resize(th4, (300, 500))

#
cv2.imshow('original image 1',img1)
cv2.imshow('original image 2',img2)
cv2.imshow('otsu 1', thres)
cv2.imshow('adaptive 1', th3)
cv2.imshow('otsu 2', thres1)
cv2.imshow('adaptive 2', th4)
cv2.waitKey(0)
