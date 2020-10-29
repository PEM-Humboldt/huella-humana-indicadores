# huella-humana-indicadores
Este repositorio contiene dos herramienta para crear las capas geográficas vectoriales con los indicadores correspondientes al producto original de [Huella Humana](https://doi.org/10.1016/j.ecolind.2020.106630). 

* `src/create_hf_indicators.py`: crea una capa vectorial con la categoría, año y promedio de Huella Humana. La capa resultante es generada a partir de la intersección de los productos originales (raster) con una capa vectorial de geocercas determinada.

* `src/creatte_hf_persistence.py`: crea una capa con la categoría de persistencia de Huella Humana a través del tiempo. La capa resultante es generada a partir de la intersección de una categorización intermedia de persistencia a través de todos los productos originales (rasters) con una capa vectorial de geocercas determinada.

Adicionalmente, hay dos scripts auxiliares para la ejecución de la herramienta:

* `src/utils/constants.py`: contiene variables de parametrización. Cada variable tiene un comentario asociado dentro del código explicando su propósito. Modifique estas variables en caso de querer cambiar el comportamiento de la herramienta o algunos aspectos de los resultados.
* `src/utils/functions.py`: contiene funciones auxiliares. Se recomienda no alterar el código a menos de que quiera extender la funcionalidad de algún método en particular.


## Por dónde empezar
A continuación se presentan las instrucciones para la ejecución de las dos herramientas de manera local.

### Prerrequisitos
Para ejecutar las herramientas es necesario instalar solo uno de los siguientes programas:

* [Anaconda](https://www.anaconda.com/products/individual)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Recomendado)
* [Python](https://www.python.org/downloads/) (versión igual o superior a 3.6)

### Instalación
Clone este repositorio en su máquina utilizando `git`:

```
git clone https://github.com/PEM-Humboldt/huella-humana-indicadores.git
```

Si no tiene `git`, también puede descargar el proyecto haciendo click [acá](https://github.com/PEM-Humboldt/huella-humana-indicadores/archive/master.zip).

#### Anaconda o Miniconda
Una alternativa para crear un entorno virtual con un intérprete de Python y todos los paquetes necesarios es utilizar `conda`, un gestor de paquetes y entornos incluído en la instalación de Anaconda o Miniconda.

Para crear el entorno virtual con todos los paquetes, abra una terminal en la raíz del proyecto y ejecute el siguiente comando:

```
conda env create -f environment.yml
```

#### Python
Otra alternativa para crear un entorno virtual es utilizar `venv`, un módulo nativo de Python para gestionar entornos virtuales.

Para crear el entorno virtual, abra una terminal en la raíz del proyecto y ejecute el siguiente comando:

```
python3 -m venv hf-indicators
```

Para instalar los paquetes necesarios en el recién creado entorno virtual, active el entorno virtual ejecutando alguno de los siguientes comando dependiendo de su sistema operativo.

Para sistemas Unix (MacOS y Linux):
```
source hf-indicators/bin/activate
```

Para sistemas Windows:
```
hf-indicators\Scripts\activate.bat
```

Una vez activado el entorno virtual, ejecute el siguiente comando para instalar los paquetes necesarios:

```
python -m pip install -r requirements.txt
```


### Ejecución
Para ejecutar las herramientas debe activar el entorno virtual creado durante la instalación. Si utilizó `conda`, ejecute el siguiente comando desde una terminal (estando ubicado en la raíz del proyecto) para activar el entorno:

```
conda activate hf-indicators
```

Si utilizó `venv`, siga los pasos de activación expuestos durante el proceso de instalación.

 Ambas herramientas están expuestas a través de una interfaz de de línea de comandos (CLI), lo cual quiere decir que se ejecutan desde una terminal. Adicionalmente, ambas herramientas tienen una serie de parámetros posicionales requeridos y un parámetro opcional para su ejecución.
 
 Para obtener una lista de los párametros y su descripción, ejecute alguno de los siguientes comandos:
 
```
python src/create_hf_indicators.py -h
```

```
python src/create_hf_persistence.py -h
```

Dependiendo del comando que haya ejecutado, en la terminal debe aparecer un mensaje similar al siguiente:

```
usage: create_hf_indicators.py [-h] [-crs CRS]
                               output_path geofences_path
                               rasters_path

Creates a geographic vector layer with the category, year
and average of the human footprint by intersecting the
original product with a specific geofences geographic vector
layer.

positional arguments:
  output_path     Relative or absolute path (including the
                  extension) of the output file. If the
                  folder where the output file will be
                  created does not exist, the folder is
                  automatically created. Existing files will
                  be overwritten. Example
                  ./results/test/hf_indicators.shp
  geofences_path  Relative or absolute path of the input
                  geofences file. Example:
                  ./data/test/geofences.shp
  rasters_path    Relative or abolsute path of the folder
                  containing the raster(s) of the original
                  Human Footprint product. Rasters must be
                  GeoTIFF files and their filenames must
                  contain (anywhere on the name) a four-
                  digit sequence representing the year of
                  the product (e.g. IHEH_1970.tif). Example:
                  ./data/test/IHEH

optional arguments:
  -h, --help      show this help message and exit
  -crs CRS        String with the EPSG code of the new
                  coordinate reference system in the form
                  epsg:code. For example: epsg:4326
```

Los párametros posicionales y el parámetro opcional son iguales para ambas herramientas. Como es posible observar en el mensaje de ayuda, las herramientas requieren que se especifiquen la ruta del archivo de salida, la ruta del archivo de geocercas de entrada y la ruta de la carpeta con los rasters de huella humana. Estas rutas pueden ser absolutas o relativas. Adicionalmente, permite opcionalmente especificar el sistema de referencia de coordenadas del archivo de salida en caso de querer reproyectarlo.
 
 Suponga que tiene todos los datos de entrada para correr las herramientas dentro de la carpeta del proyecto, de esta manera:
 
 ```
.
├── data
│   ├── test
│       ├── geofences.cpg
│       ├── geofences.dbf
│       ├── geofences.prj
│       ├── geofences.shp
│       ├── geofences.shx
│       ├── IHEH
│           ├── IHEH_1970.tif
│           ├── IHEH_1990.tif
│           ├── IHEH_2000.tif
│           ├── IHEH_2015.tif
├── environment.yml
├── LICENSE.txt
├── README.md
├── requirements.txt
├── src
│   ├── create_hf_indicators.py
│   ├── utils
│       ├── constants.py
│       ├── functions.py
```

Puede ejecutar la herramienta `create_hf_indicators.py` con el siguiente comando y los siguientes parámetros:

```
python src/create_hf_indicators.py ./results/test/hf_indicators.shp ./data/test/geofences.shp ./data/test/IHEH -c epsg:4326
```

Puede ejecutar la herramienta `create_hf_persistence.py` de igual manera.

```
python src/create_hf_persistence.py ./results/test/hf_persistence.shp ./data/test/geofences.shp ./data/test/IHEH -c epsg:4326
```


## Authors
* **Jaime Burbano-Girón** - *Diseño del flujo de trabajo e implementación inicial* - jburbano@humboldt.org.co
* **Marcelo Villa-Piñeros** - *Implementación del flujo de trabajo en Python* - mvilla@humboldt.org.co


## License
Este proyecto está licenciado bajo una licencia MIT - ver el archivo [LICENSE.txt](LICENSE.txt) para detalles.
