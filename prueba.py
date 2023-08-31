import cv2
import numpy as np
import argparse

def nothing(x):
    pass

# Load image with argparse

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Load image
image_path = args["image"]
image = cv2.imread(image_path)

# Resize image to 1280x720
up_width = 1280
up_height = 720
up_points = (up_width, up_height)
image = cv2.resize(image, up_points, interpolation=cv2.INTER_LINEAR)

# Create a window for the main image
cv2.namedWindow('image')

# Create a window for the mask with erosion and dilation
cv2.namedWindow('mask')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# Create trackbars for erosion and dilation
cv2.createTrackbar('Erode', 'image', 0, 10, nothing)
cv2.createTrackbar('Dilate', 'image', 0, 10, nothing)

# Set default values for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

while(1):
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    # Get current positions of erosion and dilation trackbars
    erode_size = cv2.getTrackbarPos('Erode', 'image')
    dilate_size = cv2.getTrackbarPos('Dilate', 'image')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    # Apply erosion and dilation
    kernel = np.ones((5, 5), np.uint8)
    erosion_dilation = cv2.erode(mask, kernel, iterations=erode_size)
    erosion_dilation = cv2.dilate(mask, kernel, iterations=dilate_size)

    # Display result image with erosion and dilation
    result = cv2.bitwise_and(image, image, mask=erosion_dilation)
    cv2.imshow('image', result)

    # Display mask with erosion and dilation
    mask_with_ed = cv2.bitwise_and(mask, mask, mask=erosion_dilation)
    cv2.imshow('mask', mask_with_ed)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
