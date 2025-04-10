from gpiozero import AngularServo, Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

servo_horizontal = Servo(
    12,
    pin_factory=PiGPIOFactory(),
    min_pulse_width = 0.5 / 1000,
    max_pulse_width = 2.5 / 1000,
    frame_width = 20 / 1000
)

servo_vertical = AngularServo(
    13,
    pin_factory=PiGPIOFactory(),
    min_pulse_width = 0.5 / 1000,
    max_pulse_width = 2.5 / 1000,
    frame_width = 20 / 1000
)

angles = [-90, 0, 90, 0]

while True:
    servo_horizontal.value = 0
    sleep(1)