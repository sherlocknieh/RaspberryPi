from gpiozero import LED, DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

TRIGGER_PIN = 15
ECHO_PIN = 14
HIGHT = 0.2

# 硬件引脚定义
class App:
    def __init__(self):
        # 引脚定义
        self.dist_sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIGGER_PIN, max_distance=1, threshold_distance=0.02, pin_factory=PiGPIOFactory())
        self.red = LED(2)
        self.green = LED(3)

        self.red.off()
        self.green.off()

        # 状态变量
        self.alerting = False
        self.danger = False
        self.distance = 0
        # 事件绑定
        self.dist_sensor.when_in_range = self.in_range
        self.dist_sensor.when_out_of_range = self.out_of_range

    # 事件处理函数
    def in_range(self):
        self.red.blink()
        print('进入范围')
    def out_of_range(self):
        self.red.off()
        print('离开范围')
        
    # 主循环
    def loop(self):
        while True:
            self.distance = self.dist_sensor.distance                    # 测量距离
            self.distance = (self.dist_sensor.distance + 0.014402)/0.984 # 距离修正
            print(f'距离: {(self.distance):.4f} 米')
            sleep(1)




if __name__ == '__main__':
    app = App()
    app.loop()