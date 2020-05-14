import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import numpy as np 

image = mpimg.imread("test.jpg")
print("This image is: {} with dimensions {}".format(type(image), image.shape))

y = image.shape[0]
x = image.shape[1]

color_select = np.copy(image)

rgb_threshold = [230, 230, 230]

thresholds = (image[:, :, 0] < rgb_threshold[0]) | (image[:, :, 1] < rgb_threshold[1]) | (image[:, :, 2] < rgb_threshold[2])

color_select[thresholds] = [0, 0, 0]

plt.imshow(color_select)
plt.show()