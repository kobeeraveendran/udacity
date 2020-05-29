import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


image = mpimg.imread("signs_vehicles_xygrad.png")


# helper functions
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def do_sobel(image, orient = 'x', sobel_kernel = 3):

    return np.absolute(cv2.Sobel(image, cv2.CV_64F, 1, 0, sobel_kernel)) if orient == 'x' else np.absolute(cv2.Sobel(image, cv2.CV_64F, 0, 1, sobel_kernel))


def create_binary_image(image, threshold = (0, 255)):

    binary_output = np.zeros_like(image)
    binary_output[(image >= threshold[0]) & (image <= threshold[1])] = 1

    return binary_output

# end helper functions


def abs_sobel_thresh(image, orient = 'x', sobel_kernel = 3, thresh = (0, 255)):

    sobel = do_sobel(grayscale(image), orient, sobel_kernel)

    abs_sobel = np.absolute(sobel)

    scaled_sobel = (255 * abs_sobel / np.max(abs_sobel))

    binary_sobel = np.zeros_like(scaled_sobel)
    binary_sobel[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1

    return binary_sobel



def mag_thresh(image, sobel_kernel = 3, mag_thresh = (0, 255)):

    gray = grayscale(image)

    abs_sobel_x = do_sobel(gray, orient = 'x', sobel_kernel = sobel_kernel)
    abs_sobel_y = do_sobel(gray, orient = 'y', sobel_kernel = sobel_kernel)

    magnitude = np.sqrt(abs_sobel_x ** 2 + abs_sobel_y ** 2)

    scaled_mag = np.uint8(255 * magnitude / np.max(magnitude))

    mag_binary = create_binary_image(scaled_mag, mag_thresh)

    return mag_binary

def dir_threshold(image, sobel_kernel = 3, thresh = (0, np.pi / 2)):

    gray = grayscale(image)

    abs_sobel_x = do_sobel(gray, 'x', sobel_kernel)
    abs_sobel_y = do_sobel(gray, 'y', sobel_kernel)

    grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)

    binary_grad = create_binary_image(grad_dir, thresh)

    return binary_grad


# test
if __name__ == "__main__":
    ksize = 3
    gradx = abs_sobel_thresh(image, orient = 'x', sobel_kernel = ksize, thresh = (20, 100))
    grady = abs_sobel_thresh(image, orient = 'y', sobel_kernel = ksize, thresh = (20, 100))

    mag_binary = mag_thresh(image, sobel_kernel = ksize, mag_thresh = (30, 100))

    dir_binary = dir_threshold(image, sobel_kernel = 15, thresh = (0.7, 1.3))

    # print("Sobel X")
    # plt.imshow(gradx, cmap = "gray")
    # plt.show()

    # print("Sobel Y")
    # plt.imshow(grady, cmap = "gray")
    # plt.show()

    # print("Binary magnitude")
    # plt.imshow(mag_binary, cmap = "gray")
    # plt.show()

    # print("Binary direction")
    # plt.imshow(dir_binary, cmap = "gray")
    # plt.show()

    combined = np.zeros_like(dir_binary)
    combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1

    plt.imshow(combined, cmap = "gray")
    plt.show()