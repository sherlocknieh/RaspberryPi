from gpiozero import Servo, LED, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

import numpy as np
from matplotlib import pyplot as plt

# 雷达测距云台
class ServoGimbal:
    def __init__(self, horizontal_pin, vertical_pin):

        # 水平伺服电机
        self.horizontal_servo = Servo(
            horizontal_pin,
            pin_factory=PiGPIOFactory(),
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )
        
        # 垂直伺服电机
        self.vertical_servo = Servo(
            vertical_pin,
            pin_factory=PiGPIOFactory(),
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )

        # 距离传感器
        self.dist_sensor = DistanceSensor(
            echo=23,
            trigger=24,
            max_distance=1,
            threshold_distance=0.02,
            pin_factory=PiGPIOFactory()
        )

    # 三角波生成器(-1~1)
    def tri_wave(self):
        while True:
            for i in np.linspace(-1, 1, 40):
                yield i
            for i in np.linspace(1, -1, 40):
                yield i

    def run(self, speed = 1):
        # 创建图形窗口（只创建一次）
        plt.figure(figsize=(8, 8))
        plt.ion() # 开启交互模式
        plt.show() 
        plt.clf()
        plt.subplot(111, projection='polar')
        for angle in self.tri_wave():
            print(f'水平伺服: {angle:.2f}')
            self.horizontal_servo.value = angle # 更新伺服位置
            self.vertical_servo.value = 0
            theta = (angle+1)/2 * np.pi         # 转换为弧度
            r = self.dist_sensor.distance       # 获取距离
            if (r):
                print(f'距离: {r:.4f} 米')
                # 把新点添加到极坐标图
                plt.plot(theta, r, 'bo', markersize=8)  # 'bo' 表示蓝色圆点，markersize控制点的大小
                plt.title(f'{int((angle+1)/2*180)}°') # 更新标题
                plt.pause(0.1)  # 暂停以更新图形
                print(f'距离: {r:.4f} 米')
            sleep(1/speed)   # 控制循环频率


# 主程序
if __name__ == "__main__":
    gimbal = ServoGimbal(14, 15)
    gimbal.run(4) # 速度为2Hz