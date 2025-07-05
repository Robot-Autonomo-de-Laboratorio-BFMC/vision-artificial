import supervision as sv
import cv2
import os
import sys
from ultralytics import YOLO
from config import choose_camera_by_OS, handle_video_capture, detect_os

def procesar_camara(model):
    """Procesa video desde la cámara web"""
    # Detectar sistema operativo y elegir path de cámara apropiado
    os_detected = detect_os()
    camera_path = choose_camera_by_OS()
    
    print("📹 Iniciando cámara web... (Presiona 'q' para salir)")
    print(f"🔍 Sistema operativo detectado: {os_detected}")
    print(f"📷 Usando path de cámara: {camera_path}")
    
    cap = handle_video_capture("Detección en tiempo real - Cámara", camera_path)
    
    if cap is None:
        print("❌ Error: No se pudo abrir la cámara.")
        return
    
    # Crear anotadores
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    print("🎥 Cámara iniciada. Presiona 'q' para salir...")
    print("📊 Solo se mostrarán detecciones con confianza > 60%")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error al capturar frame de la cámara.")
            break
        
        # Realizar inferencia con modelo local
        results = model(frame, verbose=False)[0]
        
        # Convertir resultados de YOLO a formato de supervision
        detections = sv.Detections.from_ultralytics(results)
        
        # Filtrar detecciones por confianza (solo > 60%)
        confidence_threshold = 0.6
        if len(detections) > 0:
            # Obtener índices de detecciones con confianza alta
            high_confidence_mask = detections.confidence > confidence_threshold
            
            # Filtrar detecciones
            detections = detections[high_confidence_mask]
        
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
    
    print("🤖 Cargando modelo local...")
    print(f"📋 Modelo: {model_path}")
    
    try:
        # Cargar el modelo local
        model = YOLO(model_path)
        print("✅ Modelo cargado exitosamente!")
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        print("💡 Posibles soluciones:")
        print("   - Verifica que el archivo best.pt sea válido")
        print("   - Asegúrate de que ultralytics esté instalado")
        return
    
    print("\n" + "="*50)
    print("    DETECTOR DE OBJETOS EN TIEMPO REAL")
    print("="*50)
    print("🎥 Iniciando detección con cámara...")
    print("📋 Presiona 'q' para salir")
    print("📊 Umbral de confianza: 60%")
    print("="*50)
    
    # Iniciar detección con cámara
    procesar_camara(model)
    
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()