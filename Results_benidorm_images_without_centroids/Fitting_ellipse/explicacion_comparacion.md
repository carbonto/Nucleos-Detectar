Con la elipse dada la perspectiva, se pueden delimitar los nucleos de una manera adecuada muy similar la funcion de dibujar contornos

Modifacion en el codigo realizada

```python
for contours in contours:
        #Adjust elipse to contour
        ellipse = cv2.fitEllipse(contours)

        #Draw elipse
        cv2.ellipse(result, ellipse, (0,255,0), 2)
```


**Contornos Simples:**
- **Representación:** Los contornos normales son líneas verdes que siguen con precisión la silueta de los objetos en la imagen, proporcionando una representación detallada de la forma y la estructura de cada objeto.
- **Cómputo:** Estos contornos son secuencias de puntos que definen el límite externo de cada objeto en la imagen.
- **Uso:** Son útiles cuando se requiere información detallada sobre la forma exacta de los objetos, como en aplicaciones de reconocimiento de formas o análisis de estructuras detalladas.

**Ajuste de Elipse:**
- **Representación:** Las elipses de ajuste son elipses azules que representan la mejor elipse que se ajusta al contorno de cada objeto. Proporcionan una visión más simplificada y compacta de la forma externa de los objetos.
- **Cómputo:** Se calcula la elipse que minimiza la diferencia entre los puntos del contorno y la forma elíptica ajustada.
- **Uso:** Es útil cuando la forma exacta del objeto no es crítica, y se busca una representación más compacta para propósitos como seguimiento de objetos o análisis de posición y tamaño general.

**Comparación Visual:**
- Observando ambas representaciones, los contornos normales muestran detalles precisos de la forma, mientras que las elipses de ajuste proporcionan una visión más general y simplificada, destacando la posición y el tamaño.

Esta comparación visual puede ayudarte a entender la diferencia entre utilizar contornos simples y ajuste de elipse en función de tus necesidades específicas de análisis de imagen.