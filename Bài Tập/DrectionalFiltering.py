import cv2
import numpy as np
import matplotlib.pyplot as plt

def __main__():
    img = cv2.imread("input1.jpg")
    img = cv2.resize(img, (200, 200))
    a = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])/3


    dst = np.empty_like(img)
    noise = cv2.randn(dst, (0, 0, 0), (30, 30, 30))
    noise_image = cv2.addWeighted(img, 0.5, noise, 0.5, 30)

    img1 = cv2.filter2D(noise_image, -1, a)

    plt.figure(figsize=(5, 11))
    plt.subplot(3, 2, 1), plt.imshow(img), plt.title('Original Image')
    plt.subplot(3, 2, 2), plt.imshow(noise_image), plt.title('Noise Image')
    plt.subplot(3, 2, 3), plt.imshow(img1), plt.title('Image with Filter 1')

    plt.show()

if __name__ == "__main__":
    __main__()
