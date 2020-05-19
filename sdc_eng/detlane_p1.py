import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

import os

base_dir = "CarND-LaneLines-P1/"

image_dir = base_dir + "test_images/"
vid_dir = base_dir + "test_videos/"

# helper functions

def grayscale(image):

    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def canny(image, low_threshold, high_threshold):

    return cv2.Canny(image, low_threshold, high_threshold)

def gaussian_blur(image, kernel_size):

    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def region_of_interest(image, vertices):

    mask = np.zeros_like(image)

    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255, ) * channel_count

    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def point_of_intersection(line1, line2):

    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1

    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3

    det = a1 * b2 - a2 * b1

    if det != 0:
        x = (b2 * c1 - b1 * c2) / det
        y = (a1 * c2 - a2 * c1) / det

        return (x, y)

    else:
        # lines are parallel
        return (np.inf, np.inf)

def draw_lines(image, lines, color = [255, 0, 0], thickness = 2):

    for line in lines:
        
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else np.inf

            # only include lines that have slopes characteristic of typical lane lines
            if (slope < 5 and slope > 0.5) or (slope > -5 and slope < -0.5):

                # identify left and right lane lines
                # point order seems to be consistently left-to-right
                # so, positive slope = left lane line, negative slope = right lane line

                # find intersections with the "top" and "bottom" of the lane to extend the line


                
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)

def hough_transform(image, rho, theta, threshold, min_line_len, max_line_gap):

    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]), minLineLength = min_line_len, maxLineGap = max_line_gap)

    print(lines)
    print('\n\n\n')
    line_image = np.zeros((image.shape[0], image.shape[1], 3), dtype = np.uint8)
    draw_lines(line_image, lines)

    return line_image, lines

def weighted_image(image, initial_image, alpha = 0.8, beta = 1., gamma = 0.0):

    return cv2.addWeighted(initial_image, alpha, image, beta, gamma)



# lane detection pipeline
def detect_lane_lines(input_image):

    image = mpimg.imread(input_image)
    img_dims = image.shape

    print("Image dims: ", img_dims)

    gray = grayscale(image)
    gray_blur = gaussian_blur(image, kernel_size = 5)

    edges = canny(image, low_threshold = 50, high_threshold = 150)

    mask_vertices = np.array([[(0, img_dims[0]), (450, 330), (490, 330), (img_dims[1], img_dims[0])]], dtype = np.int32)

    masked_edges = region_of_interest(edges, mask_vertices)

    line_image, lines = hough_transform(masked_edges, rho = 1, theta = np.pi / 180, threshold = 15, min_line_len = 40, max_line_gap = 20)

    color_image_with_lines = weighted_image(line_image, image)

    #print("Original image: ")
    #plt.imshow(image)
    #plt.show()

    print("Detected lines: ")
    plt.imshow(color_image_with_lines)
    plt.show()

    return color_image_with_lines


if __name__ == "__main__":

    # run basic lane detection on images
    for image in os.listdir(image_dir):
        detect_lane_lines(image_dir + image)

    #detect_lane_lines(image_dir + "solidWhiteCurve.jpg")