import cv2
import numpy as np

# Load original image
originalImage = cv2.imread('cat.jpg')
originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
reshapedImage = np.float32(originalImage.reshape(-1, 3))
numberOfClusters = 2

stopCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)
ret, labels, clusters = cv2.kmeans(reshapedImage, numberOfClusters, None, stopCriteria, 10, cv2.KMEANS_RANDOM_CENTERS)

clusters = np.uint8(clusters)

intermediateImage = clusters[labels.flatten()]
clusteredImage = intermediateImage.reshape((originalImage.shape))



cv2.imshow('Original Image',originalImage)
cv2.imshow('Image 1',clusteredImage)
if cv2.waitKey(0) & 0xFF == 27:
    cv2.destroyAllWindows()
