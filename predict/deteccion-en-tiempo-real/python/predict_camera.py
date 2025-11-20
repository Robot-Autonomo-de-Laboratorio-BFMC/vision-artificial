#!/usr/bin/env python3
"""
Script para ejecutar detección YOLO desde cámara y mostrar objetos detectados con sus posiciones.
Usa el modelo entrenado: weights/merged/best.pt
"""

import os
import sys
import cv2
import torch
from pathlib import Path
from ultralytics import YOLO

# Agregar el directorio padre al path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import choose_camera_by_OS, detect_os


def detectar_y_configurar_gpu():
    """Detecta automáticamente si hay GPU disponible y la configura"""
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        print(f"🎮 GPU detectada: {gpu_name}")
        print("⚡ Usando GPU para aceleración")
        torch.backends.cudnn.benchmark = True
        return device, True
    else:
        print("💻 GPU no disponible, usando CPU")
        return "cpu", False


def cargar_modelo(model_path, device):
    """Carga el modelo YOLO, exportando a engine si es necesario"""
    # Verificar si existe el archivo .pt
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encontró el modelo en {model_path}")
        print("💡 Asegúrate de que el archivo best.pt esté en weights/merged/")
        return None
    
    # Verificar si existe el archivo .engine
    engine_path = model_path.replace('.pt', '.engine')
    
    if os.path.exists(engine_path):
        print(f"✅ Engine file encontrado: {engine_path}")
        print("📦 Usando modelo TensorRT optimizado")
        try:
            model = YOLO(engine_path)
            if device == "cuda":
                model.to(device)
            return model
        except Exception as e:
            print(f"⚠️  Error al cargar engine, intentando con .pt: {e}")
    
    # Si no existe engine o falló, usar .pt y exportar si es necesario
    print(f"📋 Cargando modelo: {model_path}")
    try:
        model = YOLO(model_path)
        if device == "cuda":
            model.to(device)
        
        # Exportar a engine si estamos en Jetson/CUDA
        if device == "cuda" and not os.path.exists(engine_path):
            print("⚡ Exportando modelo a TensorRT para aceleración GPU...")
            print("📦 Esto puede tardar unos minutos la primera vez...")
            try:
                model.export(format='engine')
                print("✅ Exportación completada")
                # Recargar el modelo engine
                if os.path.exists(engine_path):
                    model = YOLO(engine_path)
                    if device == "cuda":
                        model.to(device)
            except Exception as e:
                print(f"⚠️  No se pudo exportar a engine: {e}")
                print("📋 Continuando con modelo .pt")
        
        return model
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return None


def procesar_camara(model, device):
    """Procesa video desde la cámara web y muestra detecciones con posiciones"""
    os_detected = detect_os()
    camera_path = choose_camera_by_OS()
    
    print("📹 Iniciando cámara web... (Presiona Ctrl+C para salir)")
    print(f"🔍 Sistema operativo detectado: {os_detected}")
    print(f"📷 Usando path de cámara: {camera_path}")
    print(f"🚀 Dispositivo de inferencia: {device}")
    
    cap = cv2.VideoCapture(camera_path)
    
    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara.")
        return
    
    # Configurar cámara si es Linux/WSL
    if isinstance(camera_path, str) and "/dev/video" in camera_path:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"📷 Cámara configurada: {width}x{height} @ 30fps (MJPG)")
    
    print("🎥 Cámara iniciada.")
    print("📊 Umbral de confianza: 60%")
    print("-" * 80)
    
    frame_count = 0
    confidence_threshold = 0.6
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error al capturar frame de la cámara.")
                break
            
            frame_count += 1
            
            # Realizar inferencia
            results = model(frame, verbose=False, device=device)[0]
            
            # Procesar detecciones
            detections = []
            if results.boxes is not None and len(results.boxes) > 0:
                boxes = results.boxes
                for i in range(len(boxes)):
                    confidence = float(boxes.conf[i])
                    if confidence >= confidence_threshold:
                        # Obtener coordenadas del bounding box
                        box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                        x1, y1, x2, y2 = box
                        
                        # Obtener clase
                        cls = int(boxes.cls[i])
                        class_name = model.names[cls]
                        
                        # Calcular centro y dimensiones
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        width = x2 - x1
                        height = y2 - y1
                        
                        detections.append({
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': {
                                'x1': float(x1),
                                'y1': float(y1),
                                'x2': float(x2),
                                'y2': float(y2),
                                'center': (float(center_x), float(center_y)),
                                'width': float(width),
                                'height': float(height)
                            }
                        })
            
            # Imprimir detecciones
            if detections:
                print(f"\n📸 Frame {frame_count}: {len(detections)} objeto(s) detectado(s)")
                for idx, det in enumerate(detections, 1):
                    bbox = det['bbox']
                    print(f"  [{idx}] {det['class']} (confianza: {det['confidence']:.2%})")
                    print(f"      Posición: ({bbox['x1']:.1f}, {bbox['y1']:.1f}) -> ({bbox['x2']:.1f}, {bbox['y2']:.1f})")
                    print(f"      Centro: ({bbox['center'][0]:.1f}, {bbox['center'][1]:.1f})")
                    print(f"      Tamaño: {bbox['width']:.1f} x {bbox['height']:.1f} px")
            else:
                # Solo mostrar cada 30 frames si no hay detecciones para no saturar la salida
                if frame_count % 30 == 0:
                    print(f"📸 Frame {frame_count}: Sin detecciones")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo detección...")
    finally:
        cap.release()
        print("✅ Cámara cerrada.")


def main():
    """Función principal"""
    # Obtener ruta del modelo relativa al directorio del script
    script_dir = Path(__file__).parent
    model_path = script_dir.parent / "weights" / "merged" / "best.pt"
    
    print("=" * 80)
    print("    DETECTOR DE OBJETOS EN TIEMPO REAL - SALIDA CONSOLA")
    print("=" * 80)
    print(f"📁 Directorio del script: {script_dir}")
    print(f"📋 Modelo: {model_path}")
    
    # Detectar y configurar GPU
    device, use_gpu = detectar_y_configurar_gpu()
    
    # Cargar modelo
    print("\n🤖 Cargando modelo...")
    model = cargar_modelo(str(model_path), device)
    
    if model is None:
        print("❌ No se pudo cargar el modelo. Saliendo...")
        return
    
    print("✅ Modelo cargado exitosamente!")
    
    if use_gpu:
        print("🚀 Modelo movido a GPU")
    
    print("\n" + "=" * 80)
    print("🎥 Iniciando detección con cámara...")
    print("📋 Presiona Ctrl+C para detener")
    print("=" * 80 + "\n")
    
    # Iniciar detección
    procesar_camara(model, device)
    
    print("\n👋 ¡Hasta luego!")


if __name__ == "__main__":
    main()

