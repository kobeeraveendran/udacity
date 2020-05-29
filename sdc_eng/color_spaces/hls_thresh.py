import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image = mpimg.imread("test6.jpg")

thresh = (180, 255)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#binary = np.zeros_like(gray)
#binary[(gray >= thresh[0]) & (gray <= thresh[1])] = 1

# R = image[:, :, 0]
# binary = np.zeros_like(R)
# binary[(R >= thresh[0]) & (R <= thresh[1])] = 1

hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
S = hls[:, :, 2]

thresh_s = (90, 150)

binary = np.zeros_like(S)
binary[(S > thresh[0]) & (S <= thresh[1])] = 1


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))

ax1.imshow(image)
ax1.set_title("Original image")

ax2.imshow(binary, cmap = "gray")
ax2.set_title("HLS thresholded")

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.1)

plt.show()