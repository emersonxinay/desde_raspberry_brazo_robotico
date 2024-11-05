import board
import busio

# Define los pines SCL y SDA
SCL = board.SCL  # GPIO 3
SDA = board.SDA  # GPIO 2

# Inicializa el bus I2C
i2c = busio.I2C(SCL, SDA)
