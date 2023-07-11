import cv2
import numpy as np

# Función para eliminar la arena y detectar los núcleos en una imagen aérea de la playa
def detectar_nucleos(image):
    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir rangos de colores para la arena
    lower_sand = np.array([0, 20, 20])
    upper_sand = np.array([40, 255, 255])

    # Segmentar la imagen en función del rango de colores de la arena
    mask_sand = cv2.inRange(hsv, lower_sand, upper_sand)

    # Aplicar operaciones morfológicas para eliminar ruido y mejorar la detección de los núcleos
    kernel = np.ones((5, 5), np.uint8)
    mask_sand = cv2.morphologyEx(mask_sand, cv2.MORPH_OPEN, kernel)
    mask_sand = cv2.morphologyEx(mask_sand, cv2.MORPH_CLOSE, kernel)

    # Aplicar operación de resta para eliminar la arena de la imagen original
    result = cv2.subtract(image, cv2.cvtColor(mask_sand, cv2.COLOR_GRAY2BGR))

    # Convertir la imagen resultante a escala de grises
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo para obtener una imagen binaria
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Encontrar los contornos de los núcleos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en la imagen original
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    # Calcular y mostrar las distancias entre los núcleos
    for i in range(len(contours)):
        for j in range(i + 1, len(contours)):
            contour_i = contours[i]
            contour_j = contours[j]
            distance = cv2.pointPolygonTest(contour_i, tuple(contour_j[0][0]), True)
            cv2.putText(image, f"{distance:.2f}", tuple(contour_j[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

# Cargar la imagen
image_path = "aerial_image.jpg"
image = cv2.imread(image_path)

# Procesar la imagen para eliminar la arena y detectar los núcleos
processed_image = detectar_nucleos(image)

# Mostrar la imagen original y la imagen procesada
cv2.imshow("Imagen Original", image)
cv2.imshow("Imagen Procesada", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
