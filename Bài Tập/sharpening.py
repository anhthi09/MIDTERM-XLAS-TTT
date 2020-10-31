import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('chess.png')

filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpen_img=cv2.filter2D(img,-1,filter)

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(sharpen_img),plt.title('Sharpen')
plt.xticks([]), plt.yticks([])
plt.show()




