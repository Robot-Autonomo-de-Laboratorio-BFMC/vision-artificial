# 🤖 Detector de Objetos en Tiempo Real

Sistema de detección de objetos en **tiempo real** usando cámara web con modelo local YOLO.

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar modelo local

El sistema usa el modelo `best.pt` ubicado en `weights/merged/`. Asegúrate de que el archivo existe.

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

Edita la línea 44 en `detection.py`:

```python
confidence_threshold = 0.6  # 60% - Cambia este valor
```

### Configuración para WSL:

La aplicación detecta automáticamente si estás en WSL y aplica configuraciones optimizadas para cámaras USB.

## 📝 Notas importantes

- **Modelo local**: No requiere internet después de la instalación
- **Cámara**: Asegúrate de que tu cámara esté conectada y disponible
- **WSL**: Optimizado para funcionar con cámaras USB en WSL
- **GPU**: Para mejor rendimiento, instala PyTorch con soporte GPU
- **Confianza**: Solo se muestran detecciones con confianza > 60%

## 🆘 Solución de problemas

### Error: "No se encontró el modelo"

- Verifica que `best.pt` esté en `weights/merged/`
- El archivo debe tener aproximadamente 50MB

### Error: "No se pudo abrir la cámara"

- Verifica que tu cámara esté conectada
- Cierra otras aplicaciones que usen la cámara
- En WSL: Verifica que la cámara esté disponible en `/dev/video*`

### Problemas específicos de WSL:

- **Timeout de cámara**: La aplicación incluye configuraciones específicas para WSL
- **Dispositivos USB**: Verifica que WSL tenga acceso a dispositivos USB
- **Permisos**: Asegúrate de estar en el grupo `video`

## 🎯 Características

- ✅ **Detección en tiempo real** con cámara web
- ✅ **Modelo local** - No requiere internet
- ✅ **Filtro de confianza** - Solo detecciones > 60%
- ✅ **Optimizado para WSL** con configuraciones específicas
- ✅ **Visualización clara** con cajas y etiquetas
- ✅ **Manejo de errores** robusto
- ✅ **Sin dependencias externas** - Todo local

## 🤝 Soporte

Si tienes problemas:

1. Verifica que seguiste todos los pasos de instalación
2. Comprueba que el archivo `best.pt` existe
3. Para WSL: Verifica que la cámara esté disponible en `/dev/video*`
