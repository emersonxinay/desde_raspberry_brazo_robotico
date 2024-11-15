import cv2

# Abre la c�mara (el �ndice 0 generalmente corresponde a la c�mara por defecto)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: No se puede abrir la c�mara")
    exit()

while True:
    # Lee el frame de la c�mara
    ret, frame = cap.read()

    if not ret:
        print("Error: No se puede leer el frame")
        break

    # Muestra el frame
    cv2.imshow('Video', frame)

    # Espera 1 ms y sale si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la c�mara y cierra las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
