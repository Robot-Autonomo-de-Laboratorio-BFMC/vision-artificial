# 🐳 YOLO con Docker y GPU

Scripts para ejecutar detección en tiempo real con YOLO usando Docker y aceleración GPU.

## 📁 Archivos disponibles

### 1. `yolo-best-pt.sh` (Completo)
Script completo con todas las optimizaciones:
- ✅ Configuración automática de GUI
- ✅ Exportación a TensorRT para mejor rendimiento
- ✅ Diagnósticos detallados
- ✅ Manejo de errores robusto

### 2. `yolo-best-pt-simple.sh` (Simplificado)
Script básico y rápido:
- ✅ Configuración mínima
- ✅ Ejecución directa
- ✅ Ideal para pruebas rápidas

### 3. `predict_with_docker_ultralytics_and_cli` (Original)
Script original modificado con volumen para compartir el modelo.

## 🚀 Uso

### Requisitos previos
```bash
# Verificar que Docker está corriendo
sudo docker info

# Verificar que nvidia-docker está instalado
docker info | grep nvidia
```

### Ejecutar detección

**Desde el directorio `vision-artificial`:**

```bash
# Opción 1: Script completo (recomendado)
./yolo-best-pt.sh

# Opción 2: Script simplificado
./yolo-best-pt-simple.sh

# Opción 3: Script original modificado
cd predict/deteccion-en-tiempo-real/
./predict_with_docker_ultralytics_and_cli
```

## 🔧 Configuración

### Variables importantes en los scripts:

```bash
# Imagen Docker (compatible con Jetson)
IMG="ultralytics/ultralytics:latest-jetson-jetpack6"

# Ruta al modelo
MODEL_PATH="predict/deteccion-en-tiempo-real/weights/merged/best.pt"

# Fuente de video
VIDEO_SOURCE="/dev/video0"  # Cámara web
```

### Volúmenes Docker:

```bash
# Compartir directorio del modelo
-v "$(pwd)/weights:/app/weights:ro"

# Compartir todo el home (para acceso completo)
-v /home/$USER:/home/$USER
```

## ⚡ Optimizaciones

### TensorRT (Solo en `yolo-best-pt.sh`)
El script completo exporta automáticamente el modelo a TensorRT para mejor rendimiento en Jetson:

```bash
# Exportación automática
yolo export model=best.pt format=engine
```

### GPU
```bash
# Habilitar GPU
--runtime=nvidia --gpus all

# Dispositivos de video
--device=/dev/video0:/dev/video0
```

## 🎮 GUI y X11

Los scripts configuran automáticamente X11 para mostrar ventanas:

```bash
# Configuración X11
xhost +local:docker
-e DISPLAY=$DISPLAY
-v /tmp/.X11-unix:/tmp/.X11-unix
```

## 🐛 Solución de problemas

### Error: "No se encontró el modelo"
```bash
# Verificar ubicación
ls -la predict/deteccion-en-tiempo-real/weights/merged/best.pt

# Ejecutar desde directorio correcto
cd vision-artificial
./yolo-best-pt.sh
```

### Error: "nvidia-docker no detectado"
```bash
# Instalar nvidia-docker-toolkit
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

### Error: "OpenCV GUI no funciona"
Los scripts instalan automáticamente las dependencias necesarias:
- `python3-opencv`
- `libgtk-3-0`
- Librerías X11

### GPU no se usa
```bash
# Verificar GPU
nvidia-smi

# Verificar en contenedor
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## 📊 Rendimiento

### Comparación de rendimiento:

| Script | Tiempo inicio | GPU | TensorRT | GUI |
|--------|---------------|-----|----------|-----|
| `yolo-best-pt.sh` | ~2-3 min | ✅ | ✅ | ✅ |
| `yolo-best-pt-simple.sh` | ~1-2 min | ✅ | ❌ | ✅ |
| Original modificado | ~30 seg | ✅ | ❌ | ✅ |

### Recomendaciones:
- **Desarrollo**: Usar `yolo-best-pt-simple.sh`
- **Producción**: Usar `yolo-best-pt.sh` (con TensorRT)
- **Pruebas rápidas**: Usar script original modificado

## 🔄 Actualizaciones

Para actualizar la imagen Docker:
```bash
sudo docker pull ultralytics/ultralytics:latest-jetson-jetpack6
```

## 📝 Notas

- Los scripts están optimizados para Jetson con JetPack 6
- Compatible con WSL2 y Linux nativo
- Requiere permisos sudo para Docker
- La primera ejecución tarda más por la instalación de dependencias
