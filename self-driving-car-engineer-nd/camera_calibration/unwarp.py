import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt

dist_pickle = pickle.load(open("wide_dist_pickle.p", "rb"))
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]

image = cv2.imread("test_image2.png")
nx = 8
ny = 6


def corners_unwarp(image, nx, ny, mtx, dist):

    undist = cv2.undistort(image, mtx, dist, None, mtx)

    gray = cv2.cvtColor(undist, cv2.COLOR_BGR2GRAY)

    retval, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    #print("Corners: \n", corners)

    if retval:
        cv2.drawChessboardCorners(undist, (nx, ny), corners, retval)
        #plt.imshow(gray, cmap = "gray")
        #plt.show()

        # choose 4 source points (chosen from corners)
        src = np.float32([
            corners[0], 
            corners[nx - 1], 
            corners[-1], 
            corners[-nx]
        ])

        print("Source: \n", src)

        plt.imshow(gray, cmap = "gray")

        for point in src:
            plt.plot(point[0][0], point[0][1], '.')
        plt.show()

        print("Source: \n", src)

        # choose 4 destination points
        # delta x ~= 700
        # delta y ~= 300
        image_size = (gray.shape[1], gray.shape[0])

        offset = 100
        dst = np.float32([
            [offset, offset], 
            [image_size[0] - offset, offset], 
            [image_size[0], image_size[1]], 
            [offset, image_size[1]]
        ])

        M = cv2.getPerspectiveTransform(src, dst)

        warped = cv2.warpPerspective(undist, M, image_size, flags = cv2.INTER_LINEAR)

        return warped, M

top_down, perspective_M = corners_unwarp(image, nx, ny, mtx, dist)

f, (ax1, ax2) = plt.subplots(1, 2, figsize = (24, 9))
f.tight_layout()

ax1.imshow(image)
ax1.set_title("Original image", fontsize = 25)

ax2.imshow(top_down)
ax2.set_title("Undistorted and Warped image", fontsize = 25)

plt.subplots_adjust(left = 0., right = 1, top = 0.9, bottom = 0.)
plt.show()