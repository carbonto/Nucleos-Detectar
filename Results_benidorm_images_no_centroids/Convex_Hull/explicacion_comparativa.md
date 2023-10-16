PARA NUESTRA FINALIDAD NO SERÍA ADECUADO

Modificacion realizada en substract_no_centroids.py  

  #Convex hull
    for contours in contours:
        hull = cv2.convexHull(contours)
        cv2.drawContours(result, [hull], -1, (0, 0, 255), thick_countours)


Ambas técnicas, Convex Hull y FindContours, son utilizadas en visión por computadora para analizar la forma de objetos en una imagen. Aquí hay una breve comparación entre ambas:

1. **FindContours:**
   - **Descripción:** La función `cv2.findContours()` identifica y sigue los contornos de los objetos en una imagen.
   - **Salida:** Devuelve una lista de contornos, donde cada contorno es una lista de puntos que forman la forma del objeto.
   - **Uso:** Útil cuando necesitas conocer los detalles precisos de la forma del objeto y su jerarquía (relaciones de inclusión).

   ```python
   contornos, jerarquia = cv2.findContours(imagen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   ```

2. **Convex Hull:**
   - **Descripción:** La función `cv2.convexHull()` calcula el casco convexo de un conjunto de puntos.
   - **Salida:** Devuelve los puntos que forman el casco convexo del conjunto de entrada.
   - **Uso:** Útil cuando estás más interesado en la forma general del objeto y deseas simplificar la representación del contorno.

   ```python
   casco_convexo = cv2.convexHull(contorno)
   ```

**Comparación:**
- **Precisión de la Forma:**
  - `FindContours` proporciona detalles precisos sobre la forma del objeto, ya que devuelve todos los puntos del contorno.
  - `Convex Hull` proporciona una forma más simplificada del objeto, eliminando las concavidades.

- **Uso en Aplicaciones:**
  - `FindContours` es más adecuado cuando necesitas detalles precisos sobre la forma del objeto, como en aplicaciones de reconocimiento de caracteres, segmentación de objetos, etc.
  - `Convex Hull` es útil cuando estás más interesado en la forma general y deseas simplificar la representación del contorno, por ejemplo, en la detección de gestos, reconocimiento de mano, etc.

- **Eficiencia Computacional:**
  - `Convex Hull` tiende a ser más eficiente computacionalmente, ya que representa de manera más simple la forma general del objeto.
  - `FindContours` puede ser más costoso en términos de cómputo debido a la necesidad de calcular todos los puntos del contorno.

**Ejemplo Visual:**
- Si visualizas ambos métodos en la misma imagen, notarás que el casco convexo es una forma más "inflada" que sigue la silueta general del objeto.

En resumen, el método a elegir depende de la aplicación específica y de si estás más interesado en la forma detallada del objeto (`FindContours`) o en una representación más simple de su forma (`Convex Hull`). En muchos casos, ambos métodos pueden ser utilizados en conjunto para diferentes propósitos dentro de una aplicación más amplia.