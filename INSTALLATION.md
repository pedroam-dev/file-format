# Guía de Instalación

## Estado de instalación

Todas las dependencias han sido instaladas exitosamente.

## Bibliotecas instaladas

### Core de Ciencia de Datos
- **pandas** (2.0.0+) - Análisis y manipulación de datos tabulares
- **numpy** (1.24.0+) - Computación numérica y arrays

### Visualización
- **matplotlib** (3.7.0+) - Gráficos y visualizaciones
- **seaborn** (0.12.0+) - Visualizaciones estadísticas

### Procesamiento de Archivos
- **Pillow** (10.0.0+) - Procesamiento de imágenes (JPEG, PNG, etc.)
- **jsonschema** (4.17.0+) - Validación de esquemas JSON
- **chardet** (5.1.0+) - Detección automática de encoding en archivos

### Formatos Avanzados
- **pyarrow** (12.0.0+) - Soporte para Apache Parquet
- **fastparquet** (2023.0.0+) - Alternativa para leer/escribir Parquet
- **h5py** (3.8.0+) - Soporte para archivos HDF5

### Jupyter Notebook
- **jupyter** (1.0.0+) - Metapaquete de Jupyter
- **notebook** (6.5.0+) - Interfaz clásica de Jupyter Notebook
- **ipykernel** (6.22.0+) - Kernel de Python para Jupyter

### Utilidades
- **python-dateutil** (2.8.0+) - Utilidades para fechas

## Verificación de Instalación

Para verificar que todo está instalado correctamente, ejecuta:

```bash
python -c "import pandas, numpy, matplotlib, seaborn, PIL, jsonschema, chardet; print('✓ Bibliotecas principales OK')"
```

Para verificar formatos avanzados:

```bash
python -c "import pyarrow, fastparquet, h5py; print('✓ Formatos avanzados OK')"
```

Para verificar Jupyter:

```bash
python -c "import jupyter, notebook, ipykernel; print('✓ Jupyter OK')"
```

## Requisitos del Sistema

- **Python**: 3.8 o superior (recomendado 3.11+)
- **Sistema Operativo**: Windows, macOS, o Linux
- **Espacio en disco**: ~500 MB para todas las dependencias
- **RAM**: Mínimo 4 GB (recomendado 8 GB para datasets grandes)

## Comandos Útiles

### Listar todas las bibliotecas instaladas
```bash
pip list
```

### Verificar versión de una biblioteca específica
```bash
pip show pandas
```

### Actualizar una biblioteca
```bash
pip install --upgrade pandas
```

### Reinstalar todas las dependencias
```bash
pip install -r requirements.txt --force-reinstall
```

### Crear un entorno virtual (recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Dependencias Opcionales

Si necesitas funcionalidades adicionales:

### Procesamiento de video
```bash
pip install opencv-python
```

### Lectura de archivos Excel
```bash
pip install openpyxl xlrd
```

### Procesamiento XML avanzado
```bash
pip install lxml
```

### Archivos YAML
```bash
pip install pyyaml
```

### Big Data
```bash
pip install dask vaex
```

## Solución de Problemas Comunes

### Error: "No module named 'XXX'"
```bash
pip install XXX
```

### Error de permisos en macOS/Linux
```bash
pip install --user -r requirements.txt
```

### Problemas con conflictos de versiones
```bash
pip install -r requirements.txt --upgrade
```

### Limpiar caché de pip
```bash
pip cache purge
pip install -r requirements.txt
```

## Información de Versiones Instaladas

Última actualización: 19 de noviembre de 2025

Todas las bibliotecas han sido instaladas con las versiones especificadas en `requirements.txt`.

## Soporte

Para problemas de instalación:
1. Verificar versión de Python: `python --version`
2. Actualizar pip: `pip install --upgrade pip`
3. Revisar logs de error
4. Consultar con el instructor del curso

---

**¡Instalación completada exitosamente!**

Ahora puedes ejecutar el notebook o los scripts de ejemplo.
