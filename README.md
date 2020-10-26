# huella-humana-indicadores

Este repositorio contiene dos herramientas diferentes para crear las capas geográficas vectoriales con los indicadores correspondientes al producto original de [Huella Humana](https://doi.org/10.1016/j.ecolind.2020.106630). 

* `src/create_hf_indicators.py`: crea una capa vectorial con la categoría, año y promedio de Huella Humana a partir de la intersección del producto original con una capa vectorial de geocercas determinada.

* `src/create_hf_persistence.py`: crea una capa vectorial con la categoría de persistencia de Huella Humana a través del tiempo a partir de la intersección del producto original con una capa vectorial de geocercas determinada.

Adicionalmente, hay dos scripts auxiliares para la ejecución de las herramientas:

* `src/utils/constants.py`: contiene variables de parametrización. Cada variable tiene un comentario asociado dentro del código explicando su propósito.
* `src/utils/functions.py`: contiene funciones auxiliares. Se recomienda no alterar el código a menos de que quiera extender la funcionalidad de algún método en particular.




## Por dónde empezar

A continuación se presentan las instrucciones para la ejecución de las dos herramientas de manera local.


### Prerrequisitos

Para ejecutar las herramientas es necesario instalar solo uno de los siguientes programas:

* [Anaconda](https://www.anaconda.com/products/individual)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Recomendado)
* [Python](https://www.python.org/downloads/) (versión igual o superior a 3.6)


### Instalación

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

