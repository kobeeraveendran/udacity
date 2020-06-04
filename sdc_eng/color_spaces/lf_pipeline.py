import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

image = mpimg.imread("bridge_shadow.jpg")

def pipeline(image, s_thresh = (170, 255), sx_thresh = (20, 100)):

    img = np.copy(image)

    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    l_channel = hls[:, :, 1]
    s_channel = hls[:, :, 2]

    sobel_x = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0)
    abs_sobel = np.absolute(sobel_x)
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    sobel_binary = np.zeros_like(scaled_sobel)
    sobel_binary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1

    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1

    color_binary = np.dstack((np.zeros_like(sobel_binary), sobel_binary, s_binary))

    return color_binary

result = pipeline(image)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 9))
fig.tight_layout()

ax1.imshow(image)
ax1.set_title("Original image")

ax2.imshow(result)
ax2.set_title("Pipeline output")

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)
plt.show()