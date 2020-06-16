import numpy as np
import matplotlib.pyplot as plt

def generate_data():
    '''
    Generates fake data to use for calculating lane curvature.
    In your own project, you'll ignore this function and instead
    feed in the output of your lane detection algorithm to
    the lane curvature calculation.
    '''
    # Set random seed number so results are consistent for grader
    # Comment this out if you'd like to see results on different random data!
    np.random.seed(0)
    # Generate some fake data to represent lane-line pixels
    ploty = np.linspace(0, 719, num=720)# to cover same y-range as image
    quadratic_coeff = 3e-4 # arbitrary quadratic coefficient
    # For each y position generate random x position within +/-50 pix
    # of the line base position in each case (x=200 for left, and x=900 for right)
    leftx = np.array([200 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])
    rightx = np.array([900 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])

    leftx = leftx[::-1]  # Reverse to match top-to-bottom in y
    rightx = rightx[::-1]  # Reverse to match top-to-bottom in y


    # Fit a second order polynomial to pixel positions in each fake lane line
    left_fit = np.polyfit(ploty, leftx, 2)
    right_fit = np.polyfit(ploty, rightx, 2)
    
    return ploty, left_fit, right_fit

def measure_curvature_pixels():
    ploty, left_fit, right_fit = generate_data()

    y_eval = np.max(ploty)

    left_curve_rad = np.power((1 + np.power(2 * left_fit[0] * y_eval + left_fit[1], 2)), 3 / 2) / np.abs(2 * left_fit[0])
    right_curve_rad = np.power((1 + np.power(2 * right_fit[0] * y_eval + right_fit[1], 2)), 3 / 2) / np.abs(2 * right_fit[0])

    #left_curve_rad = ((1 + (2 * left_fit[0] + ploty + left_fit[1]) ** 2) ** (3 / 2)) / np.abs(2 * left_fit[0])
    #right_curve_rad = ((1 + (2 * right_fit[0] + ploty + right_fit[1]) ** 2) ** (3 / 2)) / np.abs(2 * right_fit[0])

    return left_curve_rad, right_curve_rad

if __name__ == "__main__":

    left_curverad, right_curverad = measure_curvature_pixels()

    # expected: 1625.06, 1976.30
    print(left_curverad, right_curverad)

    # plt.xlim(0, 1280)
    # plt.ylim(0, 720)

    #plt.plot(left_fitx, ploty, color = 'green', linewidth = 3)
    #plt.plot(right_fitx, ploty, color = 'green', linewidth = 3)

    #plt.gca().invert_yaxis()

    #plt.show()