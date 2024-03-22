# ------- Import ---------------------------------------------------------------------------------------------------
import socket
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

# ------- Servo ---------------------------------------------------------------------------------------------------
factory = PiGPIOFactory()
servo = AngularServo(17, pin_factory=factory)

# ------- Conection ---------------------------------------------------------------------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.191.98', 8485))
connection = client_socket.makefile('wb')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Aguardando conexão...")
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            angulo = float(data.decode())
            servo.angle = angulo
