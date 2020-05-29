import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

image = mpimg.imread("signs_vehicles_xygrad.png")

def mag_thresh(image, sobel_kernel = 3, mag_thresh = (0, 255)):

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # calculate gradients in x and y directions
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize = sobel_kernel)

    # calculate magnitude
    magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    scaled_mag = np.uint8(255 * magnitude / np.max(magnitude))

    mag_binary = np.zeros_like(scaled_mag)
    mag_binary[(scaled_mag >= mag_thresh[0]) & (scaled_mag <= mag_thresh[1])] = 1

    return mag_binary

mag_binary = mag_thresh(image, sobel_kernel = 3, mag_thresh = (30, 100))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (24, 9))
fig.tight_layout()

ax1.imshow(image)
ax1.set_title("Original")

ax2.imshow(mag_binary, cmap = "gray")
ax2.set_title("Magnitude thresholded version")

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)

plt.show()