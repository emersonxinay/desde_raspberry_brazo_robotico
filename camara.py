import cv2

# Probar diferentes �ndices de c�mara
for i in range(10, 32):  # Cambia el rango seg�n los dispositivos listados
    print(f"Intentando abrir la c�mara en /dev/video{i}...")
    cap = cv2.VideoCapture(i)

    if not cap.isOpened():
        print(f"No se pudo abrir la c�mara en /dev/video{i}.")
    else:
        print(f"C�mara abierta en /dev/video{i}.")

        # Captura y muestra video
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo recibir el frame. Saliendo...")
                break

            cv2.imshow(f'Video en Vivo - /dev/video{i}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

print("Programa finalizado.")
