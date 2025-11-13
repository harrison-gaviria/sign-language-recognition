# Sign Language Recognition

Un sistema de reconocimiento de lenguaje de señas en tiempo real utilizando visión por computadora e inteligencia artificial basado en YOLOv11.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Teoría: ¿Qué es YOLO?](#teoría-qué-es-yolo)
- [Dataset](#dataset)
- [Modelo Utilizado](#modelo-utilizado)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
  - [Entrenamiento del Modelo](#entrenamiento-del-modelo)
  - [Ejecución en Tiempo Real](#ejecución-en-tiempo-real)
- [Características del Sistema](#características-del-sistema)
- [Resultados](#resultados)
- [Licencia](#licencia)

## Descripción

Este proyecto implementa un sistema de reconocimiento de lenguaje de señas americano (ASL) en tiempo real. Utiliza el modelo YOLOv11 para detectar y clasificar gestos de manos que representan letras del alfabeto en lenguaje de señas, permitiendo la comunicación visual mediante el reconocimiento de señas capturadas por la cámara web.

## Teoría: ¿Qué es YOLO?

**YOLO (You Only Look Once)** es una arquitectura de red neuronal convolucional diseñada para la detección de objetos en tiempo real. A diferencia de otros métodos de detección que requieren múltiples pasadas por la imagen, YOLO:

- **Procesa la imagen completa en una sola pasada**, dividiendo la imagen en una cuadrícula y prediciendo simultáneamente las cajas delimitadoras y las probabilidades de clase para cada región.
- **Es extremadamente rápido**, lo que lo hace ideal para aplicaciones en tiempo real como este proyecto.
- **Detecta y clasifica objetos simultáneamente**, proporcionando tanto la ubicación como la identidad de los objetos detectados.

### ¿Por qué YOLOv11?

YOLOv11 es la versión más reciente de la familia YOLO, optimizada para:
- Mayor precisión en detección de objetos pequeños
- Velocidad de inferencia mejorada
- Mejor balance entre precisión y rendimiento
- Facilidad de entrenamiento y despliegue

## Dataset

El proyecto utiliza el dataset **American Sign Language Letters** proporcionado por Roboflow:

- **Fuente**: [American Sign Language Letters Dataset](https://universe.roboflow.com/duyguj/american-sign-language-letters-vouo0/dataset/1)
- **Formato**: YOLOv11 compatible
- **Contenido**: Imágenes etiquetadas de gestos de manos representando las letras del alfabeto americano en lenguaje de señas
- **Características**:
  - Dataset pre-anotado y listo para entrenar
  - Formato de anotaciones compatible con YOLO
  - Incluye archivo `data.yaml` con configuración del dataset

El dataset se descargó directamente desde Roboflow en formato YOLOv11, lo que facilita su integración inmediata con Ultralytics.

## Modelo Utilizado

Este proyecto utiliza **YOLO11n** (nano), la versión más ligera y rápida de YOLOv11:

| Modelo | Tamaño (píxeles) | mAP<sup>val</sup> 50-95 | Velocidad CPU ONNX (ms) | Velocidad T4 TensorRT10 (ms) | Parámetros (M) | FLOPs (B) |
|--------|------------------|-------------------------|-------------------------|------------------------------|----------------|-----------|
| YOLO11n | 640 | 39.5 | 56.1 ± 0.8 | 1.5 ± 0.0 | 2.6 | 6.5 |

### ¿Por qué YOLO11n?

- **Ligero**: Solo 2.6M de parámetros, ideal para aplicaciones en tiempo real
- **Rápido**: Inferencia en ~1.5ms en GPU T4
- **Eficiente**: Bajo consumo de recursos computacionales
- **Preciso**: mAP de 39.5% es suficiente para detección de gestos de manos

## Requisitos

- Python 3.8 o superior
- Cámara web
- GPU (recomendado para entrenamiento, opcional para inferencia)

### Dependencias

```bash
ultralytics>=8.3.228
opencv-python>=4.12.0.88
```

## Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/harrison-gaviria/sign-language-recognition.git
cd sign-language-recognition
```

2. **Crear entorno virtual (recomendado)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Descargar el dataset**

El dataset ya está incluido en el repositorio como `American Sign Language Letters.v1i.yolov11.zip`. Si necesitas descargarlo nuevamente:

```bash
# Descomprimir el dataset
unzip "American Sign Language Letters.v1i.yolov11.zip"
```

5. **Descargar modelo pre-entrenado (opcional)**

El modelo base YOLO11n ya está incluido (`yolo11n.pt`). Si necesitas descargarlo:

```python
from ultralytics import YOLO
model = YOLO("yolo11n.pt")  # Se descargará automáticamente si no existe
```

## Estructura del Proyecto

```
sign-language-recognition/
├── American Sign Language Letters.v1i.yolov11/
│   ├── train/              # Imágenes de entrenamiento
│   ├── valid/              # Imágenes de validación
│   ├── test/               # Imágenes de prueba
│   └── data.yaml           # Configuración del dataset
├── runs/
│   └── detect/
│       └── train2/
│           └── weights/
│               └── best.pt # Modelo entrenado (mejor resultado)
├── yolo11n.pt              # Modelo base YOLO11n
├── sign_language_recognition.py  # Script principal
├── .gitignore
├── LICENSE
└── README.md
```

## Uso

### Entrenamiento del Modelo

**NOTA IMPORTANTE**: El código de entrenamiento está comentado en el archivo `sign_language_recognition.py` para evitar entrenamientos accidentales, ya que el modelo ya ha sido entrenado y los pesos están guardados en `runs/detect/train2/weights/best.pt`.

Si deseas **re-entrenar el modelo desde cero**, descomenta las siguientes líneas en `sign_language_recognition.py`:

```python
from ultralytics import YOLO
model = YOLO("yolo11n.pt")
model.train(data="./American Sign Language Letters.v1i.yolov11/data.yaml", epochs=10, imgsz=640)
```

#### Parámetros de Entrenamiento

- **`data`**: Ruta al archivo `data.yaml` que contiene la configuración del dataset
- **`epochs=10`**: Número de épocas de entrenamiento (ciclos completos sobre el dataset)
- **`imgsz=640`**: Tamaño de imagen para entrenamiento (640x640 píxeles)

#### Proceso de Entrenamiento

1. Descomenta las líneas de entrenamiento en `sign_language_recognition.py`
2. Ejecuta el script:

```bash
python sign_language_recognition.py
```

3. El entrenamiento comenzará y verás:
   - Progreso de cada época
   - Métricas de precisión (mAP)
   - Pérdidas de entrenamiento y validación

4. Los resultados se guardarán en:
   - `runs/detect/trainX/weights/best.pt` (mejor modelo)
   - `runs/detect/trainX/weights/last.pt` (última época)
   - Gráficas de entrenamiento y métricas

### Ejecución en Tiempo Real

Una vez que el modelo está entrenado (o usando el modelo pre-entrenado incluido), puedes ejecutar el reconocimiento en tiempo real:

1. **Asegúrate de que el código de entrenamiento esté comentado**

2. **Ejecuta el script**:

```bash
python sign_language_recognition.py
```

3. **Uso de la aplicación**:
   - Se abrirá una ventana mostrando el video de tu cámara web
   - Realiza gestos de lenguaje de señas frente a la cámara
   - El sistema detectará y clasificará las letras automáticamente
   - Presiona 'q' para salir


## Características del Sistema

### Reconocimiento Inteligente

El sistema incluye las siguientes funcionalidades:

1. **Detección en Tiempo Real**
   - Procesa el video de la cámara en tiempo real
   - Detección continua de gestos de manos

2. **Sistema de Confianza**
   - **Umbral de confianza**: 0.5 (50%)
   - Solo se registran detecciones con confianza > 50%
   - Reduce falsos positivos

3. **Intervalo de Captura**
   - Captura una letra cada **2 segundos**
   - Evita capturas repetitivas del mismo gesto
   - Permite tiempo para cambiar de letra

4. **Visualización Dual**
   ```python
   letras_reconocidas = []      # Letras con confianza > 50% (verde)
   letras_no_reconocidas = []   # Letras con confianza ≤ 50% (rojo)
   ```

5. **Límite de Historial**
   - Muestra las últimas 10 letras reconocidas
   - Muestra las últimas 10 letras no reconocidas
   - Se reinicia automáticamente al superar el límite

6. **Interfaz Visual**
   - Texto verde: letras reconocidas con alta confianza
   - Texto rojo: letras detectadas con baja confianza
   - Cajas delimitadoras alrededor de las manos detectadas

### Flujo de Trabajo

```
Cámara Web → YOLO11n → Detección → Filtro de Confianza → Clasificación → Visualización
                           ↓
                    Cada 2 segundos
                           ↓
                  Confianza > 0.5?
                    ↙         ↘
              Sí (Verde)    No (Rojo)
```

## Resultados

El modelo entrenado puede:
- Detectar gestos de manos en tiempo real
- Clasificar 26 letras del alfabeto ASL
- Procesar video a ~30 FPS (dependiendo del hardware)
- Funcionar con iluminación variable
- Adaptarse a diferentes tamaños de manos

## Documentación y Referencias

- **Ultralytics YOLOv11 Documentación**: [https://docs.ultralytics.com/es/tasks/detect/](https://docs.ultralytics.com/es/tasks/detect/)
- **Formatos de exportación YOLO11**: [Export Formats](https://docs.ultralytics.com/es/tasks/detect/#what-formats-can-i-export-a-yolo11-model-to)
- **Dataset ASL**: [Roboflow Universe](https://universe.roboflow.com/duyguj/american-sign-language-letters-vouo0/dataset/1)
- **Repositorio del Proyecto**: [GitHub](https://github.com/harrison-gaviria/sign-language-recognition)


## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Tecnologías**: YOLOv11 | Ultralytics | OpenCV | Python