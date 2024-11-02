import cv2
import mediapipe as mp
from gpiozero import Servo
from time import sleep

# Configura el pin GPIO 18 para el servo
servo = Servo(18)

# Configuraci�n de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Abre la c�mara
cap = cv2.VideoCapture(0)

# Funci�n para determinar el gesto de la mano
def detectar_gesto(mano_landmarks):
    dedos_arriba = []

    # Dedos pulgar, �ndice y medio
    dedos = [4, 8, 12]
    for i in dedos:
        if mano_landmarks.landmark[i].y < mano_landmarks.landmark[i - 2].y:
            dedos_arriba.append(1)  # Dedo levantado
        else:
            dedos_arriba.append(0)  # Dedo bajado

    if dedos_arriba == [0, 0, 0]:
        return "cerrado"  # Pu�o cerrado
    elif dedos_arriba == [0, 1, 0]:
        return "medio"  # Un dedo levantado (�ndice)
    elif dedos_arriba == [0, 1, 1]:
        return "abierto"  # Dos dedos levantados (�ndice y medio)
    return "ninguno"

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convierte la imagen a RGB para MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)

        # Verifica si se han detectado manos
        if resultado.multi_hand_landmarks:
            for hand_landmarks in resultado.multi_hand_landmarks:
                # Dibuja las marcas de la mano
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detecta el gesto
                gesto = detectar_gesto(hand_landmarks)
                print(f"Gesto detectado: {gesto}")

                # Mueve el servo seg�n el gesto
                if gesto == "cerrado":
                    servo.value = 1  # Cerrar (0 grados)
                elif gesto == "medio":
                    servo.value = 0  # Semi-abierto (90 grados)
                elif gesto == "abierto":
                    servo.value = -1  # Abrir (180 grados)
                
                sleep(1.5)

        # Muestra el video en pantalla
        cv2.imshow("Detecci�n de gestos", frame)

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass  # Permite salir del bucle con Ctrl+C

finally:
    # Libera los recursos
    cap.release()
    cv2.destroyAllWindows()
    print("Programa finalizado.")
