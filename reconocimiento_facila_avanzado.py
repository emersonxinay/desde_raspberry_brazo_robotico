import cv2
import os
import numpy as np

# FunciÃ³n para capturar imÃ¡genes
def capturar_imagenes():
    # Crear el objeto de captura de video
    cam = cv2.VideoCapture(1)  # Asegúrate de que la cámara correcta esté siendo seleccionada
    if not cam.isOpened():
        print("No se puede acceder a la cámara.")
        return

    # Configurar el detector de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("Capturando imágenes...")

    # Establecer un contador para el número de imágenes capturadas
    contador = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los rostros en la imagen
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Dibujar un rectángulo alrededor de los rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Mostrar la imagen con los rostros detectados
        cv2.imshow("Captura de Imagen", frame)

        # Guardar las imágenes cuando se detecte un rostro
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                rostro = gray[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (200, 200))
                # Guardar la imagen del rostro
                cv2.imwrite(f"rostros/rostro_{contador}.jpg", rostro)
                contador += 1

        # Finalizar si el usuario presiona 'q' o si se alcanzan 100 imágenes
        if cv2.waitKey(1) & 0xFF == ord('q') or contador >= 100:  # Limitar a 100 imágenes
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"Se han capturado {contador} imágenes.")

# FunciÃ³n para entrenar el modelo
def entrenar_modelo():
    # Cargar las imágenes de los rostros
    faces = []
    labels = []
    for archivo in os.listdir("rostros"):
        if archivo.endswith(".jpg"):
            rostro = cv2.imread(os.path.join("rostros", archivo), cv2.IMREAD_GRAYSCALE)
            faces.append(rostro)
            # Usamos el número en el nombre del archivo como etiqueta
            etiqueta = int(archivo.split('_')[1].split('.')[0])
            labels.append(etiqueta)
            print(f"Cargando rostro: {archivo}, Etiqueta: {etiqueta}")

    if len(faces) == 0:
        print("No se encontraron imágenes de rostros para entrenar.")
        return

    # Crear un modelo de reconocimiento facial
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(labels))

    # Guardar el modelo entrenado
    model.save("modelo_face.xml")
    print("Modelo entrenado y guardado con éxito.")

# FunciÃ³n para realizar el reconocimiento facial
def reconocimiento_facial():
    # Cargar el modelo entrenado
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("modelo_face.xml")

    # Configurar la cámara
    cam = cv2.VideoCapture(1)  # Asegúrate de que la cámara correcta esté siendo seleccionada
    if not cam.isOpened():
        print("No se puede acceder a la cámara.")
        return

    # Configurar el detector de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los rostros en la imagen
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Realizar el reconocimiento facial
        for (x, y, w, h) in faces:
            rostro = gray[y:y + h, x:x + w]
            label, confidence = model.predict(rostro)
            cv2.putText(frame, f"ID: {label} - {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Dibujar un rectángulo alrededor del rostro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Mostrar la imagen con el reconocimiento
        cv2.imshow("Reconocimiento Facial", frame)

        # Finalizar si el usuario presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# FunciÃ³n principal con el menú interactivo
def main():
    while True:
        # Mostrar el menú
        print("\nMenú de Opciones:")
        print("1. Capturar imágenes")
        print("2. Entrenar el modelo")
        print("3. Realizar reconocimiento facial")
        print("4. Salir")

        # Leer la opción seleccionada
        opcion = input("Elige una opción (1-4): ")

        # Ejecutar la opción seleccionada
        if opcion == "1":
            capturar_imagenes()
        elif opcion == "2":
            entrenar_modelo()
        elif opcion == "3":
            reconocimiento_facial()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor elige nuevamente.")

# Llamada a la función main
if __name__ == "__main__":
    # Crear el directorio "rostros" si no existe
    if not os.path.exists("rostros"):
        os.makedirs("rostros")
    main()
