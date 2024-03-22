import socket
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from utils2 import*
#sudo pigpiod


# Create camera aime tracker
cam_tracker = CamAimTracker()
cam_tracker.create_servo(17,18) # Create servo

# Configuração do servidor socket
HOST = ''  # Deixe em branco para aceitar conexões em todas as interfaces
PORT = 12345  # Porta para comunicação

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		print("Aguardando conexão...")
		conn, addr = s.accept()
		with conn:
			print('Conectado por', addr)
			while True:
				data = conn.recv(1024).decode()
				if len(data.split(',')) == 2: 
					x, y = data.split(',')
					x = float(x)
					y = float(y)
					cam_tracker.adjust(-x,-y)
					print(cam_tracker.servo_x.angle, cam_tracker.servo_y.angle)
except:
	print('Servo off')
finally:
	cam_tracker.kill()
cam_tracker.kill()


