# Nucleos-Detectar

## Rangos threshold para detección de nucleos
Para saber los rangos de threshold en hsv para realizar la detección de nucleos, se utilizó el siguiente script:

``` bgr_2_hsv.py ```

El cual se ejecuta de la siguiente manera:

``` python bgr_2_hsv.py --image <path_to_image> ```

Nos permite de una manera visual a través de un menú simple saber los rangos de threshold que vamos a utilziar posteriormente para eliminar la arena de las imagenes para poder identificar cada uno de los elementos de la playa 