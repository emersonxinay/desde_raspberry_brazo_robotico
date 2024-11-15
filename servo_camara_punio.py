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
            
            # Extraer las posiciones de los dedos para determinar si el pu�o est� cerrado o abierto
            dedos_abiertos = 0
            # Evaluar los dedos del 1 al 5 (el pulgar es el dedo 0)
            for i in range(1, 5):
                # Compara la posici�n de la punta del dedo con la de las articulaciones cercanas
                # Si la punta del dedo est� por debajo de la articulaci�n superior, est� doblado (cerrado)
                if landmarks.landmark[mp_hands.HandLandmark(i * 4 + 4)].y > landmarks.landmark[i * 4 + 3].y:
                    dedos_abiertos += 1
            
            # Si hay m�s de 1 dedo abierto, es un pu�o abierto
            if dedos_abiertos <= 1:  # Si solo el pulgar est� abierto o ninguno
                # Pu�o cerrado
                set_servo_angle(servo1, 180)  # Cerrar pinza
                set_servo_angle(servo2, 180)
                cv2.putText(frame, "Pu�o Cerrado - Cerrar Pinza", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Pu�o abierto
                set_servo_angle(servo1, 0)  # Abrir pinza
                set_servo_angle(servo2, 0)
                cv2.putText(frame, "Pu�o Abierto - Abrir Pinza", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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
