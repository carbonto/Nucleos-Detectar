# Nucleos-Detectar

## Indice 
- [Nucleos-Detectar](#nucleos-detectar)
  - [Indice](#indice)
  - [Requerimientos](#requerimientos)
  - [Rangos threshold para detección de nucleos](#rangos-threshold-para-detección-de-nucleos)

## Requerimientos
- Python 3.6
- OpenCV 3.4.2
- Numpy 1.16.4
- Matplotlib 3.1.0


## Rangos threshold para detección de nucleos
Para saber los rangos de threshold en hsv para realizar la detección de nucleos, se utilizó el siguiente script:

``` bgr_2_hsv.py ```

El cual se ejecuta de la siguiente manera:

``` python bgr_2_hsv.py --image <path_to_image> ```

Nos permite de una manera visual a través de un menú simple saber los rangos de threshold que vamos a utilziar posteriormente para eliminar la arena de las imagenes para poder identificar cada uno de los elementos de la playa 

## Eliminar arena de la imagen
Para poder detectar los nucleos de la playa se ha realizado un proceso de eliminacion de la arena de la playa u otros detalles que no eran relevantes para la detección de los diversos nucleos de persona u objetos en la playa 

Para realizar este proceso se ha utilizado el siguiente script:

``` substract.py ```


## Resultados

### Imagenes 
Se encuentran diversas carpetas con los resultados pero los mas relevantes son los que se encuentra en la carpeta ``` Results_benidorm_images ``` donde se encuentran los resultados de la detección de nucleos de las imagenes de la playa. Especificando el tamaño de la elipse utilizada para la apertura y cierre.

### Coordenadas de cada nucleo

En las imagenes podemos observar que se calcula el centroide de los nucleos detectados, de cada centroide tiene un numero que es la posición que ocupan las coordenada en el array 

