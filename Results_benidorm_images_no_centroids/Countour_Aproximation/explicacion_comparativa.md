Realizar mas pruebas con el codigo 

Modificacion realizada en el codigo 

``` # Itera a través de los contornos y realiza la aproximación poligonal
    for contours in contours:
        epsilon = 0.02 * cv2.arcLength(contours, True) #Modify this value to get more or less points
        approx = cv2.approxPolyDP(contours, epsilon, True)

        # Dibuja los contornos aproximados en la imagen original
        cv2.drawContours(result, [approx], -1, (0, 255, 0), 2)
```
