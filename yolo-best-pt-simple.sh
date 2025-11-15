#!/bin/bash
set -e

# Script simplificado para ejecutar YOLO con best.pt en Docker
# Basado en yolobase-fixed.sh

# Configuración
IMG="ultralytics/ultralytics:latest-jetson-jetpack6"
MODEL_PATH="predict/deteccion-en-tiempo-real/weights/merged/best.pt"

echo "🚀 Iniciando YOLO con modelo best.pt..."
echo "📁 Modelo: $MODEL_PATH"

# Verificar que el modelo existe
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Error: No se encontró el modelo en $MODEL_PATH"
    echo "💡 Ejecuta este script desde el directorio vision-artificial"
    exit 1
fi

echo "✅ Modelo encontrado"

# Obtener directorio actual del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📂 Directorio del proyecto: $PROJECT_DIR"

# Preparar X11 y descargar imagen
xhost +local:docker || true
sudo docker pull "$IMG"

# Ejecutar contenedor
echo "🎥 Iniciando detección en tiempo real... Este proceso puede tardar unos minutos..."
echo "📋 Presiona Ctrl+C para detener"

sudo docker run -it --rm --ipc=host \
  --runtime=nvidia --gpus all \
  --device=/dev/video0:/dev/video0 \
  --device=/dev/dri:/dev/dri \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e QT_QPA_PLATFORM=xcb \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "$PROJECT_DIR:/workspace" \
  -w /workspace \
  "$IMG" bash -c '
    # Instalar dependencias GUI
    apt-get update -qq && apt-get install -y -qq \
      python3-opencv libgtk-3-0 libgl1 libglib2.0-0 \
      libqt5x11extras5 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
      libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxkbcommon-x11-0 \
      x11-xserver-utils
    
    # Remover OpenCV headless
    pip uninstall -y opencv-python-headless opencv-contrib-python-headless || true
    
    # Verificar que estamos en el directorio correcto
    echo "📁 Directorio de trabajo: $(pwd)"
    
    # Verificar modelo
    if [ ! -f '$MODEL_PATH' ]; then
        echo "❌ Modelo no encontrado: '$MODEL_PATH'"
        echo "💡 Archivos en el directorio actual:"
        ls -la
        exit 1
    fi
    
    echo "✅ Modelo encontrado en el contenedor"
    echo "🎮 Usando GPU para aceleración"
    echo "📷 Fuente: cámara web"
    echo "🤖 Modelo: '$MODEL_PATH'"
    
    # Ejecutar YOLO
    yolo predict model='$MODEL_PATH' source=0 show=True save=False
  '

echo "✅ Finalizado"
