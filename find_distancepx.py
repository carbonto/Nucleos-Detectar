# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
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
    file = 'Raw_Images/3_beni.jpg'
    img = cv2.imread(file)
    up_width = 1280
    up_height = 720
    up_points = (up_width, up_height)
    img = cv2.resize(img, up_points, interpolation= cv2.INTER_LINEAR)
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
    size = 10    # can change this value depends the image
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
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  ## External better than tree for this case because we only want the external contour
    #cv2.drawContours(result, cnts, -1, (0,255,0), thick_countours)
    cnts = cnts[1] if imutils.is_cv3() else cnts[0]

    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
        (255, 0, 255))
    refObj = None

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 10000:
            continue

        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)

        # compute the center of the bounding box
        cX = np.average(box[:, 0])
        cY = np.average(box[:, 1])

        # if this is the first contour we are examining (i.e.,
        # the left-most contour), we presume this is the
        # reference object
        if refObj is None:
            # unpack the ordered bounding box, then compute the
            # midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-right and
            # bottom-right
            (tl, tr, br, bl) = box
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            # compute the Euclidean distance between the midpoints,
            # then construct the reference object
            D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            refObj = (box, (cX, cY), D)
            continue

        # draw the contours on the image
        orig = result.copy()
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), thick_countours)
        cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), thick_countours)

        # stack the reference coordinates and the object coordinates
        # to include the object center
        refCoords = np.vstack([refObj[0], refObj[1]])
        objCoords = np.vstack([box, (cX, cY)])

        # loop over the original points
        for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
            # draw circles corresponding to the current points and
            # connect them with a line
            cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
            cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
            cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                color, 2)

            # compute the Euclidean distance between the coordinates,
            # and then convert the distance in pixels to distance in
            # units
            D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
            (mX, mY) = midpoint((xA, yA), (xB, yB))
            cv2.putText(orig, "{:.1f}px".format(D), (int(mX), int(mY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
            cv2.imshow("Image", orig)
            cv2.waitKey(0)

        # update the reference object to be the current contour
        refObj = (box, (cX, cY), 1.0)

        # show the output image
        # cv2.imshow("Image", orig)
        # cv2.waitKey(0)
    
if __name__ == '__main__':
    main()