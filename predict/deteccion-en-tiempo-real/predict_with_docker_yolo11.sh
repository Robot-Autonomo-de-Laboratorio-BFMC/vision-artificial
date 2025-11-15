#!/bin/bash
set -e

# Imagen para Jetson con JetPack 6
IMG="ultralytics/ultralytics:latest-jetson-jetpack6"
IMG_SIZE=640  # Resolución de imagen (por defecto 640, más rápido que 720p)

# Función de ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Opciones:"
    echo "  --imgsz SIZE      Especifica el tamaño de imagen (por defecto: 640)"
    echo "                    Valores comunes: 320, 480, 640, 1280"
    echo "                    Menor = más rápido pero menos detalle"
    echo "  -h, --help        Muestra esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0                # Usa resolución 640 (por defecto)"
    echo "  $0 --imgsz 480    # Usa resolución 480 (más rápido)"
    echo "  $0 --imgsz 320    # Usa resolución 320 (muy rápido)"
}

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --imgsz)
            IMG_SIZE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "❌ Opción desconocida: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
done

echo "🖼️  Resolución de imagen: ${IMG_SIZE}x${IMG_SIZE}"

# 1) Preparar host para X11
xhost +local:docker || true

# 2) Traer imagen
sudo docker pull "$IMG"

# 3) Correr el contenedor y ejecutar TODO adentro en un solo bash -c
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
    # A) Librerías GUI para OpenCV + X11
    apt-get update && apt-get install -y \
      python3-opencv \
      libgtk-3-0 libgl1 libglib2.0-0 \
      libqt5x11extras5 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
      libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxkbcommon-x11-0 \
      x11-xserver-utils

    # B) Si quedó instalado el OpenCV "headless", reemplazarlo por uno con GUI
    pip uninstall -y opencv-python-headless opencv-contrib-python-headless || true

    # C) Sanity check GUI
    python3 - <<PY
import cv2, numpy as np
print("OpenCV:", cv2.__version__)
print("GTK in build info?", "GTK" in cv2.getBuildInformation())
img=np.zeros((180,360,3),np.uint8)
cv2.putText(img,"OpenCV GUI OK",(10,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
cv2.imshow("test", img); cv2.waitKey(300); cv2.destroyAllWindows()
PY

    # D) Exportar a TensorRT (si no existe aún) y predecir desde cámara
    test -f yolo11n.engine || yolo export model=yolo11n.pt format=engine
    
    # Configurar resolución de la cámara usando v4l2-ctl
    # Esto reduce la resolución real de captura, no solo el redimensionamiento
    if command -v v4l2-ctl &> /dev/null; then
        echo "⚙️  Configurando resolución de cámara a '$IMG_SIZE'x'$IMG_SIZE'..."
        v4l2-ctl --device=/dev/video0 --set-fmt-video=width='$IMG_SIZE',height='$IMG_SIZE' || echo "⚠️  No se pudo configurar resolución de cámara (continuando de todas formas)"
    else
        echo "⚠️  v4l2-ctl no encontrado, instalando..."
        apt-get install -y -qq v4l-utils || echo "⚠️  No se pudo instalar v4l-utils"
        v4l2-ctl --device=/dev/video0 --set-fmt-video=width='$IMG_SIZE',height='$IMG_SIZE' || echo "⚠️  No se pudo configurar resolución de cámara (continuando de todas formas)"
    fi
    
    # Mostrar en ventana con resolución reducida para mejor rendimiento
    echo "🖼️  Usando resolución: '$IMG_SIZE'x'$IMG_SIZE'"
    yolo predict model=yolo11n.engine source=0 imgsz='$IMG_SIZE' show=True
  '
