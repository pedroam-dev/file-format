#!/usr/bin/env python3
"""
Script de procesamiento de archivos XML para Ciencia de Datos
Demuestra diferentes técnicas de parsing y análisis
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
from typing import Dict, List
import json


def parse_experimentos_ml(xml_file: str) -> pd.DataFrame:
    """
    Extrae información de experimentos de ML desde XML a DataFrame
    
    Args:
        xml_file: Ruta al archivo XML con experimentos
        
    Returns:
        DataFrame con resultados de experimentos
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    experimentos = []
    
    for exp in root.findall('.//experiment'):
        exp_data = {
            'experiment_id': exp.get('id'),
            'model_name': exp.find('model_name').text,
            'training_samples': int(exp.find('.//training_samples').text),
            'test_samples': int(exp.find('.//test_samples').text),
            'features': int(exp.find('.//features').text),
            'accuracy': float(exp.find('.//accuracy').text),
            'precision': float(exp.find('.//precision').text),
            'recall': float(exp.find('.//recall').text),
            'f1_score': float(exp.find('.//f1_score').text),
            'execution_time': float(exp.find('execution_time').text)
        }
        
        # Extraer hiperparámetros (estructura variable)
        hyperparams = {}
        for param in exp.find('hyperparameters'):
            if param.tag == 'layers':
                layers_info = []
                for layer in param:
                    layer_dict = dict(layer.attrib)
                    layer_dict['type'] = layer.get('type')
                    layers_info.append(layer_dict)
                hyperparams['layers'] = layers_info
            else:
                hyperparams[param.tag] = param.text
        
        exp_data['hyperparameters'] = json.dumps(hyperparams)
        experimentos.append(exp_data)
    
    return pd.DataFrame(experimentos)


def analizar_ontologia(xml_file: str) -> Dict:
    """
    Analiza estructura de ontología médica
    
    Args:
        xml_file: Ruta al archivo XML con ontología
        
    Returns:
        Diccionario con estadísticas de la ontología
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    clases = root.findall('.//class')
    
    analisis = {
        'total_classes': len(clases),
        'jerarquia': {},
        'relaciones': [],
        'propiedades_por_clase': {}
    }
    
    for clase in clases:
        class_id = clase.get('id')
        class_name = clase.find('name').text
        parent = clase.find('parent').text
        
        analisis['jerarquia'][class_name] = {
            'id': class_id,
            'parent': parent
        }
        
        # Contar propiedades
        properties = clase.findall('.//property')
        analisis['propiedades_por_clase'][class_name] = len(properties)
        
        # Extraer relaciones
        relations = clase.findall('.//relation')
        for rel in relations:
            analisis['relaciones'].append({
                'source': class_name,
                'type': rel.get('type'),
                'target': rel.get('target'),
                'probability': rel.get('probability', 'N/A')
            })
    
    return analisis


def validar_xml_schema(xml_file: str) -> bool:
    """
    Valida que el XML esté bien formado
    
    Args:
        xml_file: Ruta al archivo XML
        
    Returns:
        True si es válido, False en caso contrario
    """
    try:
        tree = ET.parse(xml_file)
        print(f"✓ {xml_file} es un XML bien formado")
        
        # Estadísticas básicas
        root = tree.getroot()
        elementos = len(list(root.iter()))
        profundidad = max_depth(root)
        
        print(f"  - Elementos totales: {elementos}")
        print(f"  - Profundidad máxima: {profundidad}")
        print(f"  - Elemento raíz: <{root.tag}>")
        
        return True
    except ET.ParseError as e:
        print(f"✗ Error parseando {xml_file}: {e}")
        return False


def max_depth(element, depth=0):
    """Calcula la profundidad máxima del árbol XML"""
    if len(element) == 0:
        return depth
    return max(max_depth(child, depth + 1) for child in element)


def xml_to_dict(element) -> Dict:
    """
    Convierte un elemento XML a diccionario (útil para comparar con JSON)
    """
    result = {}
    
    # Atributos
    if element.attrib:
        result['@attributes'] = element.attrib
    
    # Texto
    if element.text and element.text.strip():
        if len(element) == 0:
            return element.text.strip()
        result['#text'] = element.text.strip()
    
    # Hijos
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            # Si ya existe, convertir a lista
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    
    return result


def comparar_xml_vs_json():
    """
    Demuestra las diferencias entre XML y JSON para representar datos
    """
    print("\n" + "="*60)
    print("COMPARACIÓN XML vs JSON")
    print("="*60)
    
    # Crear estructura de datos
    data = {
        'investigador': {
            'nombre': 'Dr. Juan Pérez',
            'especialidad': 'Machine Learning',
            'publicaciones': [
                {'titulo': 'Deep Learning en Salud', 'año': 2024, 'citas': 45},
                {'titulo': 'NLP para Diagnóstico', 'año': 2025, 'citas': 12}
            ]
        }
    }
    
    # JSON
    print("\nJSON (más compacto, nativo en web):")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    json_size = len(json.dumps(data).encode('utf-8'))
    print(f"Tamaño: {json_size} bytes")
    
    # XML equivalente
    print("\nXML (más verboso, mejor para documentos complejos):")
    xml_str = """<?xml version="1.0" encoding="UTF-8"?>
<investigador>
    <nombre>Dr. Juan Pérez</nombre>
    <especialidad>Machine Learning</especialidad>
    <publicaciones>
        <publicacion>
            <titulo>Deep Learning en Salud</titulo>
            <año>2024</año>
            <citas>45</citas>
        </publicacion>
        <publicacion>
            <titulo>NLP para Diagnóstico</titulo>
            <año>2025</año>
            <citas>12</citas>
        </publicacion>
    </publicaciones>
</investigador>"""
    print(xml_str)
    xml_size = len(xml_str.encode('utf-8'))
    print(f"Tamaño: {xml_size} bytes")
    
    print(f"\n📊 XML es {((xml_size/json_size - 1) * 100):.1f}% más grande")
    print("\nVentajas de XML:")
    print("  • Soporte de namespaces (evita colisiones de nombres)")
    print("  • Atributos y contenido mixto")
    print("  • Validación con XSD/DTD")
    print("  • XPath/XSLT para consultas complejas")
    print("\nVentajas de JSON:")
    print("  • Más ligero y rápido de parsear")
    print("  • Mapeo directo a estructuras de datos")
    print("  • Mejor para APIs REST")
    print("  • Más legible para humanos")


if __name__ == "__main__":
    print("="*60)
    print("EJEMPLOS PRÁCTICOS: PROCESAMIENTO DE XML")
    print("="*60)
    
    # 1. Validar archivos XML
    print("\n1. VALIDACIÓN DE ARCHIVOS XML")
    print("-" * 60)
    validar_xml_schema('dataset_investigacion.xml')
    print()
    validar_xml_schema('ontologia_medica.xml')
    
    # 2. Extraer experimentos a DataFrame
    print("\n2. EXTRACCIÓN DE EXPERIMENTOS A DATAFRAME")
    print("-" * 60)
    df = parse_experimentos_ml('dataset_investigacion.xml')
    print(df.to_string())
    
    # 3. Análisis de ontología
    print("\n3. ANÁLISIS DE ONTOLOGÍA MÉDICA")
    print("-" * 60)
    analisis = analizar_ontologia('ontologia_medica.xml')
    print(f"Total de clases: {analisis['total_classes']}")
    print("\nJerarquía de clases:")
    for clase, info in analisis['jerarquia'].items():
        print(f"  • {clase} -> parent: {info['parent']}")
    
    print("\nRelaciones entre clases:")
    for rel in analisis['relaciones']:
        print(f"  • {rel['source']} --[{rel['type']}]--> {rel['target']}")
    
    # 4. Comparación XML vs JSON
    comparar_xml_vs_json()
    
    print("\n" + "="*60)
    print("✓ Procesamiento completado")
    print("="*60)
