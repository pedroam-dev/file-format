#!/usr/bin/env python3
"""
Script completo de procesamiento de archivos CSV para Ciencia de Datos
Demuestra diferentes técnicas, problemas comunes y soluciones
"""

import pandas as pd
import numpy as np
import csv
from typing import List, Dict, Tuple
import chardet
import io


def detectar_delimitador(archivo: str) -> str:
    """
    Detecta automáticamente el delimitador usado en un CSV
    
    Args:
        archivo: Ruta al archivo CSV
        
    Returns:
        Delimitador detectado
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        primera_linea = f.readline()
        sniffer = csv.Sniffer()
        delimitador = sniffer.sniff(primera_linea).delimiter
    
    return delimitador


def detectar_encoding(archivo: str) -> str:
    """
    Detecta el encoding de un archivo
    
    Args:
        archivo: Ruta al archivo
        
    Returns:
        Encoding detectado
    """
    with open(archivo, 'rb') as f:
        resultado = chardet.detect(f.read())
    
    return resultado['encoding']


def analizar_csv_estructura(archivo: str):
    """
    Analiza la estructura de un archivo CSV
    
    Args:
        archivo: Ruta al archivo CSV
    """
    print(f"\n{'='*70}")
    print(f"ANÁLISIS: {archivo}")
    print('='*70)
    
    # Detectar encoding y delimitador
    encoding = detectar_encoding(archivo)
    delimitador = detectar_delimitador(archivo)
    
    print(f"📄 Encoding detectado: {encoding}")
    print(f"🔸 Delimitador detectado: '{delimitador}' (ASCII: {ord(delimitador)})")
    
    # Cargar datos
    df = pd.read_csv(archivo, encoding=encoding, sep=delimitador)
    
    print(f"\n📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"📋 Columnas: {list(df.columns)}")
    print(f"💾 Memoria: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Tipos de datos
    print(f"\n🔢 Tipos de datos:")
    for col, dtype in df.dtypes.items():
        print(f"   • {col}: {dtype}")
    
    # Valores nulos
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
        print(f"\n⚠️  Valores nulos detectados:")
        for col, count in nulos[nulos > 0].items():
            print(f"   • {col}: {count} ({count/len(df)*100:.1f}%)")
    else:
        print(f"\n✓ No hay valores nulos")
    
    # Muestra de datos
    print(f"\n📝 Primeras 3 filas:")
    print(df.head(3).to_string(index=False))
    
    return df


def problemas_comunes_csv():
    """
    Demuestra problemas comunes al trabajar con CSV y sus soluciones
    """
    print(f"\n{'='*70}")
    print("PROBLEMAS COMUNES CON CSV Y SOLUCIONES")
    print('='*70)
    
    # Problema 1: Comillas en texto
    print("\n🔴 PROBLEMA 1: Texto con comillas internas")
    print("-" * 70)
    
    df_pacientes = pd.read_csv('pacientes_comillas.csv')
    print("Ejemplo de campo con comillas escapadas:")
    print(df_pacientes[['id_paciente', 'notas_medicas']].head(3).to_string(index=False))
    
    print("\n✅ SOLUCIÓN: pandas maneja automáticamente comillas según RFC 4180")
    print("   - Comillas dobles dentro del campo se escapan: \"\"")
    print("   - El campo completo se encierra entre comillas")
    
    # Problema 2: Diferentes delimitadores
    print("\n🔴 PROBLEMA 2: Múltiples delimitadores en diferentes archivos")
    print("-" * 70)
    
    archivos = [
        ('empleados_simple.csv', ','),
        ('sensores_iot.csv', ';'),
        ('transacciones_pipe.csv', '|'),
        ('experimentos_tabs.csv', '\t')
    ]
    
    for archivo, delim_esperado in archivos:
        delim_detectado = detectar_delimitador(archivo)
        print(f"   • {archivo:30s} -> '{delim_detectado}'")
    
    print("\n✅ SOLUCIÓN: Usar csv.Sniffer() o especificar sep= explícitamente")
    
    # Problema 3: Tipos de datos incorrectos
    print("\n🔴 PROBLEMA 3: Inferencia incorrecta de tipos de datos")
    print("-" * 70)
    
    # Leer sin especificar tipos
    df = pd.read_csv('empleados_simple.csv')
    print("Tipos inferidos automáticamente:")
    print(df.dtypes)
    
    # Leer especificando tipos
    print("\n✅ SOLUCIÓN: Especificar dtype= explícitamente")
    df_tipado = pd.read_csv(
        'empleados_simple.csv',
        dtype={
            'nombre': str,
            'edad': np.int8,  # int8 suficiente para edades
            'ciudad': 'category',  # category para valores repetidos
            'departamento': 'category'
        },
        parse_dates=['fecha_ingreso']
    )
    print("Tipos especificados:")
    print(df_tipado.dtypes)
    print(f"\nReducción de memoria: {df.memory_usage(deep=True).sum() / 1024:.2f} KB "
          f"-> {df_tipado.memory_usage(deep=True).sum() / 1024:.2f} KB")


def csv_para_ml_pipeline():
    """
    Ejemplo de pipeline completo: CSV -> Limpieza -> Feature Engineering -> ML Ready
    """
    print(f"\n{'='*70}")
    print("PIPELINE: CSV -> MACHINE LEARNING")
    print('='*70)
    
    # 1. Cargar datos
    print("\n📥 PASO 1: Carga de datos")
    print("-" * 70)
    df = pd.read_csv(
        'empleados_simple.csv',
        dtype={
            'ciudad': 'category',
            'departamento': 'category'
        },
        parse_dates=['fecha_ingreso']
    )
    print(f"✓ Cargados {len(df)} registros")
    
    # 2. Exploración inicial
    print("\n🔍 PASO 2: Exploración inicial")
    print("-" * 70)
    print(df.describe())
    
    # 3. Feature Engineering
    print("\n⚙️  PASO 3: Feature Engineering")
    print("-" * 70)
    
    # Calcular antigüedad en días
    df['antiguedad_dias'] = (pd.Timestamp.now() - df['fecha_ingreso']).dt.days
    print(f"✓ Calculada 'antiguedad_dias'")
    
    # Crear bins de edad
    df['rango_edad'] = pd.cut(
        df['edad'],
        bins=[0, 30, 40, 100],
        labels=['Joven', 'Medio', 'Senior']
    )
    print(f"✓ Creada 'rango_edad' (categorical)")
    
    # Salario por departamento (mean encoding)
    df['salario_medio_dept'] = df.groupby('departamento')['salario'].transform('mean')
    print(f"✓ Calculado 'salario_medio_dept'")
    
    # 4. Encoding de variables categóricas
    print("\n🔢 PASO 4: Encoding de variables categóricas")
    print("-" * 70)
    
    # One-hot encoding
    df_encoded = pd.get_dummies(
        df,
        columns=['ciudad', 'departamento', 'rango_edad'],
        prefix=['ciudad', 'dept', 'edad']
    )
    print(f"✓ One-hot encoding aplicado")
    print(f"  Dimensiones finales: {df_encoded.shape[0]} filas × {df_encoded.shape[1]} columnas")
    
    # 5. Preparar para ML
    print("\n🤖 PASO 5: Dataset listo para ML")
    print("-" * 70)
    
    # Seleccionar solo columnas numéricas
    features = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
    features.remove('salario')  # Variable target
    
    X = df_encoded[features]
    y = df_encoded['salario']
    
    print(f"✓ Features (X): {len(features)} variables")
    print(f"  {features}")
    print(f"✓ Target (y): salario")
    print(f"\nDimensiones finales:")
    print(f"  X: {X.shape}")
    print(f"  y: {y.shape}")
    
    return X, y


def csv_a_otros_formatos(archivo_csv: str):
    """
    Convierte CSV a otros formatos comunes en ciencia de datos
    """
    print(f"\n{'='*70}")
    print("CONVERSIÓN: CSV -> OTROS FORMATOS")
    print('='*70)
    
    df = pd.read_csv(archivo_csv)
    nombre_base = archivo_csv.replace('.csv', '')
    
    # JSON
    json_file = f"{nombre_base}.json"
    df.to_json(json_file, orient='records', indent=2, force_ascii=False)
    print(f"✓ JSON: {json_file}")
    
    # Parquet (columnar, comprimido)
    parquet_file = f"{nombre_base}.parquet"
    df.to_parquet(parquet_file, engine='pyarrow', compression='snappy')
    print(f"✓ Parquet: {parquet_file}")
    
    # Excel
    excel_file = f"{nombre_base}.xlsx"
    df.to_excel(excel_file, index=False, sheet_name='Datos')
    print(f"✓ Excel: {excel_file}")
    
    # Pickle (formato nativo pandas, preserva tipos)
    pickle_file = f"{nombre_base}.pkl"
    df.to_pickle(pickle_file)
    print(f"✓ Pickle: {pickle_file}")
    
    # Comparar tamaños
    import os
    print(f"\n📦 Comparación de tamaños:")
    for archivo in [archivo_csv, json_file, parquet_file, excel_file, pickle_file]:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"   • {archivo:40s}: {size:6d} bytes")


def comparacion_csv_vs_otros():
    """
    Tabla comparativa de CSV vs otros formatos
    """
    print(f"\n{'='*70}")
    print("CSV vs OTROS FORMATOS TABULARES")
    print('='*70)
    
    comparacion = """
┌─────────────┬──────────┬────────────┬─────────────┬────────────┐
│   Formato   │  Tamaño  │ Velocidad  │  Tipos de   │   Uso      │
│             │          │   Lectura  │    Datos    │  Principal │
├─────────────┼──────────┼────────────┼─────────────┼────────────┤
│ CSV         │ Grande   │   Lento    │ No preserva │ Universal  │
│             │          │            │ tipos       │ Intercambio│
├─────────────┼──────────┼────────────┼─────────────┼────────────┤
│ Parquet     │ Pequeño  │   Rápido   │ Preserva    │ Big Data   │
│             │(columnar)│  (columnar)│ tipos       │ Analytics  │
├─────────────┼──────────┼────────────┼─────────────┼────────────┤
│ Pickle      │ Mediano  │ Muy rápido │ Preserva    │ Python     │
│             │          │            │ TODO        │ interno    │
├─────────────┼──────────┼────────────┼─────────────┼────────────┤
│ Excel       │ Grande   │   Lento    │ Limitado    │ Negocios   │
│             │          │            │             │ Reportes   │
├─────────────┼──────────┼────────────┼─────────────┼────────────┤
│ HDF5        │ Pequeño  │   Rápido   │ Preserva    │ Científico │
│             │          │            │ tipos       │ Arrays     │
└─────────────┴──────────┴────────────┴─────────────┴────────────┘

📊 CUÁNDO USAR CSV:
  ✓ Intercambio de datos entre sistemas diferentes
  ✓ Legibilidad humana importante
  ✓ Compatibilidad universal requerida
  ✓ Datasets pequeños a medianos (<1GB)
  
⚠️  CUÁNDO NO USAR CSV:
  ✗ Datasets muy grandes (usar Parquet)
  ✗ Necesitas preservar tipos de datos (usar Pickle/Parquet)
  ✗ Consultas analíticas frecuentes (usar Parquet/HDF5)
  ✗ Datos jerárquicos complejos (usar JSON/XML/Parquet)
"""
    print(comparacion)


if __name__ == "__main__":
    print("="*70)
    print("EJEMPLOS PRÁCTICOS: PROCESAMIENTO DE CSV")
    print("="*70)
    
    # Analizar cada archivo
    archivos = [
        'empleados_simple.csv',
        'sensores_iot.csv',
        'transacciones_pipe.csv',
        'pacientes_comillas.csv',
        'experimentos_tabs.csv'
    ]
    
    for archivo in archivos:
        try:
            analizar_csv_estructura(archivo)
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")
    
    # Demostrar problemas comunes
    problemas_comunes_csv()
    
    # Pipeline de ML
    try:
        csv_para_ml_pipeline()
    except Exception as e:
        print(f"❌ Error en pipeline ML: {e}")
    
    # Conversión a otros formatos
    try:
        csv_a_otros_formatos('empleados_simple.csv')
    except Exception as e:
        print(f"❌ Error en conversión: {e}")
    
    # Comparación
    comparacion_csv_vs_otros()
    
    print("\n" + "="*70)
    print("✓ Procesamiento completado")
    print("="*70)
