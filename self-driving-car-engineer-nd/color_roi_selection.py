import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import numpy as np

image = mpimg.imread("test.jpg")

y = image.shape[0]
x = image.shape[1]

color_select = np.copy(image)
line_image = np.copy(image)

rgb_threshold = [200, 200, 200]

left_bottom = [0, 539]
right_bottom = [960, 540]
apex = [x // 2, 325]

color_thresholds = (image[:, :, 0] < rgb_threshold[0]) | (image[:, :, 1] < rgb_threshold[1]) | (image[:, :, 2] < rgb_threshold[2])

fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), deg = 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), deg = 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), deg = 1)

XX, YY = np.meshgrid(np.arange(0, x), np.arange(0, y))

region_thresholds = (YY > (XX * fit_left[0] + fit_left[1])) & (YY > (XX * fit_right[0] + fit_right[1])) & (YY < (XX * fit_bottom[0] + fit_bottom[1]))

color_select[color_thresholds] = [0, 0, 0]

line_image[~color_thresholds & region_thresholds] = [255, 0, 0]

plt.imshow(color_select)
plt.imshow(line_image)

plt.show()