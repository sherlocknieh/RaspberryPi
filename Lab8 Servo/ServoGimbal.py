from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from signal import pause
import numpy as np
from matplotlib import pyplot as plt

class ServoGimbal:
    def __init__(self, horizontal_pin, vertical_pin):

        # 使用pigpio引脚工厂提高PWM精度
        self.factory = PiGPIOFactory()
        
        # 创建水平方向伺服电机（左右转动）
        self.horizontal_servo = Servo(
            horizontal_pin,
            pin_factory=self.factory,
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )
        
        # 创建垂直方向伺服电机（上下转动）
        self.vertical_servo = Servo(
            vertical_pin,
            pin_factory=self.factory,
            min_pulse_width=0.5/1000,  # 0.5ms
            max_pulse_width=2.5/1000,  # 2.5ms
            frame_width=20/1000        # 20ms
        )

        # 全局状态变量
        self.posx = 0
        self.posy = 0

    # 位置控制
    def set_position(self, horizontal, vertical):
        self.horizontal_servo.value = horizontal
        self.vertical_servo.value = vertical
    
    # 左右巡视
    def scan_area(self):
        # 创建图形窗口（只创建一次）
        step = 20
        a = np.linspace(0, 1, step)
        b = np.linspace(1, -1, step)
        c = np.linspace(-1, 0, step)
        allpath = np.concatenate((a, b, c))
        
        
        plt.figure(figsize=(8, 8))
        plt.clf()
        plt.subplot(111, projection='polar')
        try:
            while True:
                for i in allpath:
                    # 更新伺服位置
                    self.horizontal_servo.value = i
                    self.posx = i
                    # 更新图像
                    theta = (i+1)/2 * np.pi  # 转换为弧度
                    plt.clf()  # 清除当前图形
                    plt.subplot(111, projection='polar')
                    plt.polar([0, theta], [0, 1], color='blue', linewidth=2)
                    plt.title(f'{int((i+1)/2*180)}°')
                    plt.pause(0.1)
                    sleep(0.1)
        except KeyboardInterrupt:
            print("巡视结束")
        finally:
            # 完成后关闭图形窗口
            plt.close()

    def state_changer(self):
        # 更新伺服电机位置
        step = 20
        a = np.linspace(0, 1, step)
        b = np.linspace(1, -1, step)
        c = np.linspace(-1, 0, step)
        allpath = np.concatenate((a, b, c))
        while True:
            for i in allpath:
                self.posx = i
                sleep(0.1)

    def state_applier(self):
        while True:
            self.set_position(self.posx, self.posy)
            sleep(0.1)

    def plot_drawer(self):

        plt.figure(figsize=(8, 8))
        plt.clf()
        plt.subplot(111, projection='polar')

        while True:
            theta = (self.posx+1)/2 * np.pi  # 转换为弧度
            plt.clf()  # 清除当前图形
            plt.subplot(111, projection='polar')
            plt.polar([0, theta], [0, 1], color='blue', linewidth=2)
            plt.title(f'{int((self.posx+1)/2*180)}°')
            plt.pause(0.1)
            sleep(0.1)

    def run(self):
        #多线程运行
        import threading
        
        state_thread = threading.Thread(target=self.state_changer)
        state_thread.start()

        state_thread = threading.Thread(target=self.state_applier)
        state_thread.start()

        state_thread = threading.Thread(target=self.plot_drawer)
        state_thread.start()

# 主程序
if __name__ == "__main__":
    gimbal = ServoGimbal(12, 13) # GPIO12 水平，GPIO13 垂直
    gimbal.run()