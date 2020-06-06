import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


left_fit = np.array([2.13935315e-04, -3.77507980e-01,  4.76902175e+02])
right_fit = np.array([4.17622148e-04, -4.93848953e-01,  1.11806170e+03])


def fit_poly(image_shape, leftx, lefty, rightx, righty):

    # fit second order polynomials to both lane lines
    left_fit = np.polyfit(lefty, leftx, deg = 2)
    right_fit = np.polyfit(righty, rightx, deg = 2)

    ploty = np.linspace(0, image_shape[0] - 1, image_shape[0])

    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    return left_fitx, right_fitx, ploty

def search_around_poly(binary_warped):

    margin = 100

    nonzero = binary_warped.nonzero()
    nonzerox = nonzero[1]
    nonzeroy = nonzero[0]

    poly_left = left_fit[0] * nonzeroy ** 2 + nonzeroy * left_fit[1] + left_fit[2]
    poly_right = right_fit[0] * nonzeroy ** 2 + nonzeroy * right_fit[1] + right_fit[2]

    left_lane_inds = ((nonzerox > poly_left - margin) & (nonzerox < poly_left + margin))
    right_lane_inds = ((nonzerox > poly_right - margin) & (nonzerox < poly_right + margin))

    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    left_fitx, right_fitx, ploty = fit_poly(binary_warped.shape, leftx, lefty, rightx, righty)

    out_image = np.dstack((binary_warped, binary_warped, binary_warped)) * 255
    window_image = np.zeros_like(out_image)

    out_image[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
    out_image[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]

    left_line_window1 = np.array([np.transpose(np.vstack([left_fitx - margin, ploty]))])
    left_line_window2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx + margin, ploty])))])
    left_line_pts = np.hstack((left_line_window1, left_line_window2))

    right_line_window1 = np.array([np.transpose(np.vstack([right_fitx - margin, ploty]))])
    right_line_window2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx + margin, ploty])))])
    right_line_pts = np.hstack((right_line_window1, right_line_window2))

    cv2.fillPoly(window_image, np.int_([left_line_pts]), (0, 255, 0))
    cv2.fillPoly(window_image, np.int_([right_line_pts]), (0, 255, 0))

    result = cv2.addWeighted(out_image, 1, window_image, 0.3, 0)

    plt.plot(left_fitx, ploty, color = "yellow")
    plt.plot(right_fitx, ploty, color = "yellow")

    return result


if __name__ == "__main__":

    binary_warped = mpimg.imread("warped-example.jpg")

    
    result = search_around_poly(binary_warped)

    plt.imshow(result)
    plt.show()