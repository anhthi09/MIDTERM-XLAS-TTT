import cv2
import numpy as np
image1 = cv2.imread('input1.jpg')

gamma=2
image2 = np.power(image1,gamma)

gamma=3
image3 = np.power(image1,gamma)

gamma=4
image4 = np.power(image1,gamma)


cv2.imshow('nhomTTT',image1)
cv2.imshow('gamma2',image2)
cv2.imshow('gamma3',image3)
cv2.imshow('gamma4',image4)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
