
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass  # Espera hasta obtener el bloqueo del bus I2C

devices = i2c.scan()  # Escanea los dispositivos conectados al bus
print("Dispositivos encontrados:", devices)
i2c.unlock()  # Libera el bus I2C
