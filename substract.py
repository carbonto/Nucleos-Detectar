import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk

#To get de color ranges of each image each image has lower numpy array and upper numpy array
def get_color_ranges(file):
    color_ranges = {
        'sin_palmeras.jpg': (np.array([16, 12, 105]), np.array([30, 68, 245])),
        'aerea_full.jpg': (np.array([6, 15, 221]), np.array([179, 255, 255])),
        'prueba.png': (np.array([9, 14, 163]), np.array([84, 51, 255])),
        'captura_benidorm_1.JPG': (np.array([12, 31, 114]), np.array([82, 61, 223])),
        'partially_seg_SAM.jpg': (np.array([0, 158, 139]), np.array([179, 255, 255])),
        'Raw_Images/1_beni.jpg': (np.array([14, 14, 137]), np.array([21, 108, 220])),
        'Raw_Images/2_beni.jpg': (np.array([14, 40, 120]), np.array([24, 86, 215])),
        'Raw_Images/3_beni.jpg': (np.array([11, 42, 117]), np.array([92, 93, 200])),
        'Raw_Images/1_posti.jpg': (np.array([11, 27, 122]), np.array([28, 77, 213])),
        'Raw_Images/2_posti.jpg': (np.array([8, 8, 152]), np.array([45, 69, 219])),
        'Raw_Images/3_posti.jpg': (np.array([11, 43, 107]), np.array([26, 105, 181])),
    }
    return color_ranges.get(file, (None, None))
def main():
    # Read image
    file = 'Raw_Images/2_beni.jpg'
    img = cv2.imread(file)
    img= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hh, ww = img.shape[:2]

    # Rangos de color para cada imagen
    lower, upper = get_color_ranges(file)
    if lower is None or upper is None:
        print("Rangos de color no definidos para la imagen")
        return

    ##### NO IMPROVES WITH GAUSSIAN BLUR
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow('gaussian', img)

    # Create mask to only select none and
    thresh = cv2.inRange(img, lower, upper)

    # apply morphology
    size = 15     # can change this value depends the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size,size),anchor=(size//2,size//2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)


    # invert morp image
    mask = 255 - morph

    # apply mask to image
    result = cv2.bitwise_and(img, img, mask=mask)

    # hsv to bgr
    result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    #draw contours
    thick_countours = 1
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  ## External better than tree for this case because we only want the external contour
    cv2.drawContours(result, contours, -1, (0,255,0), thick_countours)

    ## Aproximate centroid of contour
    value = 0
    x_coords = []
    y_coords = []
    circle_size = 7
    number_size = 0.5
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(result, [i], -1, (0, 255, 0), 1)
            cv2.circle(result, (cx, cy), circle_size, (0, 0, 255), -1)
            value = value + 1
            cv2.putText(result, str(value), (cx - 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, number_size, (0, 0, 0), 2)
        
        x_coords.append(cx)
        y_coords.append(cy)
        # x_coords = np.append(x_coords, "x:" + str(cx))
        # y_coords = np.append(y_coords, "y:" + str(cy))
        #print(x_coords,y_coords)
        print(f"x: {cx} y: {cy}")

    # save results
    #save txt of list
    # np.savetxt('x_coords.txt', x_coords, fmt='%s')
    # np.savetxt('y_coords.txt', y_coords, fmt='%s')
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

if __name__ == '__main__':
    main()   