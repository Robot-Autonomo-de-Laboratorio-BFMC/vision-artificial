#!/usr/bin/env python3
"""
Script minimalista para detección YOLO - SOLO GPU y detección.
Sin ventanas, sin cálculos adicionales, máximo rendimiento.
Usa el modelo: weights/merged/best.pt
"""

import os
import cv2
import torch
from pathlib import Path
from ultralytics import YOLO
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import detect_os


def detectar_y_configurar_gpu():
    """Detecta GPU y configura para máximo rendimiento"""
    if torch.cuda.is_available():
        device = "cuda"
        torch.backends.cudnn.benchmark = True
        return device
    return "cpu"


def cargar_modelo(model_path, device):
    """Carga el modelo YOLO, priorizando engine si existe"""
    if not os.path.exists(model_path):
        print(f"❌ Modelo no encontrado: {model_path}")
        return None
    
    engine_path = model_path.replace('.pt', '.engine')
    
    # Priorizar engine si existe
    if os.path.exists(engine_path):
        model = YOLO(engine_path, task='detect')
        if device == "cuda":
            model.to(device)
        return model
    
    # Cargar .pt y exportar a engine si hay GPU
    model = YOLO(model_path, task='detect')
    if device == "cuda":
        model.to(device)
        if not os.path.exists(engine_path):
            try:
                model.export(format='engine')
                if os.path.exists(engine_path):
                    model = YOLO(engine_path, task='detect')
                    model.to(device)
            except:
                pass  # Continuar con .pt si falla exportación
    
    return model


def obtener_camera_path():
    """Obtiene el path de la cámara"""
    os_detected = detect_os()
    return "/dev/video0" if (os_detected == "wsl" or os_detected == "linux") else 0


def procesar_camara(model, device):
    """Procesa video desde la cámara web - SOLO DETECCIÓN, sin cálculos adicionales"""
    camera_path = obtener_camera_path()
    
    print("📹 Iniciando detección (modo minimalista GPU)... (Presiona Ctrl+C para salir)")
    print(f"📷 Cámara: {camera_path}")
    print(f"🚀 Dispositivo: {device}")
    
    # Abrir cámara
    cap = cv2.VideoCapture(camera_path)
    
    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara.")
        return
    
    # Configuración mínima de cámara
    if isinstance(camera_path, str) and "/dev/video" in camera_path:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("🎥 Iniciando detección...")
    print("-" * 80)
    
    frame_count = 0
    confidence_threshold = 0.6
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # SOLO DETECCIÓN - Inferencia en GPU
            results = model(frame, verbose=False, device=device)[0]
            
            # Procesar solo detecciones básicas (mínimo procesamiento CPU)
            if results.boxes is not None and len(results.boxes) > 0:
                boxes = results.boxes
                for i in range(len(boxes)):
                    confidence = float(boxes.conf[i])
                    if confidence >= confidence_threshold:
                        # Solo obtener coordenadas directamente (mínimo procesamiento)
                        box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                        cls = int(boxes.cls[i])
                        class_name = model.names[cls]
                        
                        # Imprimir directamente sin cálculos adicionales
                        print(f"Frame {frame_count}: {class_name} {confidence:.2%} [{box[0]:.1f},{box[1]:.1f},{box[2]:.1f},{box[3]:.1f}]")
            
    except KeyboardInterrupt:
        print("\n⏹️  Deteniendo...")
    finally:
        cap.release()
        print("✅ Finalizado.")


def main():
    """Función principal - modo minimalista"""
    script_dir = Path(__file__).parent
    model_path = script_dir.parent / "weights" / "merged" / "best.pt"
    
    # Configurar GPU
    device = detectar_y_configurar_gpu()
    
    # Cargar modelo
    model = cargar_modelo(str(model_path), device)
    if model is None:
        return
    
    # Iniciar detección
    procesar_camara(model, device)


if __name__ == "__main__":
    main()

