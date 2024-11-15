import time
import cv2
import mediapipe as mp
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Configura el bus I2C y el m�dulo PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Frecuencia de 50Hz para los servos

# Configuraci�n de los canales para los dos servos
servo1 = pca.channels[0]  # Servo 1 en el canal 0
servo2 = pca.channels[1]  # Servo 2 en el canal 1

# Funci�n para ajustar el �ngulo del servo
def set_servo_angle(channel, angle):
    pulse_min = 1000  # Ajusta seg�n la especificaci�n de tu servo
    pulse_max = 2000
    pulse_width = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    duty_cycle = int(pulse_width / 1000000 * pca.frequency * 0xFFFF)
    channel.duty_cycle = duty_cycle

# Configuraci�n de la c�mara
cap = cv2.VideoCapture(1)  # Usa la c�mara por defecto

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Funci�n para detectar dedos y reconocer los botones virtuales
def detectar_dedos(frame):
    # Convertir la imagen a RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = hands.process(img_rgb)
    
    if resultados.multi_hand_landmarks:
        for landmarks in resultados.multi_hand_landmarks:
            # Dibujar los puntos de la mano
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtener la posici�n de la punta del dedo �ndice (landmark 8)
            dedo_indice = landmarks.landmark[8]
            alto, ancho, _ = frame.shape
            x = int(dedo_indice.x * ancho)
            y = int(dedo_indice.y * alto)
            
            # Dibujar un c�rculo en la punta del dedo �ndice
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Detectar si el dedo est� sobre uno de los botones
            # Definir las �reas de los botones virtuales
            boton_abrir = (50, 50, 200, 200)  # Coordenadas del bot�n "abrir pinza"
            boton_cerrar = (250, 50, 400, 200)  # Coordenadas del bot�n "cerrar pinza"

            # Dibujar los botones virtuales
            cv2.rectangle(frame, (boton_abrir[0], boton_abrir[1]), (boton_abrir[2], boton_abrir[3]), (0, 0, 255), 3)
            cv2.rectangle(frame, (boton_cerrar[0], boton_cerrar[1]), (boton_cerrar[2], boton_cerrar[3]), (0, 0, 255), 3)

            # Comprobar si el dedo est� dentro de la regi�n del bot�n
            if boton_abrir[0] < x < boton_abrir[2] and boton_abrir[1] < y < boton_abrir[3]:
                cv2.putText(frame, "Abrir Pinza", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Abrir pinza
                set_servo_angle(servo1, 0)
                set_servo_angle(servo2, 0)
            elif boton_cerrar[0] < x < boton_cerrar[2] and boton_cerrar[1] < y < boton_cerrar[3]:
                cv2.putText(frame, "Cerrar Pinza", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # Cerrar pinza
                set_servo_angle(servo1, 180)
                set_servo_angle(servo2, 180)

    return frame

try:
    while True:
        # Captura de un fotograma de la c�mara
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar la imagen.")
            break
        
        # Detectar dedos y botones en el fotograma
        frame = detectar_dedos(frame)

        # Mostrar el fotograma con las detecciones
        cv2.imshow("Reconocimiento de Dedos", frame)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Programa finalizado.")

finally:
    # Apagar los servos al finalizar el programa
    servo1.duty_cycle = 0
    servo2.duty_cycle = 0
    cap.release()
    cv2.destroyAllWindows()
