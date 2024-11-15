import cv2
import mediapipe as mp

# Inicializar MediaPipe para el reconocimiento de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configuraci�n para el modelo de manos
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # N�mero m�ximo de manos que se pueden detectar
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Inicializar la captura de video
cap = cv2.VideoCapture(1)

# Diccionario para mapear los �ndices de los dedos con su nombre
fingers = {
    4: 'Pulgar',
    8: '�ndice',
    12: 'Medio',
    16: 'Anular',
    20: 'Me�ique'
}

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: No se puede obtener la imagen.")
        break

    # Convertir la imagen a RGB (MediaPipe usa RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con el modelo de manos
    results = hands.process(frame_rgb)

    # Si se detecta una mano
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Dibujar los puntos de referencia de la mano
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Extraer las coordenadas de los dedos y etiquetarlos
            for i, landmark in enumerate(landmarks.landmark):
                # Coordenadas (normalizadas)
                h, w, c = frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)

                # Si es uno de los dedos, dibujamos un c�rculo y mostramos el nombre
                if i in fingers:
                    cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)  # Dibuja un c�rculo azul
                    cv2.putText(frame, fingers[i], (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Mostrar la imagen con los dedos y sus nombres
    cv2.imshow("Hand Recognition", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
