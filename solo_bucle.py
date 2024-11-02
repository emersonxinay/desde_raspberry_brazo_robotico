from gpiozero import Servo
from time import sleep

# Configura el pin GPIO 18
servo = Servo(18)

# Mueve la pinza a una posici�n inicial
servo.value = 1  # 180 grados (pinza abierta)
sleep(1)

try:
    while True:
        # Cerrar (0 grados)
        servo.value = 1  # 0 grados (cerrar)
        sleep(1.5)

        # Semi-abierto (90 grados)
        servo.value = 0  # 90 grados (semi-abierto)
        sleep(1.5)

        # Abrir (180 grados)
        servo.value = -1  # 180 grados (abrir)
        sleep(1.5)

except KeyboardInterrupt:
    pass  # Permite salir del bucle con Ctrl+C

print("Programa finalizado.")
