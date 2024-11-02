import cv2

# Intenta abrir la c�mara en /dev/video14 o el �ndice adecuado
cap = cv2.VideoCapture('/dev/video14')

if not cap.isOpened():
    print("Error: No se pudo abrir la c�mara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo recibir el frame.")
        break

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
