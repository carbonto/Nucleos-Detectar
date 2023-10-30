import matplotlib.pyplot as plt
import cv2
import numpy as np

# Cargar las dos imágenes que deseas comparar
imagen1 = cv2.imread('3_beni_no_object.jpg')
imagen2 = cv2.imread('beach_result.jpg')

# Crear una nueva figura    
plt.figure(figsize=(20, 9))  # Ajusta el tamaño de la figura según tus necesidades

# Agregar la primera imagen a la figura y establecer un título
plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primera imagen
plt.imshow(cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB))  # Asegúrate de convertir BGR a RGB
plt.axis('off')  # Eliminar los ejes x e y
plt.title('Resultado final')  # Título para la primera imagen

# Agregar la segunda imagen a la figura y establecer un título
plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segunda imagen
plt.imshow(cv2.cvtColor(imagen2, cv2.COLOR_BGR2RGB))  # Asegúrate de convertir BGR a RGB
plt.axis('off')  # Eliminar los ejes x e y
plt.title('Contour Aproximation')  # Título para la segunda imagen


# Ajustar los márgenes y mostrar la figura
plt.tight_layout()
plt.show()

