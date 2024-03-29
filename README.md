# Nucleos-Detectar

## Indice 
- [Nucleos-Detectar](#nucleos-detectar)
  - [Indice](#indice)
  - [Requerimientos](#requerimientos)
  - [Conteo de personas entrando y saliendo de la playa](#conteo-de-personas-entrando-y-saliendo-de-la-playa)
    - [Datos .csv del conteo](#datos-csv-del-conteo)
    - [Procesamiento de los datos](#procesamiento-de-los-datos)
  - [Rangos threshold para detección de nucleos](#rangos-threshold-para-detección-de-nucleos)
  - [Eliminar arena de la imagen](#eliminar-arena-de-la-imagen)
  - [Interfaz gráfica](#interfaz-gráfica)
    - [Opciones interfaz](#opciones-interfaz)
  - [Pruebas con red neuronal SAM(Segment Anything Model)](#pruebas-con-red-neuronal-samsegment-anything-model)
  - [Calculo distancia en pixeles](#calculo-distancia-en-pixeles)
  - [Resultados](#resultados)
    - [Imagenes](#imagenes)
    - [Coordenadas de cada nucleo](#coordenadas-de-cada-nucleo)
    - [Pruebas con red neuronal SAM(Segment Anything Model)](#pruebas-con-red-neuronal-samsegment-anything-model-1)

## Requerimientos
- Python >= 3.8
- OpenCV 3.4.2
- Numpy 1.16.4
- Matplotlib 3.1.0
- Scipy 1.3.0
- Imutils 0.5.2
- argparse 1.1
- PySimpleGUI 4.18.2
## Conteo de personas entrando y saliendo de la playa
Se utiliza una red neuronal con diversos modelos la cual consiste de manera generalizada en el uso de bytetrack. Dadas las limitaciones de git no se puede incluir la red en el repositorio. En cambio se han añadido los datos que nos ha devuelto la red y los videos del conteo se encuentran subidos a onedrive
### Datos .csv del conteo
En la carpeta ```Datos_Conteo``` se encuentran los ficheros .csv que nos devuelve la red
### Procesamiento de los datos
Para procesar dichos datos del script y obtener las graficas para determinar la afluencia que ha habido en la playa se ha utilizado el siguiente script:

``` process_csv.py ```

Al ejecutar el fichero se puede ver la siguiente interfaz grafica:
![Captura_interfaz](./Raw_Images/Interfaz_process_csv.png)

- **Archivo**: Permite seleccionar el fichero csv que se quiere procesar.
- **Diagrama de lineas**: Muestra el diagrama de lineas de la afluencia de la playa a lo largo del tiempo en el cual se han tomado los datos.
- **Diagrama de barras**: Muestra el diagrama de barras de la afluencia de la playa con el numero total de una manera mas rapida.
- **Formato segundos**: Muestra el formato de los segundos en el eje x del diagrama de lineas.
- **Formato minutos**: Muestra el formato de los minutos en el eje x del diagrama de lineas.
- **Formato horas**: Muestra el formato de las horas en el eje x del diagrama de lineas.
- **Intervalo**: Permite modificar el intervalo de tiempo que se muestra en el eje x del diagrama de lineas.
- **Genero**: Muestra el diagrama de barras de la afluencia de la playa por genero.

## Rangos threshold para detección de nucleos
Para saber los rangos de threshold en hsv para realizar la detección de nucleos, se utilizó el siguiente script:

``` bgr_2_hsv.py ```

Nos permite de una manera visual a través de un menú simple saber los rangos de threshold que vamos a utilziar posteriormente para eliminar la arena de las imagenes para poder identificar cada uno de los elementos de la playa 

## Eliminar arena de la imagen
Para poder detectar los nucleos de la playa se ha realizado un proceso de eliminacion de la arena de la playa u otros detalles que no eran relevantes para la detección de los diversos nucleos de persona u objetos en la playa.Además de detectar los diversos contornos y numeración de cada uno de los posibles nucleos descartando los contornos muy grandes o muy pequeños para eliminar posible ruido.

Para realizar este proceso se ha utilizado el siguiente script:

``` substract_no_centroid.py ```

Además se ha realizado otro script en el cual de los contornos detectados se calcula el centroide de cada uno para poder calcular las distancias entre ellos de esa forma poder identificar los grupos de personas que se encuentran en la playa. Este script es el siguiente:

``` substract.py ```

## Interfaz gráfica
Se ha creado una interfaz grafica utilizando la librería PySimpleGui para poder realizar la detección de los nucleos de la playa de una forma mas sencilla y visual. Además de permitir modificar ciertos parametros como el tamaño de la elipse para la apertura y cierre de la imagen, o como otras opciones mas internas como tamaños de ciertas lineas etc... También permite al usuario decidir si quiere guardar las imagenes o mostrarlas , o si requiere los preprocesos realizados para llegar al resultado final.


El aspecto de la interfaz es el siguiente:
![Captura_interfaz](./Raw_Images/Captura_interfaz.png)
### Opciones interfaz
- **Imagen**: Permite seleccionar la imagen que se quiere procesar. Los formatos de imagen que puede leer son los siguientes: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .ppm, .pgm.
- **Tamaño morfologia**: Permite modificar el tamaño de la elipse para la apertura y cierre de la imagen.
- **Mostrar centroide**: Permite mostrar el centroide de cada nucleo detectado.
- **Guardar imagenes**: Guarda la imagen final con los nucleos detectados.
- **Mostrar imagenes**: Muestra la imagen final con los nucleos detectados.
- **Mostrar preprocesos**: Muestra las imagenes de los preprocesos realizados para llegar al resultado final.
- **Directorio de salida**: Permite seleccionar el directorio donde se guardaran las imagenes.
- **Debug options**: Opciones para cambiar ciertos parametros internos del script.

## Pruebas con red neuronal SAM(Segment Anything Model)
Se han realizado pruebas de segmentación con la SAM ya que este modelo nos permite realizar una segmentación de la imagen sin un entrenamiento previo de lo que, queremos detectar en la imagen. Ya que el modelo es de gran tamaño se han realizado las pruebas en google colab, para ello se ha utilizado el siguiente script:

``` Uso_de_SAM(meta)_segmentacion_playas.ipynb```
## Calculo distancia en pixeles
Para el calculo de las distancias se han testeado diferentes formas para poder saber una distancia aproximada. 

En este caso se han calculado 5 puntos en cada contorno que son 4 esquinas y el centroide y de ahí se trazan lineas con los otros nucleos que hay en la imagen.
Para calcular la distancia en pixeles entre los nucleos se ha utilizado el siguiente script:

``` find_distancepx.py```

## Resultados

### Imagenes 
Se encuentran diversas carpetas con los resultados pero los mas relevantes son los que se encuentra en la carpeta ``` Results_benidorm_centroids ``` donde se encuentran los resultados de la detección de nucleos de las imagenes de la playa. Especificando el tamaño de la elipse utilizada para la apertura y cierre.

También se encuentran las imagenes sin el calculo de los centroides en la carpeta ``` Results_benidorm_no_centroids ```.

### Coordenadas de cada nucleo

En las imagenes podemos observar que se calcula el centroide de los nucleos detectados, de cada centroide tiene un numero que es la posición que ocupan las coordenada en el array x_coords o y_coords. Los cuales se pueden guardar en un archivo .txt modificando una linea de codigo que se encuentra en el script ``` substract.py ```, también se puede consultar directamente el valor en el array en el codigo.

### Pruebas con red neuronal SAM(Segment Anything Model)
Las pruebas realizadas con la red neuronal SAM se encuentra en el siguiente enlace de onedrive:

https://unialicante-my.sharepoint.com/:f:/g/personal/laragones_mscloud_ua_es/EhXngXnfSbZBmffSeeqtxbgBgTHLTao7bFaDKtzAtlACxg?e=LwCjYk