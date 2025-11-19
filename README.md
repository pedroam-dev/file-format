# Formatos de Archivos y Representación del Conocimiento en Ciencia de Datos

Material educativo completo para clase de maestría en Ciencia de Datos e Inteligencia Artificial.

## Estado del proyecto

**Proyecto completo y listo para usar**

- Todas las dependencias instaladas (`requirements.txt`)
- Notebook interactivo con 8 secciones completas
- 15+ archivos de ejemplo en diferentes formatos
- 5 scripts Python ejecutables independientes
- Documentación completa en README

## Contenido

Este repositorio contiene ejemplos prácticos y explicaciones detalladas sobre:

1. **XML (eXtensible Markup Language)**
2. **CSV (Comma-Separated Values)**
3. **JSON (JavaScript Object Notation)**
4. **Formatos de Compresión** (TAR, GZIP, ZIP)
5. **Formatos Contenedores** (Video e Imagen)

## Estructura del Proyecto

```
file-format/
├── README.md                                   # Este archivo
├── INSTALLATION.md                             # Guía detallada de instalación
├── requirements.txt                            # Dependencias de Python
├── Formatos_Archivos_Ciencia_Datos.ipynb      # Notebook principal interactivo
│
├── ejemplos/
│   ├── 01_xml/
│   │   ├── dataset_investigacion.xml           # Dataset de experimentos ML
│   │   ├── ontologia_medica.xml                # Ontología de conocimiento médico
│   │   └── procesar_xml.py                     # Script de procesamiento
│   │
│   ├── 02_csv/
│   │   ├── empleados_simple.csv                # CSV básico
│   │   ├── sensores_iot.csv                    # CSV con delimitador ;
│   │   ├── transacciones_pipe.csv              # CSV con delimitador |
│   │   ├── pacientes_comillas.csv              # CSV con comillas escapadas
│   │   ├── experimentos_tabs.csv               # CSV con tabulaciones
│   │   └── procesar_csv.py                     # Script de procesamiento
│   │
│   ├── 03_json/
│   │   ├── investigacion_nlp.json              # Proyecto de investigación completo
│   │   ├── grafo_conocimiento.json             # Grafo de colaboración científica
│   │   ├── sensores_streaming.jsonl            # JSON Lines para streaming
│   │   ├── schema_experimento.json             # JSON Schema para validación
│   │   └── procesar_json.py                    # Script de procesamiento
│   │
│   ├── 04_compresion/
│   │   └── ejemplo_compresion.py               # Ejemplos TAR, GZIP, ZIP
│   │
│   └── 05_contenedores/
│       └── ejemplo_contenedores.py             # Ejemplos de imagen y video
```

## Inicio rápido

### Requisitos previos

- **Python 3.8 o superior** (recomendado: Python 3.11+)
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

### Instalación

#### 1. Clonar el repositorio

```bash
git clone https://github.com/pedroam-dev/file-format.git
cd file-format
```

#### 2. Instalar dependencias

```bash
# Instalar todas las bibliotecas necesarias desde requirements.txt
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:

**Bibliotecas principales:**
- `pandas` - Manipulación y análisis de datos tabulares
- `numpy` - Computación numérica y arrays
- `matplotlib` y `seaborn` - Visualización de datos
- `Pillow` - Procesamiento de imágenes
- `jsonschema` - Validación de esquemas JSON
- `chardet` - Detección automática de encoding en CSV

**Formatos avanzados (opcionales pero recomendados):**
- `pyarrow` y `fastparquet` - Soporte para formato Parquet
- `h5py` - Soporte para formato HDF5

**Jupyter Notebook:**
- `jupyter`, `notebook`, `ipykernel` - Entorno interactivo

#### 3. Verificar la instalación

```bash
python -c "import pandas, numpy, matplotlib, seaborn, PIL, jsonschema; print('✓ Todas las bibliotecas instaladas correctamente')"
```

Para más detalles sobre las dependencias instaladas y solución de problemas, consulta **[INSTALLATION.md](INSTALLATION.md)**.

### Uso del Notebook

El notebook principal `Formatos_Archivos_Ciencia_Datos.ipynb` contiene:

- Ejemplos interactivos ejecutables
- Visualizaciones comparativas
- Análisis de ventajas/desventajas
- Casos de uso en ciencia de datos
- Ejercicios prácticos

#### Abrir con Jupyter Notebook:

```bash
# Iniciar Jupyter Notebook
jupyter notebook Formatos_Archivos_Ciencia_Datos.ipynb
```

#### Abrir con VS Code (recomendado):

```bash
# Abrir con Visual Studio Code
code Formatos_Archivos_Ciencia_Datos.ipynb
```

O simplemente abre VS Code, navega al archivo y haz clic en él.

#### Abrir con JupyterLab:

```bash
# Iniciar JupyterLab 
jupyter lab
```

### Scripts independientes

Cada carpeta en `ejemplos/` contiene scripts ejecutables independientes:

```bash
# Ejemplos XML
cd ejemplos/01_xml
python procesar_xml.py

# Ejemplos CSV
cd ejemplos/02_csv
python procesar_csv.py

# Ejemplos JSON
cd ejemplos/03_json
python procesar_json.py

# Ejemplos compresión
cd ejemplos/04_compresion
python ejemplo_compresion.py

# Ejemplos contenedores (imagen/video)
cd ejemplos/05_contenedores
python ejemplo_contenedores.py
```

**Nota:** Asegúrate de volver al directorio raíz antes de ejecutar otro script:
```bash
cd /Users/tu-usuario/file-format
```

## Conceptos clave

### XML - Datos Jerárquicos

**Ventajas:**
- Estructura jerárquica y auto-descriptiva
- Validación con schemas (XSD)
- Namespaces para evitar conflictos
- XPath/XSLT para consultas

**Casos de uso:**
- Configuración de sistemas complejos
- Ontologías y grafos de conocimiento
- Intercambio entre sistemas enterprise

### CSV - Datos Tabulares

**Ventajas:**
- Universal y simple
- Legible por humanos
- Compatible con Excel, R, Python, SQL

**Casos de uso:**
- Datasets de Machine Learning
- Exports de bases de datos
- Reportes y análisis

### JSON - Flexibilidad

**Ventajas:**
- Soporta anidación
- Tipos de datos nativos
- Ampliamente usado en APIs
- Más compacto que XML

**Casos de uso:**
- APIs REST
- Configuración de modelos ML
- NoSQL databases
- JSON Lines para streaming

### Compresión

| Formato | Compresión | Velocidad | Uso |
|---------|-----------|-----------|-----|
| TAR | ✗ | Muy rápida | Empaquetar |
| GZIP | ✓ | Media | Linux/Unix std |
| ZIP | ✓ | Rápida | Windows std |

### Formatos contenedores

**Imagen:**
- JPEG: Fotografías (con pérdida)
- PNG: Gráficos, transparencia (sin pérdida)
- TIFF: Medicina, GIS (sin pérdida)

**Video:**
- Contenedor: MP4, MKV, AVI, MOV
- Codec: H.264, H.265, VP9, AV1

## Comparación Rápida

```
                 Legibilidad  Tamaño  Velocidad  Anidación  Tipos
XML                 Media    Grande    Lenta       ✓        ✗
CSV                 Alta     Medio     Media       ✗        ✗
JSON                Alta     Medio     Media       ✓        Básicos
Parquet             Baja     Pequeño   Rápida      Limitada ✓
HDF5                Baja     Pequeño   Rápida      ✓        ✓
```

## Recomendaciones por Escenario

| Escenario | Formato Recomendado |
|-----------|-------------------|
| Dataset tabular < 100MB | CSV |
| Dataset tabular > 1GB | Parquet |
| API REST | JSON |
| Configuración modelo | JSON/YAML |
| Imágenes training | JPEG Q=90 + JSON metadatos |
| Arrays científicos | HDF5 |
| Compartir proyecto | TAR.GZ |
| Ontología/Grafo | XML o JSON-LD |
| Streaming eventos | JSON Lines |
| Modelo entrenado | Pickle + GZIP |


### Datasets para practicar
- [Kaggle](https://www.kaggle.com/datasets) - Datasets de ML/DS
- [UCI ML Repository](https://archive.ics.uci.edu/ml/) - Repositorio clásico
- [Hugging Face](https://huggingface.co/datasets) - Datasets modernos

### Bibliotecas Python adicionales

Instalación de bibliotecas adicionales según necesidad:

```bash
# Procesamiento de video
pip install opencv-python

# Formatos adicionales
pip install openpyxl xlrd  # Excel
pip install lxml  # XML avanzado
pip install yaml  # Configuración

# Big Data
pip install dask  # Procesamiento paralelo
pip install vaex  # Grandes datasets
```

### Recursos de aprendizaje
- [Documentación pandas](https://pandas.pydata.org/docs/user_guide/io.html) - Guía de I/O
- [Python JSON Tutorial](https://realpython.com/python-json/)
- [Working with CSV files](https://realpython.com/python-csv/)
- [XML Processing in Python](https://docs.python.org/3/library/xml.etree.elementtree.html)
