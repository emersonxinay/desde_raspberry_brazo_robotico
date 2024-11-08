import cv2
import subprocess
import numpy as np

# RTMP URL del flujo
rtmp_url = 'rtmp://192.168.0.149/live/emerson123'

# Iniciar el proceso FFmpeg para capturar el flujo de video
ffmpeg_command = [
    'ffmpeg',
    '-i', rtmp_url,
    '-f', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', '640x480',
    '-r', '30',  # Ajusta la tasa de frames si es necesario
    '-an',  # Desactiva el audio
    '-c:v', 'libx264',  # C�dec de video
    '-preset', 'ultrafast',  # Mejorar latencia
    '-'
]


# Abre un pipe a FFmpeg
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    # Lee el video rawstream de FFmpeg
  # Ajusta seg�n tu resoluci�n
    raw_frame = ffmpeg_process.stdout.read(640 * 480 * 3)

    if not raw_frame:
        break

    # Convierte el raw stream a una imagen que OpenCV pueda procesar
   # Ajusta el tama�o seg�n tu c�mara
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))

    # Mejora de la imagen: Ajuste de brillo y contraste
    alpha = 1.5  # Contraste
    beta = 50    # Brillo
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Aplicaci�n de un filtro de desenfoque para reducir ruido
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Mostrar el video procesado con OpenCV
    cv2.imshow("Stream", frame)

    # Esperar y salir si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cierra el proceso y la ventana
ffmpeg_process.stdout.close()
ffmpeg_process.stderr.close()
ffmpeg_process.wait()
cv2.destroyAllWindows()
