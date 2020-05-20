# **Finding Lane Lines on the Road**

[gray]: ./assets/grayscale.jpg "grayscale image"

[gaussian_blur]: ./assets/gaussian_blur.jpg "Gaussian blurred image"

[canny]: ./assets/canny.jpg "Canny edge detection"

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



**3. Hough Transformation**

Edge detection will find edges, but in their current form, the representations of these edges take up much more space than needed (represented by ALL of their constituent pixels), and also may not give crucial linear structural information, which is desired for this project. Classicaly slope-intercept representations of lines are good in that they only depend on two changing parameters: m (slope) and b (y-intercept). However, this representation is flawed in that it cannot be used to represent vertical lines, as they have an undefined slope. Transforming lines into Hough space allows us to represent such lines in a manner that also only relies on two parameters (phi and theta), while also handling lines in all possible orientations. Additionally, any such line can be represented with phi and theta, which are both bounded (phi at or above 0, and theta between 0 and 2pi), unlike the parameters in point-slope form. Thus, the Hough transform is used to extract structured representations of lines from the edges detected by the Canny algorithm.  


The Hough space has the unique property of mapping lines in Cartesian space to points in Hough space. A consequence of this is that actual lines in Cartesian space become the intersection of curves in Hough space. This means that, all that is needed to find line passing through two points is find the intersection of the curves of those two points in Hough space.  

As mentioned earlier, Hough space is used for feature extraction. In this case, these features are only lines, although the Hough transform has also been adapted to handle non-linear features. Here's what an image would look like at the current stage of the pipeline:

![alt text][canny]

