import cv2

img = cv2.imread("dog.jpg",0)
equ = cv2.equalizeHist(img)
cv2.imshow('nhomTTT',img)
cv2.imshow('equ',equ)
cv2.waitKey(0)
cv2.destroyAllWindows()