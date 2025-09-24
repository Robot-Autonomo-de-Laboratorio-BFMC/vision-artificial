import torch
import os

# Pedir path por consola
img_path = input("Ingresá el path del archivo de imagen o video (puede ser una URL o path local): ")

# (Opcional) Verificar si el archivo existe si no es URL
if not (img_path.startswith("http://") or img_path.startswith("https://")) and not os.path.exists(img_path):
    print(f"El archivo '{img_path}' no existe.")
    exit(1)

# Cargar el modelo YOLOv5 (puede cambiar a yolov5n, yolov5m, etc.)
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# Realizar inferencia
results = model(img_path)

# Mostrar y guardar resultados
results.print()
results.show()   # Mostrar ventana con resultados
results.save()   # Guardar resultados en runs/detect/exp

