# **Finding Lane Lines on the Road**

[gray]: ./assets/grayscale.jpg "grayscale image"

[gaussian_blur]: ./assets/gaussian_blur.jpg "Gaussian blurred image"

[canny]: ./assets/canny.jpg "Canny edge detection"

[hough_transform_nocolor]: ./assets/hough_transform_nocolor.jpg "Initial Hough transform"

[hough_transform_slopethresholding]: ./assets/hough_transform_slopethreshold.jpg "Hough transform with slope thresholding"

[hough_transform_extended]: ./assets/hough_transform_extended.jpg "Hough transform extended to meet ends of the lane"



## Project Report

### Pipeline Overview

My lane detection pipeline consists of several major steps, each operating on single images. For video intake, the entire pipeline is simply run on individual frames in sequence.

The major steps are as follows:  


**1. Image intake and pre-processing**

In this stage, an image is read into memory (outside of the function) and passed into the pipeline as an argument. The image is first converted to the grayscale image format, in which all color channels are removed. This leaves us with a single channel image, where each pixel represents the intensity of light at that point instead, rather than a color. In grayscale images, white represents points with the highest intensity, while black represents points with the lowest intensity; anything in between is gray, as the name implies. Unlike the original RGB color image, where each pixel has varying levels of red, green, and blue (where each channel takes values in [0, 255]), grayscale typically constricts each pixel's range to only [0, 1].  


![alt text][gray]

Grayscale is particularly helpful for edge detection (a key component of this pipeline) since edge detection revolves around identifying areas of high gradient change. That is, it locates areas in an image where there is a heavy change in intensity. Grayscaling simplifies this process by making the differences in intensity the core of its representation. If given two RGB pixels, the contrast is much less trivial to detect, whereas it is infinitely easier in grayscale since it simplifies to a straightforward comparison of their single pixel values.  


The next step of the pre-processing stage is Gaussian blurring (though this is done in the Canny edge detection step already). Gaussian blurring is also useful for edge detection because it eliminates noise from images. In this use case, noise refers to minor, stray edges that our edge detector might otherwise pick up if left in. Gaussian blurring leaves the image in a state such that only the most prominent edges will be left behind, specifically major marks such as lane lines (both dashed and continuous). Blurs by their very nature remove sharpness, which causes minor edges to disappear.  


![alt text][gaussian_blur]


**2. Edge detection**

As mentioned previously, edge detection is a keystone of the entire pipeline. Edge detection finds areas in the image that have more than some pre-defined change in value. This is implemented as a threshold of accepted values. Such areas are returned as a mask over the otherwise blank space, which did not meet the threshold. Below is what the image would look like at this stage of the pipeline.  

![alt text][canny]

**3. Hough Transformation**

Edge detection will find edges, but in their current form, the representations of these edges take up much more space than needed (represented by ***all*** of their constituent pixels), and also may not give crucial linear structural information, which is desired for this project. Classicaly slope-intercept representations of lines are good in that they only depend on two changing parameters: m (slope) and b (y-intercept). However, this representation is flawed in that it cannot be used to represent vertical lines, as they would have an undefined slope. Transforming lines into Hough space allows us to represent such lines in a manner that also only relies on two parameters (rho and theta), while also handling lines in all possible orientations. Additionally, any such line can be represented with rho and theta, which are both bounded (rho at or above 0, and theta between 0 and 2pi), unlike the parameters in point-slope form. Thus, the Hough transform is used to extract structured representations of lines from the edges detected by the Canny algorithm.  


The Hough space has the unique property of mapping lines in Cartesian space to points in Hough space. A consequence of this is that actual lines in Cartesian space become the intersection of curves in Hough space. This means that, all that is needed to find line passing through two points is find the intersection of the curves of those two points in Hough space.  


As mentioned earlier, Hough transformations are used for feature extraction. In this case, these features are only lines, although the Hough transform has also been adapted to handle non-linear features. To reduce the number of lines detected to only those we're concerned with (lines on the road ahead of the driver), a region of interest mask is imposed on the image, and this is where the Hough transformation will take place. Here's what an image would look like at the current stage of the pipeline:

![alt text][hough_transform_nocolor]

  



**4. Line estimation and Post-processing**

As you can see, the result is not the most helpful for our end goal. There are stray lines even in this straightforward image, even after applying a region of interest. Additionally, there is more than one line per lane line, and we want to avoid confusing the car by limiting this to one line per lane line. Finally, these lines, except sometimes the continuous line  on one side of the road, do not extend to the full reach of the lane (in other words, from the car to the "horizon"). These problems are what I'll address next.

First, after lines are extracted in the Hough transformation step, lines that are unlikely to be lane markings are filtered out from the set of detected lines. This is done by thresholding the slope of each line; lines with very high (greater than or equal to 5) or very low (less than or equal to 0.5) slopes are very steep or near horizontal, thus making them unlikely candidates for lane lines. Of course, that only applies to left lane lines, since right lane lines have a negative slope (coordinates were returned in left-to-right order). So the process was also applied to the negated threshold above, and these lines were then separated by their position in the lane. This results in the image below, which contains no stray lines:

![alt text][hough_transform_slopethresholding]

Directly after this, the lines were extended to meet the horizon and car camera. The most sensible way I though of doing this would be to find the points of intersection between the current lines and the lines making up the top and bottom of the region of interest mask. The function `point_of_intersection()` takes in two 4-tuples, each representing the 2 points needed to represent a line, and calculates an integer-only point of intersection. In the rare case that the lines are parallel, a tuple of `maxsize` is returned. However, in these cases this condition is never satisfied. Below is the result after getting this far:

![alt text][hough_transform_extended]

However, this still left behind multiple lines per lane line. To remedy this, the lines belonging to the left and right sides of the lane were aggregated and averaged componentwise by their coordinate points (i.e. all x1's were averaged against each other, all y2's against each other, etc.). Since their slopes were similar, the resultant average line for both sides would be nearly parallel to the original lines from which it was derived.