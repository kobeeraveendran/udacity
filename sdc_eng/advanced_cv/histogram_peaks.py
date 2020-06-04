import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image = mpimg.imread("warped-example.jpg") / 255

def hist(image):

    #print(image.shape)
    # plt.imshow(image, cmap = "gray")
    # plt.show()

    height = image.shape[0]
    width = image.shape[1]

    bottom_half = image[height // 2:,:]

    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))

    # ax1.set_title("full image")
    # ax1.imshow(image, cmap = "gray")

    # ax2.set_title("bottom half")
    # ax2.imshow(bottom_half, cmap = "gray")

    # plt.show()

    histogram = np.sum(bottom_half, axis = 0)

    return histogram


if __name__ == "__main__":
    histogram = hist(image)

    plt.plot(histogram)
    plt.xlabel("Pixel position")
    plt.ylabel("Counts")
    plt.show()