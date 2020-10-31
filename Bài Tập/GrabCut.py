import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('bolt.jpg')              # img.shape : (413, 620, 3)
mask = np.zeros(img.shape[:2],np.uint8)   # img.shape[:2] = (413, 620)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (300,120,470,350)


cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)


mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

img_cut = img*mask2[:,:,np.newaxis]

plt.subplot(211),plt.imshow(img)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(212),plt.imshow(img_cut)
plt.title('Grab cut'), plt.xticks([]), plt.yticks([])
plt.show()
