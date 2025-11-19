#!/usr/bin/env python3
"""
Ejemplos prácticos de formatos contenedores: Video e Imagen
Extracción de metadatos para Ciencia de Datos y Computer Vision
"""

from PIL import Image
from PIL.ExifTags import TAGS
import json
from pathlib import Path
from typing import Dict, List, Any
import struct


def analizar_imagen_metadata():
    """
    Explica los metadatos en formatos de imagen
    """
    print(f"\n{'='*70}")
    print("FORMATOS CONTENEDORES DE IMAGEN")
    print('='*70)
    
    print("""
📷 FORMATOS DE IMAGEN - Conceptos clave:

1. RASTER vs VECTOR:
   • Raster: Píxeles (JPEG, PNG, BMP, TIFF, WebP)
   • Vector: Formas matemáticas (SVG, AI, EPS)

2. COMPRESIÓN:
   • Sin pérdida (Lossless): PNG, GIF, BMP, TIFF
   • Con pérdida (Lossy): JPEG, WebP

3. TRANSPARENCIA:
   • Soportan: PNG, GIF, WebP, TIFF
   • No soportan: JPEG, BMP

┌────────────┬──────────┬────────────┬──────────────┬─────────────────┐
│  Formato   │  Tipo    │ Compresión │ Transparencia│  Uso principal  │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ JPEG       │ Raster   │ Lossy      │      ✗       │ Fotografía      │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ PNG        │ Raster   │ Lossless   │      ✓       │ Gráficos, web   │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ GIF        │ Raster   │ Lossless   │      ✓       │ Animaciones     │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ WebP       │ Raster   │ Both       │      ✓       │ Web moderna     │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ TIFF       │ Raster   │ Optional   │      ✓       │ Impresión, GIS  │
├────────────┼──────────┼────────────┼──────────────┼─────────────────┤
│ BMP        │ Raster   │ None       │      ✗       │ Windows nativo  │
└────────────┴──────────┴────────────┴──────────────┴─────────────────┘

🔬 METADATOS IMPORTANTES PARA CIENCIA DE DATOS:

EXIF (Exchangeable Image File Format):
  • Cámara: Marca, modelo, lente
  • Configuración: ISO, apertura, velocidad obturación, distancia focal
  • Tiempo: Fecha y hora de captura
  • Ubicación: GPS (latitud, longitud, altitud)
  • Orientación: Rotación de la imagen

IPTC (International Press Telecommunications Council):
  • Autor, copyright, caption
  • Keywords, categorías
  • Usado en fotoperiodismo

XMP (Extensible Metadata Platform):
  • Adobe standard
  • Extensible, basado en XML
  • Soporta metadatos personalizados
""")


def crear_imagen_ejemplo():
    """
    Crea imágenes de ejemplo con diferentes características
    """
    print(f"\n📁 Creando imágenes de ejemplo...")
    
    Path("imagenes_ejemplo").mkdir(exist_ok=True)
    
    # 1. PNG con transparencia
    img_png = Image.new('RGBA', (200, 200), (255, 0, 0, 0))
    # Dibujar círculo con transparencia
    for x in range(200):
        for y in range(200):
            dist = ((x - 100) ** 2 + (y - 100) ** 2) ** 0.5
            if dist < 80:
                alpha = int(255 * (1 - dist / 80))
                img_png.putpixel((x, y), (0, 128, 255, alpha))
    
    img_png.save('imagenes_ejemplo/circulo_transparente.png')
    print("✓ PNG con transparencia: circulo_transparente.png")
    
    # 2. JPEG (degradado)
    img_jpg = Image.new('RGB', (400, 300))
    for x in range(400):
        for y in range(300):
            r = int(255 * x / 400)
            g = int(255 * y / 300)
            b = 128
            img_jpg.putpixel((x, y), (r, g, b))
    
    # Guardar con diferentes calidades
    img_jpg.save('imagenes_ejemplo/degradado_q95.jpg', quality=95)
    img_jpg.save('imagenes_ejemplo/degradado_q50.jpg', quality=50)
    img_jpg.save('imagenes_ejemplo/degradado_q10.jpg', quality=10)
    print("✓ JPEG con diferentes calidades: degradado_q*.jpg")
    
    # 3. GIF animado simulado
    img_gif = Image.new('P', (100, 100), 0)
    # Paleta simple
    palette = [i for i in range(256) for _ in range(3)]
    img_gif.putpalette(palette)
    img_gif.save('imagenes_ejemplo/paleta.gif')
    print("✓ GIF con paleta: paleta.gif")


def analizar_imagen_detallado(ruta_imagen: str) -> Dict[str, Any]:
    """
    Extrae toda la información posible de una imagen
    
    Args:
        ruta_imagen: Ruta a la imagen
        
    Returns:
        Diccionario con metadatos
    """
    img = Image.open(ruta_imagen)
    
    metadata = {
        'archivo': {
            'ruta': ruta_imagen,
            'nombre': Path(ruta_imagen).name,
            'tamaño_bytes': Path(ruta_imagen).stat().st_size,
            'formato_archivo': Path(ruta_imagen).suffix
        },
        'imagen': {
            'formato': img.format,
            'modo': img.mode,
            'tamaño': img.size,
            'ancho': img.width,
            'alto': img.height,
            'num_pixeles': img.width * img.height,
            'megapixeles': round(img.width * img.height / 1_000_000, 2)
        },
        'profundidad': {
            'modo_descripcion': {
                '1': '1-bit pixels, blanco y negro',
                'L': '8-bit pixels, escala de grises',
                'P': '8-bit pixels, paleta',
                'RGB': '3x8-bit pixels, color verdadero',
                'RGBA': '4x8-bit pixels, color verdadero + alpha',
                'CMYK': '4x8-bit pixels, separación de color',
                'YCbCr': '3x8-bit pixels, formato de video',
                'LAB': '3x8-bit pixels, espacio de color L*a*b',
                'HSV': '3x8-bit pixels, Hue, Saturation, Value',
                'I': '32-bit signed integer pixels',
                'F': '32-bit floating point pixels'
            }.get(img.mode, 'Desconocido'),
            'canales': len(img.getbands()),
            'bandas': img.getbands()
        }
    }
    
    # EXIF data (si existe)
    if hasattr(img, '_getexif') and img._getexif():
        exif_data = {}
        for tag_id, value in img._getexif().items():
            tag = TAGS.get(tag_id, tag_id)
            exif_data[tag] = str(value)
        metadata['exif'] = exif_data
    
    # Info adicional del formato
    if hasattr(img, 'info'):
        metadata['info_formato'] = dict(img.info)
    
    return metadata


def comparar_tamaños_compresion():
    """
    Compara tamaños de archivo con diferentes formatos y calidades
    """
    print(f"\n{'='*70}")
    print("COMPARACIÓN DE TAMAÑOS - COMPRESIÓN DE IMAGEN")
    print('='*70)
    
    archivos = [
        'imagenes_ejemplo/degradado_q95.jpg',
        'imagenes_ejemplo/degradado_q50.jpg',
        'imagenes_ejemplo/degradado_q10.jpg',
        'imagenes_ejemplo/circulo_transparente.png',
        'imagenes_ejemplo/paleta.gif'
    ]
    
    print(f"\n{'Archivo':<35s} {'Formato':<8s} {'Tamaño':<12s} {'Dimensiones':<15s} {'Modo':<8s}")
    print("-" * 85)
    
    for archivo in archivos:
        if Path(archivo).exists():
            img = Image.open(archivo)
            tamaño = Path(archivo).stat().st_size
            print(f"{Path(archivo).name:<35s} {img.format:<8s} "
                  f"{tamaño:>8d} bytes  {img.width}x{img.height:<12s} {img.mode:<8s}")
    
    print(f"\n💡 Observaciones:")
    print("   • JPEG Q95: Alta calidad, archivo más grande")
    print("   • JPEG Q50: Calidad media, buen balance")
    print("   • JPEG Q10: Baja calidad, muy comprimido, artefactos visibles")
    print("   • PNG: Sin pérdida, soporta transparencia")
    print("   • GIF: Paleta limitada (256 colores), soporta animación")


def analizar_formato_video():
    """
    Explica formatos contenedores de video
    """
    print(f"\n{'='*70}")
    print("FORMATOS CONTENEDORES DE VIDEO")
    print('='*70)
    
    print("""
🎬 CONTENEDOR vs CODEC:

CONTENEDOR (Container):
  • Es el "envoltorio" del archivo
  • Contiene: video + audio + subtítulos + metadatos
  • Ejemplos: MP4, MKV, AVI, MOV, WebM

CODEC (Coder-Decoder):
  • Algoritmo de compresión de video/audio
  • Video: H.264, H.265/HEVC, VP9, AV1
  • Audio: AAC, MP3, Opus, FLAC

Ejemplo: archivo.mp4 puede contener:
  • Video: H.264 codec
  • Audio: AAC codec
  • Subtítulos: SRT
  • Metadatos: título, duración, etc.

┌────────────┬──────────────┬──────────────┬─────────────────────────────┐
│ Contenedor │  Extensión   │ Codecs común │     Uso principal           │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ MP4        │ .mp4, .m4v   │ H.264/H.265  │ Universal, web, streaming   │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ MKV        │ .mkv         │ Cualquiera   │ Archivo, múltiples pistas   │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ WebM       │ .webm        │ VP8/VP9, AV1 │ Web (HTML5 video)           │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ AVI        │ .avi         │ Variable     │ Legado (Windows antiguo)    │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ MOV        │ .mov, .qt    │ Variable     │ Apple, edición profesional  │
├────────────┼──────────────┼──────────────┼─────────────────────────────┤
│ FLV        │ .flv         │ H.263/H.264  │ Flash (obsoleto)            │
└────────────┴──────────────┴──────────────┴─────────────────────────────┘

🎥 CODECS DE VIDEO MODERNOS:

H.264/AVC (2003):
  • Más usado actualmente
  • Buen balance calidad/tamaño
  • Soportado universalmente
  • Patentado (pero ampliamente licenciado)

H.265/HEVC (2013):
  • 50% mejor compresión que H.264
  • Mayor calidad a igual bitrate
  • Requiere más procesamiento
  • 4K, 8K, HDR
  • Problemas de licencias

VP9 (2013):
  • Google, open source
  • Similar a H.265
  • Usado en YouTube
  • WebM container

AV1 (2018):
  • Sucesor de VP9
  • 30% mejor que H.265
  • Completamente libre (royalty-free)
  • Futuro de streaming
  • Usado por Netflix, YouTube

🔊 CODECS DE AUDIO:

AAC (Advanced Audio Coding):
  • Sucesor de MP3
  • Mejor calidad que MP3 a mismo bitrate
  • Estándar en MP4, iOS

MP3:
  • Legado pero universal
  • Patentes expiradas
  • Buen soporte

Opus:
  • Moderno, open source
  • Mejor que AAC
  • Usado en WebRTC, WhatsApp

FLAC:
  • Sin pérdida (lossless)
  • Para archiving de audio

📊 METADATOS EN VIDEO:

Metadatos de contenedor:
  • Duración total
  • Número de pistas (video, audio, subtítulos)
  • Fecha de creación
  • Título, artista, álbum (ID3 tags)

Metadatos de video:
  • Resolución (1920x1080, 3840x2160, etc.)
  • Frame rate (24fps, 30fps, 60fps)
  • Bitrate (kbps o Mbps)
  • Codec usado
  • Aspect ratio (16:9, 4:3, 21:9)
  • Color space (BT.709, BT.2020)
  • HDR metadata

Metadatos de audio:
  • Sample rate (44.1kHz, 48kHz)
  • Bitrate (128kbps, 320kbps)
  • Canales (mono, stereo, 5.1, 7.1)
  • Codec
  • Idioma
""")


def estructura_mp4():
    """
    Explica la estructura interna de un archivo MP4
    """
    print(f"\n{'='*70}")
    print("ESTRUCTURA INTERNA: MP4 (MPEG-4 Part 14)")
    print('='*70)
    
    print("""
📦 ESTRUCTURA DE CAJAS (BOX/ATOM):

MP4 usa estructura jerárquica de "cajas" (boxes o atoms).
Cada caja tiene:
  • Tamaño (4 bytes)
  • Tipo (4 bytes, ej: 'ftyp', 'moov', 'mdat')
  • Datos

Estructura típica de MP4:

archivo.mp4
│
├── ftyp (File Type Box)
│   └── Identifica formato y compatibilidad
│
├── moov (Movie Box) - METADATOS
│   ├── mvhd (Movie Header)
│   │   └── Duración, escala de tiempo, fecha creación
│   │
│   └── trak (Track) - Una por cada pista
│       ├── tkhd (Track Header)
│       │   └── ID, dimensiones, volumen
│       │
│       ├── mdia (Media)
│       │   ├── mdhd (Media Header)
│       │   │   └── Duración, idioma
│       │   │
│       │   └── minf (Media Information)
│       │       ├── vmhd (Video Media Header) o
│       │       ├── smhd (Sound Media Header)
│       │       │
│       │       └── stbl (Sample Table)
│       │           ├── stsd (Sample Description)
│       │           │   └── Codec, resolución
│       │           ├── stts (Time-to-Sample)
│       │           ├── stsc (Sample-to-Chunk)
│       │           └── stco (Chunk Offset)
│       │
│       └── edts (Edit List) - Opcional
│
└── mdat (Media Data Box) - DATOS REALES
    └── Frames de video y audio comprimidos

🔍 CAJAS IMPORTANTES PARA CIENCIA DE DATOS:

1. ftyp - Identifica compatibilidad
   • major_brand: 'isom', 'mp41', 'mp42'
   • compatible_brands: lista de formatos soportados

2. moov - Todo los metadatos (crítico)
   • Puede estar al inicio (fast start) o al final
   • "Fast start": mejor para streaming web

3. mdat - Datos multimedia
   • Puede ser muy grande (GB)
   • Contiene frames H.264/H.265 comprimidos

4. uuid - Metadatos personalizados
   • GPS, cámara específica, timestamps
   • Usado por drones, cámaras deportivas

🎯 EXTRACCIÓN DE METADATOS SIN LIBRERÍAS PESADAS:

Para análisis rápido sin decodificar video:
  • Leer solo 'moov' box
  • Parsear 'stsd' para codec
  • Parsear 'mvhd' para duración
  • No necesitas decodificar 'mdat'

Ventajas:
  ✓ Muy rápido (KB vs GB)
  ✓ No requiere FFmpeg
  ✓ Ideal para análisis batch de miles de videos
""")


def casos_uso_vision():
    """
    Casos de uso en Computer Vision y Data Science
    """
    print(f"\n{'='*70}")
    print("CASOS DE USO EN COMPUTER VISION Y DATA SCIENCE")
    print('='*70)
    
    print("""
🤖 COMPUTER VISION:

1. DATASETS DE IMÁGENES:
   
   ImageNet:
     • Formato: JPEG
     • Razón: Balance tamaño/calidad
     • ~1.2M imágenes, ~150GB
   
   COCO (Common Objects in Context):
     • Formato: JPEG + JSON (anotaciones)
     • Metadatos: bounding boxes, segmentations, captions
   
   CIFAR-10/100:
     • Formato: Binario custom (eficiencia)
     • 32x32 RGB, empaquetado

2. PREPROCESAMIENTO:
   
   • Leer JPEG → NumPy array
   • Redimensionar (resize)
   • Normalizar [0,255] → [0,1] o [-1,1]
   • Data augmentation: flip, rotate, crop
   • Guardar en formato eficiente (HDF5, LMDB)

3. FORMATOS PARA DEEP LEARNING:
   
   HDF5 (.h5):
     • Datasets grandes que no caben en RAM
     • Acceso aleatorio rápido
     • Usado por Keras, PyTorch
   
   LMDB (Lightning Memory-Mapped Database):
     • Muy rápido para lectura
     • Usado en Caffe
   
   TFRecord (TensorFlow):
     • Formato nativo TensorFlow
     • Serialización eficiente
   
   WebDataset:
     • TAR + subdirectorios
     • Streaming para datasets enormes

📹 VIDEO ANALYSIS:

4. EXTRACCIÓN DE FRAMES:
   
   FFmpeg command:
   $ ffmpeg -i video.mp4 -vf fps=1 frame_%04d.jpg
   
   Extrae 1 frame por segundo como JPEG

5. ACTION RECOGNITION:
   
   • Videos cortos (2-10 segundos)
   • Formato: MP4 (H.264)
   • Dataset: Kinetics, UCF-101
   • Preprocesamiento: clips de frames consecutivos

6. OBJECT TRACKING:
   
   • Video + bounding boxes por frame
   • Formato: MP4 + JSON/XML anotaciones
   • Dataset: MOT Challenge

🔬 ANÁLISIS DE METADATOS:

7. ANÁLISIS GEO-ESPACIAL:
   
   • Extraer GPS de EXIF
   • Mapear ubicaciones de fotos
   • Clustering espacial
   • Uso: social media analysis, turismo

8. ANÁLISIS TEMPORAL:
   
   • Timestamp de EXIF
   • Análisis de patrones temporales
   • Uso: vida silvestre (cámaras trampa)

9. FORENSE DIGITAL:
   
   • Verificar autenticidad
   • Detectar manipulación
   • Metadatos de cámara
   • Uso: investigación, periodismo

💾 ALMACENAMIENTO EFICIENTE:

10. CLOUD STORAGE:
    
    S3/GCS/Azure Blob:
      • Originales: JPEG/PNG
      • Thumbnails: WebP (menor tamaño)
      • Metadatos: JSON separado
    
    Estructura recomendada:
    bucket/
      ├── images/
      │   ├── 2025/11/19/
      │   │   ├── img_001.jpg
      │   │   └── img_002.jpg
      ├── thumbnails/
      │   └── 2025/11/19/
      │       ├── img_001_thumb.webp
      │       └── img_002_thumb.webp
      └── metadata/
          └── 2025/11/19/
              └── metadata.jsonl

🎓 MEJORES PRÁCTICAS:

✓ HACER:
  • JPEG para fotografías (Q=85-95 para calidad)
  • PNG para gráficos, logos, transparencias
  • WebP para web moderna (menor tamaño)
  • Extraer y guardar metadatos separadamente
  • Usar formatos eficientes para entrenamiento (HDF5, TFRecord)
  • Mantener versión original sin comprimir (TIFF/PNG)

✗ NO HACER:
  • Recomprimir JPEG múltiples veces (pérdida acumulativa)
  • Usar BMP (sin compresión, archivos enormes)
  • Ignorar EXIF (información valiosa)
  • Mezclar diferentes resoluciones sin documentar
  • Usar PNG para fotografías (archivos muy grandes)

🐍 LIBRERÍAS PYTHON RECOMENDADAS:

Imagen:
  • Pillow (PIL): Básico, universal
  • OpenCV: Computer vision
  • scikit-image: Procesamiento científico
  • imageio: Lectura/escritura múltiples formatos

Video:
  • OpenCV: Básico
  • moviepy: Edición simple
  • ffmpeg-python: Wrapper de FFmpeg
  • PyAV: Binding directo a libav

Metadatos:
  • ExifRead: EXIF de imágenes
  • mutagen: Metadatos de audio/video
  • pymediainfo: Wrapper de MediaInfo
""")


def ejemplo_codigo_practico():
    """
    Ejemplos de código para casos comunes
    """
    print(f"\n{'='*70}")
    print("EJEMPLOS DE CÓDIGO PRÁCTICO")
    print('='*70)
    
    print("""
📝 1. EXTRAER METADATOS DE IMAGEN:

from PIL import Image
from PIL.ExifTags import TAGS
import json

def extraer_exif(imagen_path):
    img = Image.open(imagen_path)
    exif = {}
    
    if hasattr(img, '_getexif') and img._getexif():
        for tag_id, value in img._getexif().items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = str(value)
    
    return {
        'dimensiones': img.size,
        'formato': img.format,
        'modo': img.mode,
        'exif': exif
    }

metadata = extraer_exif('foto.jpg')
print(json.dumps(metadata, indent=2))


📝 2. REDIMENSIONAR Y OPTIMIZAR BATCH:

from PIL import Image
from pathlib import Path

def optimizar_imagenes(input_dir, output_dir, max_size=1920):
    Path(output_dir).mkdir(exist_ok=True)
    
    for img_path in Path(input_dir).glob('*.jpg'):
        img = Image.open(img_path)
        
        # Redimensionar manteniendo aspect ratio
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Guardar optimizado
        output_path = Path(output_dir) / img_path.name
        img.save(output_path, 'JPEG', quality=85, optimize=True)
        
        print(f"✓ {img_path.name}: {img_path.stat().st_size} → "
              f"{output_path.stat().st_size} bytes")

optimizar_imagenes('originales/', 'optimizadas/')


📝 3. CONVERTIR VIDEO A FRAMES (OpenCV):

import cv2
from pathlib import Path

def video_a_frames(video_path, output_dir, fps_target=1):
    Path(output_dir).mkdir(exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    fps_original = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps_original / fps_target)
    
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            output_path = Path(output_dir) / f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(str(output_path), frame, 
                       [cv2.IMWRITE_JPEG_QUALITY, 95])
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"✓ Extraídos {saved_count} frames de {frame_count} totales")

video_a_frames('video.mp4', 'frames/', fps_target=1)


📝 4. BATCH ANALYSIS DE DATASET:

from PIL import Image
import pandas as pd
from pathlib import Path

def analizar_dataset_imagenes(dataset_dir):
    datos = []
    
    for img_path in Path(dataset_dir).rglob('*.jpg'):
        try:
            img = Image.open(img_path)
            datos.append({
                'archivo': img_path.name,
                'clase': img_path.parent.name,
                'ancho': img.width,
                'alto': img.height,
                'aspect_ratio': img.width / img.height,
                'megapixeles': (img.width * img.height) / 1_000_000,
                'tamaño_bytes': img_path.stat().st_size,
                'modo': img.mode
            })
        except Exception as e:
            print(f"Error en {img_path}: {e}")
    
    df = pd.DataFrame(datos)
    
    print("\\n📊 ESTADÍSTICAS DEL DATASET:")
    print(f"Total imágenes: {len(df)}")
    print(f"\\nDimensiones:")
    print(df[['ancho', 'alto']].describe())
    print(f"\\nDistribución por clase:")
    print(df['clase'].value_counts())
    
    return df

df = analizar_dataset_imagenes('dataset/')
df.to_csv('analisis_dataset.csv', index=False)


📝 5. CREAR DATASET PARA DEEP LEARNING (HDF5):

import h5py
import numpy as np
from PIL import Image
from pathlib import Path

def crear_hdf5_dataset(img_dir, output_hdf5, target_size=(224, 224)):
    img_paths = list(Path(img_dir).glob('*.jpg'))
    num_images = len(img_paths)
    
    with h5py.File(output_hdf5, 'w') as f:
        # Crear datasets
        images = f.create_dataset('images', 
                                  shape=(num_images, *target_size, 3),
                                  dtype='uint8')
        labels = f.create_dataset('labels',
                                  shape=(num_images,),
                                  dtype='int')
        filenames = f.create_dataset('filenames',
                                     shape=(num_images,),
                                     dtype=h5py.string_dtype())
        
        # Llenar datasets
        for i, img_path in enumerate(img_paths):
            img = Image.open(img_path).resize(target_size)
            images[i] = np.array(img)
            labels[i] = 0  # Reemplazar con label real
            filenames[i] = img_path.name
            
            if i % 100 == 0:
                print(f"Procesadas {i}/{num_images} imágenes")
    
    print(f"✓ Dataset guardado en {output_hdf5}")

crear_hdf5_dataset('imagenes/', 'dataset.h5')


📝 6. STREAMING DE VIDEO ANALYSIS:

import cv2

def analizar_video_streaming(video_path):
    cap = cv2.VideoCapture(video_path)
    
    # Metadatos
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps
    
    print(f"📹 Video: {video_path}")
    print(f"   Resolución: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Frames: {frame_count}")
    print(f"   Duración: {duration:.2f} segundos")
    
    # Procesar frame por frame (streaming)
    brightness_values = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calcular brightness promedio del frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()
        brightness_values.append(brightness)
    
    cap.release()
    
    print(f"   Brightness promedio: {np.mean(brightness_values):.2f}")
    print(f"   Brightness std: {np.std(brightness_values):.2f}")

analizar_video_streaming('video.mp4')
""")


if __name__ == "__main__":
    print("="*70)
    print("EJEMPLOS PRÁCTICOS: FORMATOS CONTENEDORES")
    print("IMAGEN Y VIDEO")
    print("="*70)
    
    # Crear imágenes de ejemplo
    crear_imagen_ejemplo()
    
    # Analizar formatos de imagen
    analizar_imagen_metadata()
    
    # Analizar imágenes creadas
    print(f"\n{'='*70}")
    print("ANÁLISIS DETALLADO DE IMÁGENES DE EJEMPLO")
    print('='*70)
    
    for imagen in Path('imagenes_ejemplo').glob('*'):
        if imagen.suffix in ['.png', '.jpg', '.gif']:
            metadata = analizar_imagen_detallado(str(imagen))
            print(f"\n📄 {metadata['archivo']['nombre']}")
            print(f"   Formato: {metadata['imagen']['formato']}")
            print(f"   Dimensiones: {metadata['imagen']['ancho']}x{metadata['imagen']['alto']}")
            print(f"   Modo: {metadata['imagen']['modo']} ({metadata['profundidad']['modo_descripcion']})")
            print(f"   Tamaño archivo: {metadata['archivo']['tamaño_bytes']} bytes")
            print(f"   Megapíxeles: {metadata['imagen']['megapixeles']}")
    
    # Comparar tamaños
    comparar_tamaños_compresion()
    
    # Formatos de video
    analizar_formato_video()
    
    # Estructura MP4
    estructura_mp4()
    
    # Casos de uso
    casos_uso_vision()
    
    # Ejemplos de código
    ejemplo_codigo_practico()
    
    print("\n" + "="*70)
    print("✓ Demostración completada")
    print("="*70)
    
    print("\n📚 Para instalar librerías necesarias:")
    print("   pip install Pillow opencv-python h5py pandas")
    print("\n📚 Para análisis avanzado de video:")
    print("   # Instalar FFmpeg primero")
    print("   pip install ffmpeg-python pymediainfo")
