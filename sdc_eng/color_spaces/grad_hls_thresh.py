import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2


def hls_with_grad_threshold(image, hls_threshold = (170, 255), grad_threshold = (20, 100)):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    S = hls[:, :, 2]

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    abs_sobel = np.absolute(sobel_x)
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    sobel_x_binary = np.zeros_like(scaled_sobel)
    sobel_x_binary[(scaled_sobel >= grad_threshold[0]) & (scaled_sobel <= grad_threshold[1])] = 1
    
    hls_binary = np.zeros_like(S)
    hls_binary[(S >= hls_threshold[0]) & (S <= hls_threshold[1])] = 1

    color_binary = np.dstack((np.zeros_like(sobel_x_binary), sobel_x_binary, hls_binary)) * 255

    combined_binary = np.zeros_like(sobel_x_binary)
    combined_binary[(hls_binary == 1) | (sobel_x_binary == 1)] = 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))
    ax1.set_title("Stacked thresholds")
    ax1.imshow(color_binary)

    ax2.set_title("Combined S channel and gradient thresholds")
    ax2.imshow(combined_binary, cmap = "gray")

    plt.show()

    return combined_binary

if __name__ == "__main__":
    image = mpimg.imread("test6.jpg")

    combined_binary = hls_with_grad_threshold(image)