#!/usr/bin/env python3
"""
Ejemplos prácticos de formatos de compresión: TAR, GZIP, ZIP
Aplicaciones en Ciencia de Datos y Big Data
"""

import tarfile
import gzip
import zipfile
import os
import shutil
from pathlib import Path
import time
import json


def crear_datos_ejemplo():
    """
    Crea archivos de ejemplo para comprimir
    """
    print("📁 Creando datos de ejemplo...")
    
    # Crear directorio temporal
    Path("datos_ejemplo").mkdir(exist_ok=True)
    
    # Crear varios archivos CSV
    for i in range(5):
        with open(f"datos_ejemplo/dataset_{i}.csv", 'w') as f:
            f.write("id,valor1,valor2,valor3\n")
            for j in range(10000):
                f.write(f"{j},{j*2},{j*3},{j*4}\n")
    
    # Crear archivos JSON
    for i in range(3):
        with open(f"datos_ejemplo/config_{i}.json", 'w') as f:
            json.dump({
                "experimento": f"EXP-{i:03d}",
                "parametros": {"lr": 0.001 * (i+1), "epochs": 100},
                "resultados": [{"epoch": e, "loss": 1.0/(e+1)} for e in range(50)]
            }, f, indent=2)
    
    # Crear un archivo de texto grande
    with open("datos_ejemplo/logs.txt", 'w') as f:
        for i in range(50000):
            f.write(f"[2025-11-19 10:{i%60:02d}:{i%60:02d}] INFO: Procesando registro {i}\n")
    
    print("✓ Datos de ejemplo creados")


def calcular_tamaño_directorio(path: str) -> int:
    """
    Calcula el tamaño total de un directorio
    
    Args:
        path: Ruta al directorio
        
    Returns:
        Tamaño en bytes
    """
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total


def formatear_tamaño(bytes: int) -> str:
    """
    Formatea bytes a formato legible
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"


def ejemplo_tar():
    """
    Demuestra uso de TAR (tape archive)
    """
    print(f"\n{'='*70}")
    print("TAR (TAPE ARCHIVE) - Empaquetado sin compresión")
    print('='*70)
    
    print("\n📦 TAR es un formato de EMPAQUETADO (no compresión):")
    print("   • Combina múltiples archivos en uno solo")
    print("   • Preserva estructura de directorios")
    print("   • Preserva permisos y metadatos")
    print("   • NO reduce el tamaño (sin compresión)")
    
    # Crear archivo TAR
    print("\n1️⃣  Creando archivo TAR...")
    inicio = time.time()
    
    with tarfile.open('datos.tar', 'w') as tar:
        tar.add('datos_ejemplo', arcname='datos')
    
    tiempo_tar = time.time() - inicio
    
    tamaño_original = calcular_tamaño_directorio('datos_ejemplo')
    tamaño_tar = os.path.getsize('datos.tar')
    
    print(f"✓ Archivo TAR creado: datos.tar")
    print(f"  Tamaño original: {formatear_tamaño(tamaño_original)}")
    print(f"  Tamaño TAR:      {formatear_tamaño(tamaño_tar)}")
    print(f"  Ratio:           {tamaño_tar/tamaño_original:.2%}")
    print(f"  Tiempo:          {tiempo_tar:.3f} segundos")
    
    # Listar contenido
    print("\n📋 Contenido del archivo TAR:")
    with tarfile.open('datos.tar', 'r') as tar:
        for i, member in enumerate(tar.getmembers()[:5]):
            print(f"   • {member.name:40s} {formatear_tamaño(member.size):>10s}")
        if len(tar.getmembers()) > 5:
            print(f"   ... y {len(tar.getmembers()) - 5} archivos más")
    
    # Extraer
    print("\n📤 Extrayendo archivo TAR...")
    Path("extracted_tar").mkdir(exist_ok=True)
    with tarfile.open('datos.tar', 'r') as tar:
        tar.extractall('extracted_tar')
    print("✓ Extracción completada en: extracted_tar/")


def ejemplo_gzip():
    """
    Demuestra uso de GZIP
    """
    print(f"\n{'='*70}")
    print("GZIP - Compresión de archivos individuales")
    print('='*70)
    
    print("\n🗜️  GZIP características:")
    print("   • Comprime UN archivo a la vez")
    print("   • Algoritmo DEFLATE (LZ77 + Huffman)")
    print("   • Muy común en Linux/Unix")
    print("   • Extensión: .gz")
    print("   • Streaming-friendly (no necesita archivo completo)")
    
    # Comprimir archivo individual
    print("\n1️⃣  Comprimiendo archivo individual con GZIP...")
    archivo = 'datos_ejemplo/logs.txt'
    inicio = time.time()
    
    with open(archivo, 'rb') as f_in:
        with gzip.open(f'{archivo}.gz', 'wb', compresslevel=9) as f_out:
            f_out.writelines(f_in)
    
    tiempo_gzip = time.time() - inicio
    
    tamaño_original = os.path.getsize(archivo)
    tamaño_gz = os.path.getsize(f'{archivo}.gz')
    
    print(f"✓ Archivo comprimido: {archivo}.gz")
    print(f"  Tamaño original: {formatear_tamaño(tamaño_original)}")
    print(f"  Tamaño GZIP:     {formatear_tamaño(tamaño_gz)}")
    print(f"  Compresión:      {(1 - tamaño_gz/tamaño_original)*100:.1f}%")
    print(f"  Tiempo:          {tiempo_gzip:.3f} segundos")
    
    # TAR + GZIP (tar.gz / tgz)
    print("\n2️⃣  Combinando TAR + GZIP (formato .tar.gz)...")
    inicio = time.time()
    
    with tarfile.open('datos.tar.gz', 'w:gz') as tar:
        tar.add('datos_ejemplo', arcname='datos')
    
    tiempo_targz = time.time() - inicio
    
    tamaño_original = calcular_tamaño_directorio('datos_ejemplo')
    tamaño_targz = os.path.getsize('datos.tar.gz')
    
    print(f"✓ Archivo TAR.GZ creado: datos.tar.gz")
    print(f"  Tamaño original: {formatear_tamaño(tamaño_original)}")
    print(f"  Tamaño TAR.GZ:   {formatear_tamaño(tamaño_targz)}")
    print(f"  Compresión:      {(1 - tamaño_targz/tamaño_original)*100:.1f}%")
    print(f"  Tiempo:          {tiempo_targz:.3f} segundos")
    
    print("\n💡 TAR.GZ es el estándar en Linux para distribuir código fuente")


def ejemplo_zip():
    """
    Demuestra uso de ZIP
    """
    print(f"\n{'='*70}")
    print("ZIP - Compresión y empaquetado combinados")
    print('='*70)
    
    print("\n📦 ZIP características:")
    print("   • Empaqueta Y comprime múltiples archivos")
    print("   • Cada archivo se comprime independientemente")
    print("   • Acceso aleatorio (no necesita descomprimir todo)")
    print("   • Estándar en Windows")
    print("   • Soporta encriptación")
    
    # Crear archivo ZIP
    print("\n1️⃣  Creando archivo ZIP...")
    inicio = time.time()
    
    with zipfile.ZipFile('datos.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('datos_ejemplo'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'datos_ejemplo')
                zipf.write(file_path, arcname)
    
    tiempo_zip = time.time() - inicio
    
    tamaño_original = calcular_tamaño_directorio('datos_ejemplo')
    tamaño_zip = os.path.getsize('datos.zip')
    
    print(f"✓ Archivo ZIP creado: datos.zip")
    print(f"  Tamaño original: {formatear_tamaño(tamaño_original)}")
    print(f"  Tamaño ZIP:      {formatear_tamaño(tamaño_zip)}")
    print(f"  Compresión:      {(1 - tamaño_zip/tamaño_original)*100:.1f}%")
    print(f"  Tiempo:          {tiempo_zip:.3f} segundos")
    
    # Listar contenido
    print("\n📋 Contenido del archivo ZIP:")
    with zipfile.ZipFile('datos.zip', 'r') as zipf:
        info_list = zipf.infolist()
        for i, info in enumerate(info_list[:5]):
            ratio = (1 - info.compress_size / info.file_size) * 100 if info.file_size > 0 else 0
            print(f"   • {info.filename:30s} {formatear_tamaño(info.file_size):>10s} "
                  f"→ {formatear_tamaño(info.compress_size):>10s} ({ratio:.1f}%)")
        if len(info_list) > 5:
            print(f"   ... y {len(info_list) - 5} archivos más")
    
    # Extraer archivo específico
    print("\n📤 Extrayendo archivo específico (sin descomprimir todo)...")
    with zipfile.ZipFile('datos.zip', 'r') as zipf:
        zipf.extract('dataset_0.csv', 'extracted_zip')
    print("✓ Extraído: extracted_zip/dataset_0.csv")


def comparacion_formatos():
    """
    Tabla comparativa de formatos de compresión
    """
    print(f"\n{'='*70}")
    print("COMPARACIÓN DE FORMATOS DE COMPRESIÓN")
    print('='*70)
    
    # Obtener tamaños
    tamaño_original = calcular_tamaño_directorio('datos_ejemplo')
    tamaño_tar = os.path.getsize('datos.tar') if os.path.exists('datos.tar') else 0
    tamaño_targz = os.path.getsize('datos.tar.gz') if os.path.exists('datos.tar.gz') else 0
    tamaño_zip = os.path.getsize('datos.zip') if os.path.exists('datos.zip') else 0
    
    print(f"""
┌─────────────┬──────────────┬─────────────┬───────────────┬─────────────┐
│  Formato    │    Tamaño    │ Compresión  │  Velocidad    │   Uso       │
├─────────────┼──────────────┼─────────────┼───────────────┼─────────────┤
│ Original    │ {formatear_tamaño(tamaño_original):>12s} │      -      │       -       │      -      │
├─────────────┼──────────────┼─────────────┼───────────────┼─────────────┤
│ TAR         │ {formatear_tamaño(tamaño_tar):>12s} │     0%      │   Muy rápida  │ Empaquetar  │
├─────────────┼──────────────┼─────────────┼───────────────┼─────────────┤
│ TAR.GZ      │ {formatear_tamaño(tamaño_targz):>12s} │ {(1-tamaño_targz/tamaño_original)*100:>6.1f}%    │     Media     │ Linux std   │
├─────────────┼──────────────┼─────────────┼───────────────┼─────────────┤
│ ZIP         │ {formatear_tamaño(tamaño_zip):>12s} │ {(1-tamaño_zip/tamaño_original)*100:>6.1f}%    │     Rápida    │ Windows std │
└─────────────┴──────────────┴─────────────┴───────────────┴─────────────┘

🎯 CUÁNDO USAR CADA FORMATO:

TAR (.tar):
  ✓ Empaquetar sin comprimir (luego comprimir con GZIP/BZIP2/XZ)
  ✓ Preservar permisos Unix (backups)
  ✓ Streaming de archivos
  ✗ No reduce espacio

TAR.GZ (.tar.gz, .tgz):
  ✓ Distribución de código fuente
  ✓ Backups en Linux/Unix
  ✓ Datasets para ML (Kaggle, etc.)
  ✓ Mejor compresión que ZIP
  ✗ Debe descomprimir todo (no acceso aleatorio)

GZIP (.gz):
  ✓ Comprimir archivos individuales grandes
  ✓ Logs de servidor
  ✓ Streaming (compresión HTTP)
  ✓ Pipelines de datos en tiempo real
  ✗ Solo un archivo a la vez

ZIP (.zip):
  ✓ Compatibilidad universal (Windows, Mac, Linux)
  ✓ Acceso aleatorio a archivos internos
  ✓ Distribución de software
  ✓ Datasets con estructura de carpetas
  ✗ Compresión ligeramente peor que GZIP

OTROS FORMATOS MODERNOS:

7-Zip (.7z):
  • Mejor compresión que ZIP/GZIP
  • Más lento
  • Menos compatible

BZIP2 (.bz2):
  • Mejor compresión que GZIP
  • Más lento
  • Común en Linux

XZ (.xz):
  • Excelente compresión
  • Muy lento
  • Usado en distribuciones Linux modernas

ZSTD (.zst):
  • Balance compresión/velocidad
  • Moderno (Facebook)
  • Usado en PyTorch, databases
""")


def casos_uso_ciencia_datos():
    """
    Casos de uso específicos en ciencia de datos
    """
    print(f"\n{'='*70}")
    print("CASOS DE USO EN CIENCIA DE DATOS")
    print('='*70)
    
    print("""
📊 DATASETS PÚBLICOS:

1. KAGGLE:
   • Formato: ZIP
   • Razón: Acceso aleatorio, compatibilidad universal
   • Ejemplo: competitions descargadas como .zip

2. HUGGING FACE:
   • Formato: TAR.GZ
   • Razón: Mejor compresión para datasets grandes
   • Ejemplo: language models, embeddings

3. UCI ML REPOSITORY:
   • Formato: ZIP o TAR.GZ
   • Razón: Mantener estructura de carpetas con README

🔬 INVESTIGACIÓN:

4. COMPARTIR EXPERIMENTOS:
   • Formato: TAR.GZ + MD5 checksum
   • Contenido: código + datos + modelos + resultados
   • Ejemplo:
     experimento_001.tar.gz (contiene):
       ├── src/           # Código
       ├── data/          # Datos procesados
       ├── models/        # Modelos entrenados
       ├── results/       # Métricas y plots
       └── README.md      # Documentación

5. REPRODUCIBILIDAD:
   • Incluir: requirements.txt, environment.yml
   • Formato: ZIP (Windows) o TAR.GZ (Linux)

💾 BIG DATA:

6. LOGS DE SERVIDORES:
   • Formato: GZIP (individual) o TAR.GZ (múltiples)
   • Razón: Streaming, compresión line-by-line
   • Ejemplo: logs-2025-11-19.log.gz

7. DATA LAKES:
   • Formato: GZIP + Parquet
   • Razón: Columnar + compresión
   • Ejemplo: s3://bucket/data/year=2025/month=11/data.parquet.gz

8. BACKUPS:
   • Formato: TAR.GZ incremental
   • Herramientas: rsync + tar
   • Ejemplo: backup-YYYY-MM-DD.tar.gz

🐍 PYTHON ESPECÍFICO:

9. PACKAGES:
   • Formato: .whl (ZIP renombrado)
   • .tar.gz (source distribution)

10. PICKLE + GZIP:
    • Modelos ML serializados comprimidos
    • Ejemplo: model.pkl.gz
    
    import pickle
    import gzip
    
    # Guardar
    with gzip.open('model.pkl.gz', 'wb') as f:
        pickle.dump(model, f)
    
    # Cargar
    with gzip.open('model.pkl.gz', 'rb') as f:
        model = pickle.load(f)

🎓 MEJORES PRÁCTICAS:

✓ HACER:
  • Comprimir datos antes de subir a cloud (reduce costos)
  • Usar TAR.GZ para distribuir proyectos completos
  • Incluir checksums (MD5/SHA256) para verificar integridad
  • Documentar formato y estructura en README

✗ NO HACER:
  • Comprimir archivos ya comprimidos (JPG, PNG, MP4)
  • Usar compresión máxima si necesitas velocidad
  • Olvidar que ZIP no preserva permisos Unix
  • Comprimir databases en uso (usar dumps)
""")


def limpiar():
    """
    Limpia archivos temporales
    """
    print(f"\n{'='*70}")
    print("LIMPIEZA")
    print('='*70)
    
    # Eliminar directorios
    for dir_path in ['datos_ejemplo', 'extracted_tar', 'extracted_zip']:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"✓ Eliminado: {dir_path}/")
    
    # Eliminar archivos comprimidos
    for archivo in ['datos.tar', 'datos.tar.gz', 'datos.zip', 
                    'datos_ejemplo/logs.txt.gz']:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"✓ Eliminado: {archivo}")


if __name__ == "__main__":
    print("="*70)
    print("EJEMPLOS PRÁCTICOS: FORMATOS DE COMPRESIÓN")
    print("TAR, GZIP, ZIP")
    print("="*70)
    
    try:
        # Crear datos de ejemplo
        crear_datos_ejemplo()
        
        # Demostrar cada formato
        ejemplo_tar()
        ejemplo_gzip()
        ejemplo_zip()
        
        # Comparación
        comparacion_formatos()
        
        # Casos de uso
        casos_uso_ciencia_datos()
        
        # Limpiar
        respuesta = input("\n¿Deseas limpiar los archivos temporales? (s/n): ")
        if respuesta.lower() == 's':
            limpiar()
        
        print("\n" + "="*70)
        print("✓ Demostración completada")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
