import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image = mpimg.imread("signs_vehicles_xygrad.png")

def dir_threshold(image, sobel_kernel = 3, thresh = (0, np.pi / 2)):

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # calculate gradient in x and y directions
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize = sobel_kernel)

    abs_sobel_x = np.absolute(sobel_x)
    abs_sobel_y = np.absolute(sobel_y)

    grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)

    grad_binary = np.zeros_like(grad_dir)
    grad_binary[(grad_dir >= thresh[0]) & (grad_dir <= thresh[1])] = 1

    return grad_binary

dir_binary = dir_threshold(image, sobel_kernel = 15, thresh = (0.7, 1.3))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (24, 9))
fig.tight_layout()

ax1.imshow(image)
ax1.set_title("Original image")

ax2.imshow(dir_binary, cmap = "gray")
ax2.set_title("Binary image w/ Dir threshold")

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)

plt.show()