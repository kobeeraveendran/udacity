import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def abs_sobel_thresh(image, orient = 'x', threshold_min = 0, threshold_max = 255):

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # apply sobel operator
    sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0) if orient == 'x' else cv2.Sobel(gray, cv2.CV_64F, 0, 1)

    # absolute value
    abs_sobel = np.absolute(sobel)

    # scale to 8-bit image
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    # create binary threshold to select pixels based on gradient strength
    sobel_binary = np.zeros_like(scaled_sobel)
    sobel_binary[(scaled_sobel >= threshold_min) & (scaled_sobel <= threshold_max)] = 1

    return sobel_binary

image = mpimg.imread("signs_vehicles_xygrad.png")
grad_binary = abs_sobel_thresh(image, orient = 'x', threshold_min = 20, threshold_max = 100)
f, (ax1, ax2) = plt.subplots(1, 2, figsize = (24, 9))
f.tight_layout()

ax1.imshow(image)
ax1.set_title("Original image")

ax2.imshow(grad_binary)
ax2.set_title("Thresholded gradient")


plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)
plt.show()