from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

# 云台
class ServoGimbal:
    def __init__(self, horizontal_pin, vertical_pin):
        # 水平伺服电机
        self.horizontal_servo = AngularServo(
            horizontal_pin,
            pin_factory=PiGPIOFactory(),
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )
        # 垂直伺服电机
        self.vertical_servo = AngularServo(
            vertical_pin,
            pin_factory=PiGPIOFactory(),
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )
        # 当前视角
        self.theta = 0
        self.phi = 0

    # 云台控制
    def move_to(self, theta, phi):
        "theta: -90 ~ 90, 水平视角"
        "phi: -90 ~ 90, 仰视角"
        self.theta = theta
        self.phi = phi
        self.horizontal_servo.angle = theta
        self.vertical_servo.angle = (-phi)
    
    # 坐标跟踪控制
    def track_to(self, dx, dy):
        "dx: -200 ~ 200, 相对水平位移"
        "dy: -200 ~ 200, 相对仰视位移"
        if abs(dx) > 20 and abs(dy) > 20:
            self.move_to(self.theta - dx/50, self.phi + dy/50)

    # 释放资源
    def release(self):
        self.horizontal_servo.close()
        self.vertical_servo.close()
    
    def __del__(self):
        self.release()

if __name__ == "__main__":
    gimbal = ServoGimbal(14, 15)
    try:
        gimbal.move_to(0, 0)
        sleep(1)
    finally:
        gimbal.release()
        