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

### Global variables for contours
MIN_CONTOUR_AREA = 100
MAX_CONTOUR_AREA = 10000

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

def process_image(file,size,show_object,show_centroid,save_image,show_results,output_dir,save_preprocess,thick_countours,size_points,size_object):
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
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  ## External better than tree for this case because we only want the external contour
    #cv2.drawContours(result, cnts, -1, (0,255,0), thick_countours)

    cnts = cnts[0] if imutils.is_cv4() else cnts[1]

    # sort the contours from left-to-right and initialize the bounding box point colors
    # also you can sort rigth to left or top to bottom or bottom to top
    (cnts, _) = contours.sort_contours(cnts)
    #colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
    colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
        (255, 0, 255))
    
    # loop over the contours individually
    for (i, c) in enumerate(cnts):
        # if the contour is not sufficiently large, ignore it
        print(cv2.contourArea(c))
        if cv2.contourArea(c) < MIN_CONTOUR_AREA or cv2.contourArea(c) > MAX_CONTOUR_AREA:
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

        if show_centroid:
            center_x = int((rect[0][0] + rect[1][0] + rect[2][0] + rect[3][0]) / 4)
            center_y = int((rect[0][1] + rect[1][1] + rect[2][1] + rect[3][1]) / 4)

            # Dibujar un círculo en el centro
            cv2.circle(result, (center_x, center_y),size_points, (0, 255, 0), -1)


        # show the re-ordered coordinates
        print(rect.astype("int"))
        print("")

        # loop over the original points and draw them
        for ((x, y), color) in zip(rect, colors):
            cv2.circle(result, (int(x), int(y)), size_points, color, -1)
        
        if show_object:
            # draw the object num at the top-left corner
            size_object = 0.4
            cv2.putText(result, "Nucleo#{}".format(i + 1),
                (int(rect[0][0] - 15), int(rect[0][1] - 15)),
                cv2.FONT_HERSHEY_SIMPLEX, size_object, (255, 255, 255), 2)
            # show the image
            # cv2.imshow("Image", result)
            # cv2.waitKey(0)

    if save_image:
        if save_preprocess:
            cv2.imwrite(os.path.join(output_dir,'beach_thresh.jpg'), thresh)
            cv2.imwrite(os.path.join(output_dir,'beach_morph.jpg'), morph)
            cv2.imwrite(os.path.join(output_dir,'beach_mask.jpg'), mask)
        cv2.imwrite(os.path.join(output_dir,'beach_result.jpg'), result)
    if show_results:
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
        [sg.Checkbox("Mostrar numero nucleo", key="-OBJECT-", default=True)],
        [sg.Checkbox("Mostrar centroide", key="-CENTROID-", default=True)],
        [sg.Checkbox("Guardar imagenes", key="-SAVE-", default=True)],
        [sg.Checkbox("Mostrar imagenes", key="-SHOW-", default=True)],
        [sg.Checkbox("Guardar preprocesos", key="-SAVE_PREPROCESS-", default=False)],
        [sg.Text("Directorio de salida"),sg.InputText(key="-OUTPUT-"), sg.FolderBrowse()],
        [sg.Text("Debug options")],
        [sg.Text("Thick contour:"), sg.InputText(key="-CONTOUR-", size=(10, 1), default_text="1")],
        [sg.Text("Size points:"), sg.InputText(key="-SIZE_POINTS-", size=(10, 1), default_text="2")],
        [sg.Text("Size object:"), sg.InputText(key="-SIZE_OBJECT-", size=(10, 1), default_text="0.4")],
        [sg.Button("Procesar"), sg.Button("Salir")]
    ]

    #Create window application
    window = sg.Window("Procesador de Imágenes",layout)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Salir":
            break

        if event == "Procesar":
            ruta_imagen = values["-FILE-"]
            size = int(values["-SIZE-"]) 
            show_object = values["-OBJECT-"]
            show_centroid = values["-CENTROID-"]
            save_image = values["-SAVE-"]
            show_results = values["-SHOW-"]
            output_dir = values["-OUTPUT-"]
            save_preprocess = values["-SAVE_PREPROCESS-"]
            thick_countours = int(values["-CONTOUR-"])
            size_points = int(values["-SIZE_POINTS-"])
            size_object = float(values["-SIZE_OBJECT-"])

            if not os.path.exists(output_dir):
                sg.popup_error("Directorio de salida no existe")
                continue

            if ruta_imagen:
                process_image(ruta_imagen,size,show_object,show_centroid,save_image,show_results,output_dir,save_preprocess,thick_countours,size_points,size_object)

    # Cerrar la ventana de la aplicación
    window.close()


   
if __name__ == '__main__':
    main()   