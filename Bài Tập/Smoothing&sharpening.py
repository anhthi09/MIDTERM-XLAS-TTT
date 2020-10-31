# Necessary imports
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
# Loading the image
# Integer 0 indicates that we want to load a grayscale image
img1 = cv2.imread('Cybertruck.jpg',0)
img2 = cv2.imread('logo.png',0)
cv2_imshow(img1)
cv2_imshow(img2)

# Performing averaging blurring on our Cybertruck image
# Filters - left (3,3), middle(5,5), right(9,9)

blurred_1 = np.hstack([
  cv2.blur(img1,(3,3)),
  cv2.blur(img1,(5,5)),
  cv2.blur(img1,(9,9)) ])
cv2_imshow(blurred_1)

# Performing averaging blurring on our Logo image
# Filters - left (3,3), middle(5,5), right(9,9)

blurred_2 = np.hstack([
  cv2.blur(img2,(3,3)),
  cv2.blur(img2,(5,5)),
  cv2.blur(img2,(9,9))])
cv2_imshow(blurred_2)

