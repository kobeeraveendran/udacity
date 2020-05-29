import matplotlib.image as mpimg
import numpy as np
import cv2
import matplotlib.pyplot as plt

image = mpimg.imread("test6.jpg")

def hls_select(image, thresh = (0, 255)):

    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

    S = hls[:, :, 2]

    binary = np.zeros_like(S)
    binary[(S > thresh[0]) & (S <= thresh[1])] = 1

    return binary

hls_binary = hls_select(image, thresh = (90, 255))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))
fig.tight_layout()

ax1.imshow(image)
ax1.set_title("Original Image")

ax2.imshow(hls_binary, cmap = "gray")
ax2.set_title("HLS thresholded image")

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)
plt.show()