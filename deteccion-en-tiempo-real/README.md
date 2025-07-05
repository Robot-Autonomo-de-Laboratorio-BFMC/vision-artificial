# 🤖 Detector de Objetos en Tiempo Real

Sistema de detección de objetos en **tiempo real** usando cámara web con modelo local YOLO y soporte automático para GPU.

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar modelo local

El sistema usa el modelo `best.pt` ubicado en `weights/merged/`. Asegúrate de que el archivo existe.

### 3. Soporte GPU (opcional pero recomendado)
Para mejor rendimiento, instala PyTorch con soporte CUDA:
```bash
# Desinstalar versión CPU
pip uninstall torch torchvision

# Instalar versión con CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 🎮 Uso

### Ejecutar el programa:

```bash
cd deteccion-en-tiempo-real
python3 detection.py
```

### Funcionalidad:

- **🎥 Cámara Web** - Detección en tiempo real automática
- **📋 Visualización** - Cajas de detección y etiquetas
- **⚡ Tiempo Real** - Procesamiento continuo de frames
- **📊 Filtro de Confianza** - Solo muestra detecciones > 60%
- **🚀 Aceleración GPU** - Detecta automáticamente si hay GPU disponible
- **📈 Monitor FPS** - Muestra FPS en tiempo real

### Controles:

- **`q`** - Salir de la aplicación

## 📁 Estructura de archivos

```
deteccion-en-tiempo-real/
├── detection.py       # Programa principal
├── config.py          # Configuración de cámara
├── weights/
│   └── merged/
│       └── best.pt    # Modelo local (50MB)
├── requirements.txt   # Dependencias
└── README.md          # Este archivo
```

## 🔧 Configuración

### Cambiar el umbral de confianza:

Edita la línea 67 en `detection.py`:

```python
confidence_threshold = 0.6  # 60% - Cambia este valor
```

### Configuración para WSL:

La aplicación detecta automáticamente si estás en WSL y aplica configuraciones optimizadas para cámaras USB.

### Configuración GPU:
La aplicación detecta automáticamente si hay GPU disponible:
- **GPU NVIDIA**: Se usa automáticamente para aceleración
- **CPU**: Se usa como respaldo si no hay GPU
- **Optimizaciones**: CUDNN benchmark activado automáticamente

## 📝 Notas importantes

- **Modelo local**: No requiere internet después de la instalación
- **Cámara**: Asegúrate de que tu cámara esté conectada y disponible
- **WSL**: Optimizado para funcionar con cámaras USB en WSL
- **GPU**: Detección automática y optimizaciones incluidas
- **Confianza**: Solo se muestran detecciones con confianza > 60%
- **FPS**: Monitor de rendimiento incluido

## 🆘 Solución de problemas

### Error: "No se encontró el modelo"

- Verifica que `best.pt` esté en `weights/merged/`
- El archivo debe tener aproximadamente 50MB

### Error: "No se pudo abrir la cámara"

- Verifica que tu cámara esté conectada
- Cierra otras aplicaciones que usen la cámara
- En WSL: Verifica que la cámara esté disponible en `/dev/video*`

### Error: "ultralytics no está instalado"
```bash
pip install ultralytics
```

### Problemas con GPU:
- **GPU no detectada**: Instala PyTorch con soporte CUDA
- **Error CUDA**: Verifica drivers NVIDIA actualizados
- **Out of memory**: Reduce resolución de cámara o cierra otras apps

### Problemas específicos de WSL:

- **Timeout de cámara**: La aplicación incluye configuraciones específicas para WSL
- **Dispositivos USB**: Verifica que WSL tenga acceso a dispositivos USB
- **Permisos**: Asegúrate de estar en el grupo `video`

## 🎯 Características

- ✅ **Detección en tiempo real** con cámara web
- ✅ **Modelo local** - No requiere internet
- ✅ **Filtro de confianza** - Solo detecciones > 60%
- ✅ **Aceleración GPU automática** - Detecta y usa GPU si está disponible
- ✅ **Monitor FPS** - Rendimiento en tiempo real
- ✅ **Optimizado para WSL** con configuraciones específicas
- ✅ **Visualización clara** con cajas y etiquetas
- ✅ **Manejo de errores** robusto
- ✅ **Sin dependencias externas** - Todo local

## 🚀 Rendimiento

### Con GPU:
- **FPS**: 15-30+ (dependiendo de la GPU)
- **Latencia**: Muy baja
- **Precisión**: Alta

### Con CPU:
- **FPS**: 5-15
- **Latencia**: Media
- **Precisión**: Alta

## 🤝 Soporte

Si tienes problemas:

1. Verifica que seguiste todos los pasos de instalación
2. Comprueba que el archivo `best.pt` existe
3. Para WSL: Verifica que la cámara esté disponible en `/dev/video*`
4. Para GPU: Verifica que PyTorch tenga soporte CUDA
