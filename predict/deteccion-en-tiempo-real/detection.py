import supervision as sv
import cv2
import os
import torch
from ultralytics import YOLO
from config import choose_camera_by_OS, handle_video_capture, detect_os

def detectar_y_configurar_gpu():
    """Detecta automáticamente si hay GPU disponible y la configura"""
    
    # Diagnóstico completo de PyTorch y CUDA
    print("🔍 DIAGNÓSTICO DE PYTORCH Y CUDA:")
    print(f"   PyTorch versión: {torch.__version__}")
    print(f"   CUDA disponible: {torch.cuda.is_available()}")
    print(f"   CUDA versión compilada: {torch.version.cuda}")
    print(f"   cuDNN versión: {torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else 'No disponible'}")
    
    # Verificar si estamos en Jetson
    try:
        with open('/etc/nv_tegra_release', 'r') as f:
            jetson_info = f.read().strip()
            print(f"   Jetson detectado: {jetson_info}")
    except FileNotFoundError:
        print("   No es un dispositivo Jetson")
    
    # Verificar drivers NVIDIA
    try:
        import subprocess
        nvidia_smi = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if nvidia_smi.returncode == 0:
            print("   nvidia-smi: ✅ Disponible")
        else:
            print("   nvidia-smi: ❌ No disponible")
    except:
        print("   nvidia-smi: ❌ No disponible")
    
    print("-" * 50)
    
    if torch.cuda.is_available():
        # Configurar GPU
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"🎮 GPU detectada: {gpu_name}")
        print(f"🎮 Memoria GPU: {gpu_memory:.1f} GB")
        print("⚡ Usando GPU para aceleración")
        
        # Optimizaciones para GPU
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
        
        return device, True
    else:
        print("💻 GPU no disponible, usando CPU")
        return "cpu", False

def procesar_camara(model, device, use_gpu):
    """Procesa video desde la cámara web"""
    # Detectar sistema operativo y elegir path de cámara apropiado
    os_detected = detect_os()
    camera_path = choose_camera_by_OS()
    
    print("📹 Iniciando cámara web... (Presiona 'q' para salir)")
    print(f"🔍 Sistema operativo detectado: {os_detected}")
    print(f"📷 Usando path de cámara: {camera_path}")
    print(f"🚀 Dispositivo de inferencia: {device}")
    
    cap = handle_video_capture("Detección en tiempo real - Cámara", camera_path)
    
    if cap is None:
        print("❌ Error: No se pudo abrir la cámara.")
        return
    
    # Crear anotadores
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    print("🎥 Cámara iniciada. Presiona 'q' para salir...")
    print("📊 Solo se mostrarán detecciones con confianza > 60%")
    
    # Contador de FPS
    frame_count = 0
    start_time = cv2.getTickCount()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error al capturar frame de la cámara.")
            break
        
        # Realizar inferencia con modelo local (usando GPU si está disponible)
        results = model(frame, verbose=False, device=device)[0]
        
        # Convertir resultados de YOLO a formato de supervision
        detections = sv.Detections.from_ultralytics(results)
        
        # Filtrar detecciones por confianza (solo > 60%)
        confidence_threshold = 0.6
        if len(detections) > 0:
            # Obtener índices de detecciones con confianza alta
            high_confidence_mask = detections.confidence > confidence_threshold
            
            # Filtrar detecciones
            detections = detections[high_confidence_mask]
        
        # Calcular FPS
        frame_count += 1
        if frame_count % 30 == 0:  # Actualizar FPS cada 30 frames
            current_time = cv2.getTickCount()
            fps = 30 * cv2.getTickFrequency() / (current_time - start_time)
            start_time = current_time
            print(f"📊 FPS: {fps:.1f}")
        
        # Anotar el frame solo si hay detecciones válidas
        if len(detections) > 0:
            annotated_frame = bounding_box_annotator.annotate(
                scene=frame, detections=detections)
            annotated_frame = label_annotator.annotate(
                scene=annotated_frame, detections=detections)
        else:
            annotated_frame = frame
        
        # Mostrar el frame
        cv2.imshow('Detección en tiempo real - Cámara', annotated_frame)
        
        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Cámara cerrada.")

def main():
    """Función principal"""
    # Ruta al modelo local
    model_path = "weights/merged/best.pt"
    
    # Verificar que el modelo existe
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encontró el modelo en {model_path}")
        print("💡 Asegúrate de que el archivo best.pt esté en weights/merged/")
        return
    
    # Mostrar información del sistema
    os_detected = detect_os()
    camera_path = choose_camera_by_OS()
    print(f"💻 Sistema operativo detectado: {os_detected}")
    print(f"📷 Path de cámara configurado: {camera_path}")
    
    # Detectar y configurar GPU automáticamente
    device, use_gpu = detectar_y_configurar_gpu()
    
    print("🤖 Cargando modelo local...")
    print(f"📋 Modelo: {model_path}")
    
    try:
        # Cargar el modelo local
        model = YOLO(model_path)
        print("✅ Modelo cargado exitosamente!")
        
        # Si hay GPU, mover el modelo a GPU
        if use_gpu:
            model.to(device)
            print("🚀 Modelo movido a GPU")
            
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        print("💡 Posibles soluciones:")
        print("   - Verifica que el archivo best.pt sea válido")
        print("   - Asegúrate de que ultralytics esté instalado")
        if use_gpu:
            print("   - Si hay problemas con GPU, instala PyTorch con soporte CUDA")
        return
    
    print("\n" + "="*50)
    print("    DETECTOR DE OBJETOS EN TIEMPO REAL")
    print("="*50)
    print("🎥 Iniciando detección con cámara...")
    print("📋 Presiona 'q' para salir")
    print("📊 Umbral de confianza: 60%")
    if use_gpu:
        print("⚡ Aceleración GPU activada")
    print("="*50)
    
    # Iniciar detección con cámara
    procesar_camara(model, device, use_gpu)
    
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()