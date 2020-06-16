import numpy as np
import matplotlib.pyplot as plt

def generate_data(ym_per_pix, xm_per_pix):
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
    # additionally, adjust to real-world curvature rather than pixel-space curvature
    left_fit = np.polyfit(ploty * ym_per_pix, leftx * xm_per_pix, 2)
    right_fit = np.polyfit(ploty * ym_per_pix, rightx * xm_per_pix, 2)
    
    return ploty, left_fit, right_fit

def measure_curvature_pixels():

    ym_per_pix = 30 / 720
    xm_per_pix = 3.7 / 700

    ploty, left_fit, right_fit = generate_data(ym_per_pix, xm_per_pix)

    y_eval = np.max(ploty)
    y_eval *= ym_per_pix

    left_curve_rad = ((1 + (2 * left_fit[0] * y_eval + left_fit[1]) ** 2) ** (3 / 2)) / abs(2 * left_fit[0])
    right_curve_rad = ((1 + (2 * right_fit[0] * y_eval + right_fit[1]) ** 2) ** (3 / 2)) / abs(2 * right_fit[0])

    return left_curve_rad, right_curve_rad

if __name__ == "__main__":

    left_curverad, right_curverad = measure_curvature_pixels()

    # pixel-space expected: 1625.06, 1976.30
    # real-world space expected: 533.75, 648.16
    print(left_curverad, right_curverad)