import cv2
import numpy as np

# Read image
img = cv2.imread('sin_palmeras.jpg')
img= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hh, ww = img.shape[:2]

#Rangos para sin_palmeras.jpg
lower = np.array([16, 12, 105])
upper = np.array([30, 68, 245])

#Rangos arena para aerea_full.jpg
# lower = np.array([6, 15, 221])
# upper = np.array([179, 255, 255])

#Rangos para prueba.png
# lower = np.array([9, 14, 163])
# upper = np.array([84, 51, 255])

# Create mask to only select black
thresh = cv2.inRange(img, lower, upper)

# apply morphology
size = 20
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size,size))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# invert morp image
mask = 255 - morph

# apply mask to image
result = cv2.bitwise_and(img, img, mask=mask)

# hsv to bgr
result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

#draw contours
thick_countours = 1
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(result, contours, -1, (0,255,0), thick_countours)



# save results
cv2.imwrite('beach_thresh.jpg', thresh)
cv2.imwrite('beach_morph.jpg', morph)
cv2.imwrite('beach_mask.jpg', mask)
cv2.imwrite('beach_result.jpg', result)

cv2.imshow('thresh', thresh)
cv2.imshow('morph', morph)
cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()