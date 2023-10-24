from __future__ import print_function
import cv2
import numpy as np
from imutils import perspective
from imutils import contours
import imutils
import argparse
from scipy.spatial import distance as dist
import PySimpleGUI as sg
import os


def order_points_old(pts):
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

##### This way works better in our case
def order_points(pts):
    # sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl], dtype="float32")



#To get de color ranges of each image each image has lower numpy array and upper numpy array
def get_color_ranges(file):

    file_name = os.path.basename(file)
    color_ranges = {
        'sin_palmeras.jpg': (np.array([16, 12, 105]), np.array([30, 68, 245])),
        'aerea_full.jpg': (np.array([6, 15, 221]), np.array([179, 255, 255])),
        'prueba.png': (np.array([9, 14, 163]), np.array([84, 51, 255])),
        'captura_benidorm_1.JPG': (np.array([12, 31, 114]), np.array([82, 61, 223])),
        'partially_seg_SAM.jpg': (np.array([0, 158, 139]), np.array([179, 255, 255])),
        '1_beni.jpg': (np.array([14, 14, 137]), np.array([21, 108, 220])),
        '2_beni.jpg': (np.array([14, 40, 120]), np.array([24, 86, 215])),
        '3_beni.jpg': (np.array([11, 42, 117]), np.array([92, 93, 200])),
        '1_posti.jpg': (np.array([11, 27, 122]), np.array([28, 77, 213])),
        '2_posti.jpg': (np.array([8, 8, 152]), np.array([45, 69, 219])),
        '3_posti.jpg': (np.array([11, 43, 107]), np.array([26, 105, 181])),
    }
    return color_ranges.get(file_name, (None, None))

def process_image(file,size,show_object):
    # Load image
    img = cv2.imread(file)
    img= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hh, ww = img.shape[:2]

    # Rangos de color para cada imagen
    lower, upper = get_color_ranges(file)
    if lower is None or upper is None:
        sg.popup_error("Rangos de color no definidos para la imagen")
        return

    ##### NO IMPROVES WITH GAUSSIAN BLUR
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow('gaussian', img)

    # Create mask to only select none and
    thresh = cv2.inRange(img, lower, upper)

    # apply morphology
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

    cnts = cnts[0] if imutils.is_cv4() else cnts[1]

    # sort the contours from left-to-right and initialize the bounding box
    # point colors
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

    # loop over the contours individually
    for (i, c) in enumerate(cnts):
        # if the contour is not sufficiently large, ignore it
        print(cv2.contourArea(c))
        if cv2.contourArea(c) < 100 or cv2.contourArea(c) > 10000:
            continue
        
        # compute the rotated bounding box of the contour, then
        # draw the contours
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        cv2.drawContours(result, [box], -1, (0, 255, 0), thick_countours)

        # show the original coordinates
        print("Object #{}:".format(i + 1))
        #print(box)

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box 
        rect = perspective.order_points(box)

        # show the re-ordered coordinates
        print(rect.astype("int"))
        print("")

        # loop over the original points and draw them
        size_points = 2
        for ((x, y), color) in zip(rect, colors):
            cv2.circle(result, (int(x), int(y)), size_points, color, -1)
        
        if show_object:
            # draw the object num at the top-left corner
            size_object = 0.4
            cv2.putText(result, "Object #{}".format(i + 1),
                (int(rect[0][0] - 15), int(rect[0][1] - 15)),
                cv2.FONT_HERSHEY_SIMPLEX, size_object, (255, 255, 255), 2)
            # show the image
            # cv2.imshow("Image", result)
            # cv2.waitKey(0)

    
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



def main():
    # Define design of graphical interface
    layout = [
        [sg.Text("Selecciona una imagen para procesar")],
        [sg.InputText(key="-FILE-"), sg.FileBrowse()],
        [sg.Text("Tamaño de Morfología:"), sg.InputText(key="-SIZE-", size=(10, 1), default_text="10")],
        [sg.Checkbox("OBJ", key="-OBJECT-", default=True)],
        [sg.Button("Procesar"), sg.Button("Salir")]
    ]

    #Create window application
    window = sg.Window("Procesador de Imágenes", layout)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Salir":
            break
        elif event == "Procesar":
            ruta_imagen = values["-FILE-"]
            size = int(values["-SIZE-"]) 
            show_object = values["-OBJECT-"]
            if ruta_imagen:
                process_image(ruta_imagen,size,show_object)

    # Cerrar la ventana de la aplicación
    window.close()


   
if __name__ == '__main__':
    main()   