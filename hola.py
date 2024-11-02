from gpiozero import Servo
from time import sleep

# Configura el pin GPIO 18
servo = Servo(18)

# Posici�n actual del servo
posicion_actual = 0  # Inicialmente en 0 grados (pinza cerrada)

# Mueve la pinza a una posici�n inicial
servo.value = 1  # 180 grados (pinza cerrada)
sleep(1)

try:
    while True:
        # Men� de opciones
        print("\nOpciones:")
        print("1. Cerrar (0 grados)")
        print("2. Semi-abierto (90 grados)")
        print("3. Abrir (180 grados)")
        print("4. Salir")
        
        # Solicitar la opci�n del usuario
        opcion = input("Elige una opcion (1-4): ")
        
        if opcion == '1' and posicion_actual != 0:
            servo.value = 1  # 0 grados (pinza cerrada)
            posicion_actual = 0
        elif opcion == '2' and posicion_actual != 90:
            servo.value = 0  # 90 grados (semi-abierto)
            posicion_actual = 90
        elif opcion == '3' and posicion_actual != 180:
            servo.value = -1  # 180 grados (pinza abierta)
            posicion_actual = 180
        elif opcion == '4':
            break
        else:
            print("Opcion no valida o no se requiere movimiento.")

except KeyboardInterrupt:
    pass  # Permite salir del bucle con Ctrl+C

print("Programa finalizado.")
