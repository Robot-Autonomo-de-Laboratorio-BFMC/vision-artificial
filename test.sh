#!/bin/sh

t=ultralytics/ultralytics:latest-jetson-jetpack6
sudo docker pull $t

xhost +local:docker

sudo docker run -it --ipc=host \
  --runtime=nvidia \
  --gpus all \
  -v /home/$USER:/home/$USER \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
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
    yolo export model=yolo11n.pt format=engine && \
    yolo predict model=yolo11n.engine source=0 show=True"
