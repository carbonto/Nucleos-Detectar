import cv2
import numpy as np

# Función para eliminar la arena y detectar los núcleos en una imagen aérea de la playa
def detectar_nucleos(image):
    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir rangos de colores para la arena

    #Rangos arena para sin_palmeras.jpg
    lower_sand = np.array([16, 12, 105])
    upper_sand = np.array([30, 68, 245])

    #Rangos arena para aerea_full.jpg
    # lower_sand = np.array([6, 15, 221])
    # upper_sand = np.array([179, 255, 255])

    # lower_sand = np.array([10, 50, 50])
    # upper_sand = np.array([30, 255, 255])

    # Segmentar la imagen en función del rango de colores de la arena
    mask_sand = cv2.inRange(hsv, lower_sand, upper_sand)
    cv2.imshow("mask sand", mask_sand)  ########DEBUG
    cv2.waitKey(0)
    # Aplicar operaciones morfológicas para eliminar ruido y mejorar la detección de los núcleos
    kernel = np.ones((5, 5), np.uint8)
    mask_sand = cv2.morphologyEx(mask_sand, cv2.MORPH_OPEN, kernel)
    mask_sand = cv2.morphologyEx(mask_sand, cv2.MORPH_CLOSE, kernel)

    # Aplicar operación de resta para eliminar la arena de la imagen origina
    result = cv2.subtract(image, cv2.cvtColor(mask_sand, cv2.COLOR_GRAY2BGR))

    cv2.imshow("sinarena", result) #######DEBUG
    cv2.waitKey(0)
    # Convertir la imagen resultante a escala de grises
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo para obtener una imagen binaria
    ## FIX 
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow("sinarena", thresh)
    cv2.waitKey(0)

    # Encontrar los contornos de los núcleos 
    # FIX  
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en la imagen original
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    return image

# Cargar la imagen
image_path = "sin_palmeras.jpg"
image = cv2.imread(image_path)

# Procesar la imagen para eliminar la arena y detectar los núcleos
processed_image = detectar_nucleos(image)

#Resize image
up_width = 600
up_height = 400
up_points = (up_width, up_height)
resized_up = cv2.resize(image, up_points, interpolation= cv2.INTER_LINEAR)

# Mostrar la imagen original y la imagen procesada
cv2.imshow("image", resized_up)

cv2.imshow("Imagen Procesada", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
