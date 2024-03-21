# Import
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

# Set up pigpio pin factory
factory = PiGPIOFactory()

# Create servo object using pigpio pin factory
servo = AngularServo(17, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)

# Loop principal
try:
    while True:
        angulo = int(input())
        servo.angle = max(-90, min(90, angulo))
except :
    print('Servo off')
finally:
    servo.detach()
    servo.close()
