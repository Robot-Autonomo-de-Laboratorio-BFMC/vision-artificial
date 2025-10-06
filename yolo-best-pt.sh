#!/bin/bash
set -e

# Imagen para Jetson con JetPack 6
IMG="ultralytics/ultralytics:latest-jetson-jetpack6"

# Ruta al modelo best.pt
MODEL_PATH="predict/deteccion-en-tiempo-real/weights/merged/best.pt"
MODEL_NAME="best"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que el modelo existe
if [ ! -f "$MODEL_PATH" ]; then
    print_error "No se encontró el modelo en: $MODEL_PATH"
    print_info "Asegúrate de ejecutar este script desde el directorio vision-artificial"
    exit 1
fi

print_success "Modelo encontrado: $MODEL_PATH"

# 1) Preparar host para X11
print_info "Preparando X11 para GUI..."
xhost +local:docker || true

# 2) Traer imagen
print_info "Descargando imagen Docker: $IMG"
sudo docker pull "$IMG"
print_success "Imagen descargada"

# 3) Correr el contenedor y ejecutar TODO adentro en un solo bash -c
print_info "Iniciando contenedor con GPU y GUI..."
print_info "Presiona Ctrl+C para detener la detección"

sudo docker run -it --rm --ipc=host \
  --runtime=nvidia --gpus all \
  --device=/dev/video0:/dev/video0 \
  --device=/dev/dri:/dev/dri \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e QT_QPA_PLATFORM=xcb \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/$USER:/home/$USER \
  "$IMG" bash -c '
    set -e
    echo "🚀 Configurando entorno dentro del contenedor..."
    
    # A) Librerías GUI para OpenCV + X11
    echo "📦 Instalando librerías GUI..."
    apt-get update && apt-get install -y \
      python3-opencv \
      libgtk-3-0 libgl1 libglib2.0-0 \
      libqt5x11extras5 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
      libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxkbcommon-x11-0 \
      x11-xserver-utils

    # B) Si quedó instalado el OpenCV "headless", reemplazarlo por uno con GUI
    echo "🔧 Configurando OpenCV para GUI..."
    pip uninstall -y opencv-python-headless opencv-contrib-python-headless || true

    # C) Sanity check GUI
    echo "🧪 Verificando OpenCV GUI..."
    python3 - <<PY
import cv2, numpy as np
print("OpenCV:", cv2.__version__)
print("GTK in build info?", "GTK" in cv2.getBuildInformation())
img=np.zeros((180,360,3),np.uint8)
cv2.putText(img,"OpenCV GUI OK",(10,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
cv2.imshow("test", img); cv2.waitKey(300); cv2.destroyAllWindows()
print("✅ OpenCV GUI funcionando correctamente")
PY

    # D) Navegar al directorio del modelo
    echo "📁 Navegando al directorio del modelo..."
    cd /home/'$USER'/projects/universidad/bfmc/Robot-Autonomo-de-Laboratorio-BFMC/vision-artificial
    
    # E) Verificar que el modelo existe
    if [ ! -f "'$MODEL_PATH'" ]; then
        echo "❌ Error: No se encontró el modelo en '$MODEL_PATH'"
        echo "💡 Asegúrate de que el archivo best.pt esté en la ubicación correcta"
        exit 1
    fi
    
    echo "✅ Modelo encontrado: '$MODEL_PATH'"
    
    # F) Exportar a TensorRT para mejor rendimiento en Jetson (opcional)
    echo "⚡ Exportando modelo a TensorRT para optimización..."
    ENGINE_PATH="'$MODEL_NAME'.engine"
    if [ ! -f "$ENGINE_PATH" ]; then
        echo "🔄 Convirtiendo '$MODEL_PATH' a TensorRT..."
        yolo export model='$MODEL_PATH' format=engine
        echo "✅ Modelo exportado a TensorRT: $ENGINE_PATH"
    else
        echo "✅ Modelo TensorRT ya existe: $ENGINE_PATH"
    fi
    
    # G) Ejecutar predicción desde cámara
    echo "🎥 Iniciando detección en tiempo real..."
    echo "📋 Presiona Ctrl+C para detener"
    echo "📊 Usando modelo: $ENGINE_PATH"
    echo "📷 Fuente: cámara web (/dev/video0)"
    
    # Usar el modelo TensorRT si existe, sino usar el .pt original
    if [ -f "$ENGINE_PATH" ]; then
        MODEL_TO_USE="$ENGINE_PATH"
    else
        MODEL_TO_USE="'$MODEL_PATH'"
    fi
    
    yolo predict model="$MODEL_TO_USE" source=0 show=True save=False verbose=True
  '

print_success "Contenedor finalizado"
