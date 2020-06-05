import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

from histogram_peaks import hist

image = mpimg.imread("warped-example.jpg")


# def find_lane_pixels(image):
#     histogram = hist(image)

#     out_image = np.dstack((image, image, image)) * 255

#     print("Histogram shape: ", histogram.shape)
#     midpoint = np.int(histogram.shape[0] // 2)

#     # find peaks in histogram on left and right sides
#     leftx_base = np.argmax(histogram[:midpoint])
#     rightx_base = np.argmax(histogram[midpoint:]) + midpoint

#     # hyperparameters

#     num_windows = 9
#     margin = 100
#     min_pixels = 50

#     window_height = np.int(image.shape[0] // num_windows)

#     nonzero = image.nonzero()
#     nonzeroy = np.array(nonzero[0])
#     nonzerox = np.array(nonzero[1])

#     #print("nonzero x: \n", nonzerox)
#     #print("nonzero y: \n", nonzeroy)

#     # print("nonzero: \n", nonzero)
#     # print("nonzero shape: ", len(nonzero))
#     # print("\nNonzero x: \n", nonzerox[:5])
#     # print("\nNonzero y: \n", nonzeroy[:5])

#     #print("nonzero x shape: ", nonzerox.shape)
#     #print("nonzero y shape: ", nonzeroy.shape)

#     leftx_current = leftx_base
#     rightx_current = rightx_base

#     left_lane_indices = []
#     right_lane_indices = []

#     for window in range(num_windows):
#         y_coord_low = image.shape[0] - (window + 1) * window_height
#         y_coord_high = image.shape[0] - window * window_height

#         xleft_low = leftx_current - margin
#         xleft_high = leftx_current + margin
#         xright_low = rightx_current - margin
#         xright_high = rightx_current + margin
#         #left_start = (leftx_current - margin, y_coord)
#         #right_start = (rightx_current - margin, y_coord)

#         #left_end = (leftx_current + margin, y_coord + window_height)
#         #right_end = (rightx_current + margin, y_coord + window_height)

#         cv2.rectangle(out_image, (xleft_low, y_coord_low), (xleft_high, y_coord_high), color = (0, 255, 0), thickness = 2)
#         cv2.rectangle(out_image, (xright_low, y_coord_low), (xright_high, y_coord_high), color = (0, 255, 0), thickness = 2)

#         #plt.imshow(out_image)

#         #good_left_inds = nonzerox[(nonzerox >= xleft_low) & (nonzerox <= xleft_high)]

#         good_left_inds = ((nonzerox >= xleft_low) & (nonzerox < xleft_high) & (nonzeroy >= y_coord_low) & (nonzeroy < y_coord_high)).nonzero()[0]
#         good_right_inds = ((nonzerox >= xright_low) & (nonzerox < xright_high) & (nonzeroy >= y_coord_low) & (nonzeroy < y_coord_high)).nonzero()[0]

#         #print("good left indices: ", good_left_inds)
#         #print("good left indices shape: ", good_left_inds.shape)

#         # good_left_inds = nonzero[((nonzerox >= xleft_low) & (nonzerox <= xleft_high)) & ((nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high))]
#         # good_right_inds = nonzero[((nonzerox >= xright_low) & (nonzerox <= xright_high)) & ((nonzeroy >= y_coord_low) & (nonzeroy <= y_coord_high))]

#         left_lane_indices.append(good_left_inds)
#         right_lane_indices.append(good_right_inds)

#         if len(good_left_inds) > min_pixels:
#             leftx_current = np.int(np.mean(nonzerox[good_left_inds]))

#         if len(good_right_inds) > min_pixels:
#             rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

#     left_lane_indices = np.concatenate(left_lane_indices)
#     right_lane_indices = np.concatenate(right_lane_indices)

#     leftx = nonzerox[left_lane_indices]
#     lefty = nonzeroy[left_lane_indices]
#     rightx = nonzerox[right_lane_indices]
#     righty = nonzeroy[right_lane_indices]

#     return leftx, lefty, rightx, righty, out_image

# def fit_polynomial(binary_warped):

#     leftx, lefty, rightx, righty, out_image = find_lane_pixels(binary_warped)

#     left_fit = np.polyfit(leftx, lefty, deg = 2)
#     right_fit = np.polyfit(rightx, righty, deg = 2)

#     ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0])

#     left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
#     right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

#     # viz
#     out_image[lefty, leftx] = [255, 0, 0]
#     out_image[righty, rightx] = [0, 0, 255]

#     plt.plot(left_fitx, ploty, color = 'yellow')
#     plt.plot(right_fitx, ploty, color = 'yellow')

#     return out_image

def find_lane_pixels(binary_warped):
    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)
    # Create an output image to draw on and visualize the result
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]//2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # HYPERPARAMETERS
    # Choose the number of sliding windows
    nwindows = 9
    # Set the width of the windows +/- margin
    margin = 100
    # Set minimum number of pixels found to recenter window
    minpix = 50

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(binary_warped.shape[0]//nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated later for each window in nwindows
    leftx_current = leftx_base
    rightx_current = rightx_base

    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window+1)*window_height
        win_y_high = binary_warped.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        # Draw the windows on the visualization image
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),
        (win_xleft_high,win_y_high),(0,255,0), 2) 
        cv2.rectangle(out_img,(win_xright_low,win_y_low),
        (win_xright_high,win_y_high),(0,255,0), 2) 
        
        # Identify the nonzero pixels in x and y within the window #
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
        (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
        (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
        
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    except ValueError:
        # Avoids an error if the above is not implemented fully
        pass

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    return leftx, lefty, rightx, righty, out_img


def fit_polynomial(binary_warped):
    # Find our lane pixels first
    leftx, lefty, rightx, righty, out_img = find_lane_pixels(binary_warped)

    # Fit a second order polynomial to each using `np.polyfit`
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    # Generate x and y values for plotting
    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )
    try:
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    except TypeError:
        # Avoids an error if `left` and `right_fit` are still none or incorrect
        print('The function failed to fit a line!')
        left_fitx = 1*ploty**2 + 1*ploty
        right_fitx = 1*ploty**2 + 1*ploty

    ## Visualization ##
    # Colors in the left and right lane regions
    out_img[lefty, leftx] = [255, 0, 0]
    out_img[righty, rightx] = [0, 0, 255]

    # Plots the left and right polynomials on the lane lines
    plt.plot(left_fitx, ploty, color='yellow')
    plt.plot(right_fitx, ploty, color='yellow')

    return out_img

if __name__ == "__main__":
    image = mpimg.imread("warped-example.jpg")

    out_image = fit_polynomial(image)
    plt.imshow(out_image)
    plt.show()