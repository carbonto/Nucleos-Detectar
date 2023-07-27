import cv2
import numpy as np

#To get de color ranges of each image each image has lower numpy array and upper numpy array
def get_color_ranges(file):
    color_ranges = {
        'sin_palmeras.jpg': (np.array([16, 12, 105]), np.array([30, 68, 245])),
        'aerea_full.jpg': (np.array([6, 15, 221]), np.array([179, 255, 255])),
        'prueba.png': (np.array([9, 14, 163]), np.array([84, 51, 255])),
        'captura_benidorm_1.JPG': (np.array([12, 31, 114]), np.array([82, 61, 223]))
    }
    return color_ranges.get(file, (None, None))
def main():
    # Read image
    file = 'captura_benidorm_1.JPG'
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
    size = 20
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
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(result, [i], -1, (0, 255, 0), 2)
            cv2.circle(result, (cx, cy), 7, (0, 0, 255), -1)
            value = value + 1
            cv2.putText(result, str(value), (cx - 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        print(f"x: {cx} y: {cy}")

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

if __name__ == '__main__':
    main()