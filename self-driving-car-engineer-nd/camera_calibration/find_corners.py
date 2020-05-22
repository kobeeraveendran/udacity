import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

nx = 8
ny = 6

image = cv2.imread("calibration_test.png")

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

ret, corners = cv2.findChessboardCorners(gray, patternSize = (nx, ny), corners = None)

# if found...
if ret:

    # draw the corners
    cv2.drawChessboardCorners(image, (nx, ny), corners, ret)
    plt.imshow(image)
    plt.show()