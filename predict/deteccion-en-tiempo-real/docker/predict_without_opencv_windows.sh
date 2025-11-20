#!/bin/sh

t=ultralytics/ultralytics:latest-jetson-jetpack6
sudo docker pull $t

xhost +local:docker

# Obtener directorio del proyecto automáticamente
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

sudo docker run -it --ipc=host \
  --runtime=nvidia \
  --gpus all \
  -v "$PROJECT_ROOT:/workspace" \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -w /workspace/predict/deteccion-en-tiempo-real \
  $t bash -c "\
    apt-get update && apt-get install -y \
      libqt5x11extras5 \
      libxcb-icccm4 \
      libxcb-image0 \
      libxcb-keysyms1 \
      libxcb-randr0 \
      libxcb-render-util0 \
      libxcb-xinerama0 \
      libxkbcommon-x11-0 \
      x11-xserver-utils \
      python3-opencv && \
    ([ -f weights/merged/best.engine ] && echo 'Engine file already exists, skipping export' || yolo export model=weights/merged/best.pt format=engine) && \
    yolo predict model=weights/merged/best.engine source=0 show=False verbose=True"