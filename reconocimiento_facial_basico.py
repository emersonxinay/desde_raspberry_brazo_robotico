import cv2

# Cargar el clasificador en cascada para detecci�n de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar la captura de video
cap = cv2.VideoCapture(1)  # Usa el �ndice de la c�mara correcta (cambia a 0 si es necesario)

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo obtener la imagen.")
        break

    # Convertir la imagen a escala de grises (mejora la precisi�n de la detecci�n)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen (usando el clasificador en cascada)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar un rect�ngulo alrededor de cada rostro detectado
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibujar un rect�ngulo azul

    # Mostrar la imagen con los rostros detectados
    cv2.imshow('Face Detection', frame)

    # Salir del loop con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
