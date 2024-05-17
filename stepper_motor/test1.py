# # import RPi.GPIO as GPIO
# # from time import sleep
# # import sys

# # # Atribui os pinos GPIO para o motor
# # motor_channel = (11, 12, 15, 16)
# # GPIO.setwarnings(False)
# # GPIO.setmode(GPIO.BOARD)

# # GPIO.setup(motor_channel, GPIO.OUT)

# # def run_motor(direction, delay):
# #     while True:
# #         try:
# #             if direction == 'c':  # Sentido horário
# #                 print('motor running clockwise\n')
# #                 GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
# #                 GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
# #                 GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
# #                 GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
# #                 sleep(delay)

# #             elif direction == 'a':  # Sentido anti-horário
# #                 print('motor running anti-clockwise\n')
# #                 GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
# #                 GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
# #                 GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
# #                 GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
# #                 sleep(delay)

# #         except KeyboardInterrupt:
# #             direction = input('select motor direction a=anticlockwise, c=clockwise or q=exit: ')
# #             if direction == 'q':
# #                 print('motor stopped')
# #                 GPIO.cleanup()
# #                 sys.exit(0)

# # if __name__ == "__main__":
# #     motor_direction = input('select motor direction a=anticlockwise, c=clockwise: ')
# #     delay = float(input('Enter delay in seconds (e.g., 0.01): '))
# #     run_motor(motor_direction, delay)

# import RPi.GPIO as GPIO
# import time
# GPIO.setmode(GPIO.BOARD)
# control_pins = [11,12,15,16]
# for pin in control_pins:
#   GPIO.setup(pin, GPIO.OUT)
#   GPIO.output(pin, 0)
# halfstep_seq = [
#   [1,0,0,0],
#   [1,1,0,0],
#   [0,1,0,0],
#   [0,1,1,0],
#   [0,0,1,0],
#   [0,0,1,1],
#   [0,0,0,1],
#   [1,0,0,1]
# ]
# for i in range(512):
#   for halfstep in range(8):
#     for pin in range(4):
#       GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
#     time.sleep(0.001)
# GPIO.cleanup()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
control_pins = [11, 12, 15, 16]

# Define a sequência de passos completa
fullstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Configura os pinos como saída
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Função para mover o motor em uma direção
def move_motor(sequence):
    for _ in range(512):  # Realiza 512 passos para completar uma volta (200 passos por revolução * 2)
        for halfstep in sequence:
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep[pin])
            time.sleep(0.001)  # Tempo de atraso mínimo

try:
    while True:
        move_motor(fullstep_seq)  # Move no sentido horário
        # move_motor(fullstep_seq[::-1])  # Move no sentido anti-horário

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")

finally:
    GPIO.cleanup()
