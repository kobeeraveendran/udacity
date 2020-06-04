import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

from histogram_peaks import hist

image = mpimg.imread("warped-example.jpg")


def find_lane_pixels(image):
    histogram = hist(image)

    out_image = np.dstack((image, image, image)) * 255

    print("Histogram shape: ", histogram.shape)
    midpoint = np.int(histogram.shape[0] // 2)

    # find peaks in histogram on left and right sides
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # hyperparameters

    num_windows = 9
    margin = 100
    min_pixels = 50

    window_height = np.int(image.shape[0] // num_windows)

    nonzero = image.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    #print("nonzero x: \n", nonzerox)
    #print("nonzero y: \n", nonzeroy)

    # print("nonzero: \n", nonzero)
    # print("nonzero shape: ", len(nonzero))
    # print("\nNonzero x: \n", nonzerox[:5])
    # print("\nNonzero y: \n", nonzeroy[:5])

    #print("nonzero x shape: ", nonzerox.shape)
    #print("nonzero y shape: ", nonzeroy.shape)

    leftx_current = leftx_base
    rightx_current = rightx_base

    left_lane_indices = []
    right_lane_indices = []

    for window in range(num_windows):
        y_coord_low = image.shape[0] - (window + 1) * window_height
        y_coord_high = image.shape[0] - window * window_height

        xleft_low = leftx_current - margin
        xleft_high = leftx_current + margin
        xright_low = rightx_current - margin
        xright_high = rightx_current + margin
        #left_start = (leftx_current - margin, y_coord)
        #right_start = (rightx_current - margin, y_coord)

        #left_end = (leftx_current + margin, y_coord + window_height)
        #right_end = (rightx_current + margin, y_coord + window_height)

        cv2.rectangle(out_image, (xleft_low, y_coord_low), (xleft_high, y_coord_high), color = (255, 0, 0), thickness = 2)
        cv2.rectangle(out_image, (xright_low, y_coord_low), (xright_high, y_coord_high), color = (255, 0, 0), thickness = 2)

        #plt.imshow(out_image)

        curr_window = ((xleft_low, y_coord_low), (xleft_high, y_coord_high))

        #good_left_inds = nonzerox[(nonzerox >= xleft_low) & (nonzerox <= xleft_high)]

        good_left_inds = ((nonzerox >= xleft_low) & (nonzerox <= xleft_high) & (nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high)).nonzero()[0]
        good_right_inds = ((nonzerox >= xright_low) & (nonzerox <= xright_high) & (nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high)).nonzero()[0]

        #print("good left indices: ", good_left_inds)
        #print("good left indices shape: ", good_left_inds.shape)

        # good_left_inds = nonzero[((nonzerox >= xleft_low) & (nonzerox <= xleft_high)) & ((nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high))]
        # good_right_inds = nonzero[((nonzerox >= xright_low) & (nonzerox <= xright_high)) & ((nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high))]

        left_lane_indices.append(good_left_inds)
        right_lane_indices.append(good_right_inds)

    leftx = nonzerox[left_lane_indices]
    lefty = nonzeroy[left_lane_indices]
    rightx = nonzerox[right_lane_indices]
    righty = nonzeroy[right_lane_indices]

    return leftx, lefty, rightx, righty, out_image

def fit_polynomial(binary_warped):

    