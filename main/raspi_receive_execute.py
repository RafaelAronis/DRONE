# ------- Advise ---------------------------------------------------------------------------------------------------
#### Run ###
# sudo pigpiod

# ------- Import Libraries ---------------------------------------------------------------------------------------------------
import socket
from utils_main.utils_RSPI import*

# Create camera aime tracker
rspi_tracker = RspiServoControl()
rspi_tracker.create_servo(17,18) # Create servo on pins 17 and 18

# Configuração do servidor socket
PORT_GET = 12345  # Porta para comunicação

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('', PORT_GET))
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
					rspi_tracker.adjust(-x,-y)
					print(rspi_tracker.servo_x.angle, rspi_tracker.servo_y.angle)
except:
	print('Servo off')
finally:
	rspi_tracker.kill()
rspi_tracker.kill()
