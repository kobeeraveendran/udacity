import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image = mpimg.imread("exit-ramp.jpg")

#plt.imshow(image)

import cv2
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
plt.imshow(gray, cmap = "gray")

kernel_size = 1
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 2)

low_threshold = 100
high_threshold = 255
edges = cv2.Canny(gray, low_threshold, high_threshold)
plt.imshow(edges, cmap = "Greys_r")
plt.show()