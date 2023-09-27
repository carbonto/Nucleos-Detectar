import cv2
import numpy as np
import argparse

########### PROBAR CANNY #####################

# # Lee la imagen
# imagen = cv2.imread('partially_seg_SAM.jpg')

# # Convierte la imagen a escala de grises
# imagen_escala_de_grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)



# # Valores iniciales de los umbrales
# T2 = 500
# T1 = 0.4 * T2

# # Aplica la detección de bordes Canny
# bordes = cv2.Canny(imagen_escala_de_grises, int(T1), int(T2))

# #pasar a bgr

# # Muestra el resultado de la detección de bordes
# cv2.imshow('Bordes', bordes)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



## PRUEBA CONTORNOS SAM ##

# # Lee la imagen
mask = cv2.imread('segmented.jpg')
result = cv2.imread('segmented.jpg')

## grey scale
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

#draw contours
thick_countours = 1
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  ## External better than tree for this case because we only want the external contour
cv2.drawContours(result, contours, -1, (0,255,0), thick_countours)

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()