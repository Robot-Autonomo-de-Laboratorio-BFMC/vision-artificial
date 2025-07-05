import platform
import cv2

LINUX_CAMERA_PATH = "/dev/video0"
WINDOWS_CAMERA_PATH = 0


def handle_video_capture(window_name, path):
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(path)

    if not capture.isOpened():
        print("Error: Could not open video stream.")
        return None

    # Optimizar configuración para Logitech BRIO en Linux/WSL
    if isinstance(path, str) and "/dev/video" in path:
        # Configurar para mejor rendimiento con MJPG
        capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        capture.set(cv2.CAP_PROP_FPS, 30)
        
        # Verificar configuración aplicada
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        
        print(f"📷 Cámara configurada: {width}x{height} @ {fps}fps (MJPG)")

    return capture


def detect_os():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "mac"
    elif "microsoft" in platform.uname().release.lower():  # Detect WSL
        return "wsl"
    else:
        return "linux"


def choose_camera_by_OS():
    os = detect_os()
    if os == "wsl" or os == "linux":
        return LINUX_CAMERA_PATH
    else:
        return WINDOWS_CAMERA_PATH