# Nucleos-Detectar

## Indice 
- [Nucleos-Detectar](#nucleos-detectar)
  - [Indice](#indice)
  - [Requerimientos](#requerimientos)
  - [Rangos threshold para detección de nucleos](#rangos-threshold-para-detección-de-nucleos)
  - [Eliminar arena de la imagen](#eliminar-arena-de-la-imagen)
  - [Pruebas con red neuronal SAM(Segment Anything Model)](#pruebas-con-red-neuronal-samsegment-anything-model)
  - [Resultados](#resultados)
    - [Imagenes](#imagenes)
    - [Coordenadas de cada nucleo](#coordenadas-de-cada-nucleo)
    - [Pruebas con red neuronal SAM(Segment Anything Model)](#pruebas-con-red-neuronal-samsegment-anything-model-1)

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

``` substract_no_centroid.py ```

Además se ha realizado otro script en el cual de los contornos detectados se calcula el centroide de cada uno para poder calcular las distancias entre ellos de esa forma poder identificar los grupos de personas que se encuentran en la playa. Este script es el siguiente:

``` substract.py ```
## Pruebas con red neuronal SAM(Segment Anything Model)
Se han realizado pruebas de segmentación con la SAM ya que este modelo nos permite realizar una segmentación de la imagen sin un entrenamiento previo de lo que, queremos detectar en la imagen. Ya que el modelo es de gran tamaño se han realizado las pruebas en google colab, para ello se ha utilizado el siguiente script:

``` Uso_de_SAM(meta)_segmentacion_playas.ipynb```

## Resultados

### Imagenes 
Se encuentran diversas carpetas con los resultados pero los mas relevantes son los que se encuentra en la carpeta ``` Results_benidorm_images ``` donde se encuentran los resultados de la detección de nucleos de las imagenes de la playa. Especificando el tamaño de la elipse utilizada para la apertura y cierre.

También se encuentran las imagenes sin el calculo de los centroides en la carpeta ``` Results_benidorm_images_without_centroids ```.

### Coordenadas de cada nucleo

En las imagenes podemos observar que se calcula el centroide de los nucleos detectados, de cada centroide tiene un numero que es la posición que ocupan las coordenada en el array x_coords o y_coords. Los cuales se pueden guardar en un archivo .txt modificando una linea de codigo que se encuentra en el script ``` substract.py ```, también se puede consultar directamente el valor en el array en el codigo.

### Pruebas con red neuronal SAM(Segment Anything Model)
Las pruebas realizadas con la red neuronal SAM se encuentra en el siguiente enlace de onedrive:

https://unialicante-my.sharepoint.com/:f:/g/personal/laragones_mscloud_ua_es/EhXngXnfSbZBmffSeeqtxbgBgTHLTao7bFaDKtzAtlACxg?e=LwCjYk