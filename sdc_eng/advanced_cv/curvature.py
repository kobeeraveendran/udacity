import numpy as np
import matplotlib.pyplot as plt

def generate_data():

    # generate fake data
    ploty = np.linspace(0, 719, num = 720)
    quadratic_coeff = 3e-4

    # generate random x position for each y within minpix range of base line
    leftx = np.array([200 + (y ** 2) * quadratic_coeff + np.random.randint(-50, high = 51) for y in ploty])
    leftx = leftx[::-1]

    rightx = np.array([900 + (y ** 2) * quadratic_coeff + np.random.randint(-50, high = 51) for y in ploty])
    rightx = rightx[::-1]

    left_fit = np.polyfit(ploty, leftx, 2)
    right_fit = np.polyfit(ploty, rightx, 2)

    return ploty, left_fit, right_fit

def measure_curvature_pixels():
    ploty, left_fit, right_fit = generate_data()

    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    y_eval = np.max(ploty)

    left_curve_rad = ((1 + (2 * left_fit[0] + ploty + left_fit[1]) ** 2) ** (3 / 2)) / np.abs(2 * left_fit[0])
    right_curve_rad = ((1 + (2 * right_fit[0] + ploty + right_fit[1]) ** 2) ** (3 / 2)) / np.abs(2 * right_fit[0])

    return left_curve_rad, right_curve_rad

if __name__ == "__main__":

    ploty, left_fit, right_fit = generate_data

    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    mark_size = 3
    plt.plot(leftx, ploty, 'o', color = 'red', markersize = mark_size)
    plt.plot(rightx, ploty, 'o', color = 'blue', markersize = mark_size)

    plt.xlim(0, 1280)
    plt.ylim(0, 720)

    plt.plot(left_fitx, ploty, color = 'green', linewidth = 3)
    plt.plot(right_fitx, ploty, color = 'green', linewidth = 3)

    plt.gca().invert_yaxis()

    plt.show()