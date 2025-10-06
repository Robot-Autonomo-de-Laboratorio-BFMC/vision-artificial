#!/bin/bash
set -e

# Imagen para Jetson con JetPack 6
IMG="ultralytics/ultralytics:latest-jetson-jetpack6"

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
    # Mostrar en ventana; si preferís sin ventana, poné show=False save=True
    yolo predict model=yolo11n.engine source=0 show=True
  '
