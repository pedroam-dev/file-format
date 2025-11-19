#!/usr/bin/env python3
"""
Script completo de procesamiento de archivos JSON para Ciencia de Datos
Demuestra JSON estándar, JSON Lines, JSON Schema, y conversión a otros formatos
"""

import json
import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, List, Any
import pandas as pd
from collections import defaultdict
import os


def cargar_json(archivo: str) -> Dict:
    """
    Carga un archivo JSON
    
    Args:
        archivo: Ruta al archivo JSON
        
    Returns:
        Diccionario con datos JSON
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)


def cargar_jsonl(archivo: str) -> List[Dict]:
    """
    Carga un archivo JSON Lines (cada línea es un JSON)
    
    Args:
        archivo: Ruta al archivo JSONL
        
    Returns:
        Lista de diccionarios
    """
    datos = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():  # Ignorar líneas vacías
                datos.append(json.loads(linea))
    return datos


def analizar_estructura_json(datos: Any, prefijo: str = "", max_profundidad: int = 5):
    """
    Analiza recursivamente la estructura de un JSON
    
    Args:
        datos: Datos JSON a analizar
        prefijo: Prefijo para el path actual
        max_profundidad: Profundidad máxima de análisis
    """
    if max_profundidad == 0:
        print(f"{prefijo}: [profundidad máxima alcanzada]")
        return
    
    if isinstance(datos, dict):
        for clave, valor in datos.items():
            nuevo_prefijo = f"{prefijo}.{clave}" if prefijo else clave
            tipo = type(valor).__name__
            
            if isinstance(valor, (dict, list)):
                tamaño = len(valor)
                print(f"{nuevo_prefijo}: {tipo} (tamaño={tamaño})")
                analizar_estructura_json(valor, nuevo_prefijo, max_profundidad - 1)
            else:
                print(f"{nuevo_prefijo}: {tipo} = {repr(valor)[:50]}")
    
    elif isinstance(datos, list):
        if len(datos) > 0:
            print(f"{prefijo}[0]: {type(datos[0]).__name__}")
            if len(datos) > 1:
                print(f"{prefijo}[1..{len(datos)-1}]: ... ({len(datos)-1} elementos más)")
            analizar_estructura_json(datos[0], f"{prefijo}[0]", max_profundidad - 1)


def validar_con_schema(datos_json: Dict, schema_json: Dict) -> bool:
    """
    Valida datos JSON contra un JSON Schema
    
    Args:
        datos_json: Datos a validar
        schema_json: Schema JSON
        
    Returns:
        True si es válido, False en caso contrario
    """
    try:
        validate(instance=datos_json, schema=schema_json)
        print("✓ JSON es válido según el schema")
        return True
    except ValidationError as e:
        print(f"✗ JSON no es válido:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        print(f"  Schema path: {' -> '.join(str(p) for p in e.schema_path)}")
        return False


def extraer_metricas_experimentos(datos: Dict) -> pd.DataFrame:
    """
    Extrae métricas de experimentos a DataFrame
    
    Args:
        datos: Datos JSON con experimentos
        
    Returns:
        DataFrame con métricas
    """
    experimentos = datos['investigacion']['experimentos']
    
    filas = []
    for exp in experimentos:
        fila = {
            'id': exp['id'],
            'fecha': exp['fecha'],
            'modelo': exp['modelo']['nombre'],
            'arquitectura': exp['modelo']['arquitectura'],
            'parametros': exp['modelo']['parametros'],
            'batch_size': exp['hiperparametros']['batch_size'],
            'learning_rate': exp['hiperparametros']['learning_rate'],
            'epochs': exp['hiperparametros']['epochs'],
            'accuracy': exp['resultados']['accuracy'],
            'precision': exp['resultados']['precision'],
            'recall': exp['resultados']['recall'],
            'f1_score': exp['resultados']['f1_score'],
            'tiempo_entrenamiento_seg': exp['resultados']['tiempo_entrenamiento_seg'],
            'tiempo_inferencia_ms': exp['resultados']['tiempo_inferencia_ms']
        }
        filas.append(fila)
    
    return pd.DataFrame(filas)


def analizar_grafo_json(datos: Dict):
    """
    Analiza estadísticas de un grafo en formato JSON
    
    Args:
        datos: Datos del grafo en JSON
    """
    grafo = datos['grafo_conocimiento']
    
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DEL GRAFO: {grafo['metadata']['nombre']}")
    print('='*70)
    
    # Estadísticas generales
    meta = grafo['metadata']
    stats = meta['estadisticas']
    print(f"\n📊 Estadísticas generales:")
    print(f"   • Nodos: {stats['num_nodos']}")
    print(f"   • Aristas: {stats['num_aristas']}")
    print(f"   • Densidad: {stats['densidad']:.4f}")
    print(f"   • Diámetro: {stats['diametro']}")
    
    # Análisis de nodos por tipo
    nodos_por_tipo = defaultdict(int)
    for nodo in grafo['nodos']:
        nodos_por_tipo[nodo['tipo']] += 1
    
    print(f"\n🔵 Nodos por tipo:")
    for tipo, count in nodos_por_tipo.items():
        print(f"   • {tipo}: {count}")
    
    # Análisis de aristas por tipo
    aristas_por_tipo = defaultdict(int)
    for arista in grafo['aristas']:
        aristas_por_tipo[arista['tipo']] += 1
    
    print(f"\n🔗 Aristas por tipo:")
    for tipo, count in aristas_por_tipo.items():
        print(f"   • {tipo}: {count}")
    
    # Investigadores con más colaboraciones
    colaboraciones = defaultdict(list)
    for arista in grafo['aristas']:
        if arista['tipo'] == 'COLABORA_CON':
            fuente = arista['fuente']
            destino = arista['destino']
            fuerza = arista['propiedades']['fuerza_colaboracion']
            colaboraciones[fuente].append((destino, fuerza))
            colaboraciones[destino].append((fuente, fuerza))
    
    print(f"\n👥 Top investigadores por número de colaboraciones:")
    top_colaboradores = sorted(
        colaboraciones.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:3]
    
    for inv_id, colabs in top_colaboradores:
        # Buscar nombre del investigador
        nombre = next(
            (n['propiedades']['nombre'] for n in grafo['nodos'] if n['id'] == inv_id),
            inv_id
        )
        print(f"   • {nombre}: {len(colabs)} colaboraciones")


def json_vs_jsonl_demo():
    """
    Demuestra las diferencias entre JSON y JSON Lines
    """
    print(f"\n{'='*70}")
    print("JSON vs JSON LINES (JSONL)")
    print('='*70)
    
    # JSON estándar
    print("\n📄 JSON ESTÁNDAR:")
    print("   • Un único objeto/array que contiene todos los datos")
    print("   • Debe cargarse completo en memoria")
    print("   • No se puede procesar línea por línea")
    print("   • Formato: { \"datos\": [...] }")
    
    # JSON Lines
    print("\n📄 JSON LINES (JSONL):")
    print("   • Cada línea es un JSON válido independiente")
    print("   • Puede procesarse en streaming")
    print("   • Ideal para logs y datos de sensores")
    print("   • Formato: cada línea es un JSON")
    
    # Cargar y mostrar JSONL
    datos_jsonl = cargar_jsonl('sensores_streaming.jsonl')
    print(f"\n✓ Cargadas {len(datos_jsonl)} líneas de sensores_streaming.jsonl")
    print("\nPrimeras 3 líneas:")
    for i, dato in enumerate(datos_jsonl[:3], 1):
        print(f"   {i}. {dato}")
    
    # Convertir JSONL a DataFrame
    df = pd.DataFrame(datos_jsonl)
    print(f"\n📊 Convertido a DataFrame: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(df.head())
    
    # Estadísticas por sensor
    print(f"\n📈 Estadísticas por sensor:")
    stats = df.groupby('sensor_id').agg({
        'temperatura': ['mean', 'std', 'min', 'max'],
        'humedad': ['mean', 'std']
    }).round(2)
    print(stats)


def json_nested_to_flat():
    """
    Demuestra cómo aplanar JSON anidado
    """
    print(f"\n{'='*70}")
    print("APLANAMIENTO DE JSON ANIDADO")
    print('='*70)
    
    datos = cargar_json('investigacion_nlp.json')
    
    # Extraer información anidada
    inv = datos['investigacion']['investigador_principal']
    
    datos_planos = {
        'titulo': datos['investigacion']['titulo'],
        'investigador_nombre': inv['nombre'],
        'investigador_email': inv['email'],
        'institucion': inv['afiliacion']['institucion'],
        'departamento': inv['afiliacion']['departamento'],
        'pais': inv['afiliacion']['pais'],
        'num_tweets': datos['investigacion']['dataset']['tamaño']['tweets'],
        'tamano_mb': datos['investigacion']['dataset']['tamaño']['tamano_mb'],
        'mejor_modelo': datos['investigacion']['conclusiones']['mejor_modelo'],
        'mejor_accuracy': max(
            exp['resultados']['accuracy'] 
            for exp in datos['investigacion']['experimentos']
        )
    }
    
    print("\nJSON anidado original:")
    print(json.dumps(
        {k: datos['investigacion'][k] for k in ['titulo', 'investigador_principal']},
        indent=2,
        ensure_ascii=False
    )[:300] + "...")
    
    print("\n➡️  JSON plano resultante:")
    print(json.dumps(datos_planos, indent=2, ensure_ascii=False))
    
    # Usar pandas para aplanar
    df_flat = pd.json_normalize(datos['investigacion'])
    print(f"\n✓ Aplanado con pandas.json_normalize:")
    print(f"  Columnas: {len(df_flat.columns)}")
    print(f"  Muestra de columnas: {list(df_flat.columns)[:5]}")


def comparacion_formatos():
    """
    Compara JSON con XML y CSV
    """
    print(f"\n{'='*70}")
    print("COMPARACIÓN: JSON vs XML vs CSV")
    print('='*70)
    
    comparacion = """
┌──────────────┬─────────┬──────────┬───────────┬─────────────┬──────────┐
│  Aspecto     │  JSON   │   XML    │    CSV    │   Parquet   │  Pickle  │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Legibilidad  │   ⭐⭐⭐⭐   │  ⭐⭐⭐    │   ⭐⭐⭐⭐⭐   │     ⭐       │    ⭐     │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Tamaño       │  Medio  │  Grande  │  Pequeño  │  Muy peq.   │  Medio   │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Parsing      │  Rápido │  Lento   │  Rápido   │  Muy rápido │ Rápido   │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Anidación    │    ✓    │    ✓     │     ✗     │      ✓      │    ✓     │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Tipos datos  │ Básicos │ Básicos  │ Solo str  │  Preserva   │Preserva  │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Streaming    │ Limitado│ Limitado │     ✓     │      ✓      │    ✗     │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Schema       │   ✓ *   │    ✓     │     ✗     │      ✓      │    ✗     │
├──────────────┼─────────┼──────────┼───────────┼─────────────┼──────────┤
│ Ecosistema   │   Web   │Enterprise│ Universal │  Big Data   │  Python  │
└──────────────┴─────────┴──────────┴───────────┴─────────────┴──────────┘

* JSON Schema (estándar separado)

🎯 CUÁNDO USAR JSON:
  ✓ APIs REST / GraphQL
  ✓ Configuración de aplicaciones
  ✓ Datos jerárquicos (grafos, árboles)
  ✓ Intercambio web (JavaScript nativo)
  ✓ NoSQL databases (MongoDB, CouchDB)

🎯 CUÁNDO USAR JSON LINES:
  ✓ Logs de aplicaciones
  ✓ Streaming de datos (IoT, eventos)
  ✓ Datasets grandes que no caben en memoria
  ✓ Procesamiento incremental
  ✓ Machine Learning training data

⚠️  LIMITACIONES DE JSON:
  ✗ No soporta fechas nativas (usar ISO 8601 strings)
  ✗ No distingue int vs float (todo es "number")
  ✗ No soporta comentarios (usar "_comment" keys)
  ✗ No soporta referencias/punteros
  ✗ Archivos muy grandes son difíciles de editar
"""
    print(comparacion)


if __name__ == "__main__":
    print("="*70)
    print("EJEMPLOS PRÁCTICOS: PROCESAMIENTO DE JSON")
    print("="*70)
    
    # 1. Analizar estructura
    print("\n1. ANÁLISIS DE ESTRUCTURA JSON")
    print("-" * 70)
    datos_inv = cargar_json('investigacion_nlp.json')
    analizar_estructura_json(datos_inv, max_profundidad=3)
    
    # 2. Extraer métricas
    print("\n2. EXTRACCIÓN DE MÉTRICAS A DATAFRAME")
    print("-" * 70)
    df_metricas = extraer_metricas_experimentos(datos_inv)
    print(df_metricas.to_string(index=False))
    
    # 3. Analizar grafo
    datos_grafo = cargar_json('grafo_conocimiento.json')
    analizar_grafo_json(datos_grafo)
    
    # 4. JSON vs JSON Lines
    json_vs_jsonl_demo()
    
    # 5. Aplanamiento
    json_nested_to_flat()
    
    # 6. Validación con schema
    print(f"\n{'='*70}")
    print("VALIDACIÓN CON JSON SCHEMA")
    print('='*70)
    
    schema = cargar_json('schema_experimento.json')
    
    # Ejemplo válido
    experimento_valido = {
        "id": "EXP-001",
        "fecha": "2025-11-19",
        "modelo": {
            "nombre": "BERT",
            "tipo": "clasificacion"
        },
        "dataset": {
            "nombre": "IMDB",
            "tamaño": {
                "train": 25000,
                "test": 25000
            }
        },
        "resultados": {
            "accuracy": 0.89
        }
    }
    
    print("\n✅ Validando experimento válido:")
    validar_con_schema(experimento_valido, schema)
    
    # Ejemplo inválido
    experimento_invalido = {
        "id": "EXP001",  # Formato incorrecto (falta guión)
        "fecha": "2025-11-19",
        "modelo": {
            "nombre": "BERT",
            "tipo": "clasificacion"
        },
        "dataset": {
            "nombre": "IMDB",
            "tamaño": {
                "train": -100  # Número negativo (inválido)
            }
        },
        "resultados": {
            "accuracy": 1.5  # Mayor que 1 (inválido)
        }
    }
    
    print("\n❌ Validando experimento inválido:")
    validar_con_schema(experimento_invalido, schema)
    
    # 7. Comparación de formatos
    comparacion_formatos()
    
    print("\n" + "="*70)
    print("✓ Procesamiento completado")
    print("="*70)
