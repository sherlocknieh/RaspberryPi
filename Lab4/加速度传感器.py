from adafruit_adxl34x import ADXL345
from gpiozero import DigitalInputDevice, LED
import board
from time import sleep


class APP:
    def __init__(self):

        # 引脚配置
        self.i2c = board.I2C() # 使用板载I2C针脚
        self.accelerometer = ADXL345(self.i2c) # 创建ADXL345对象
        self.accelerometer.enable_freefall_detection(threshold=10) # 开启自由落体检测

        self.interrupt = DigitalInputDevice(21, pull_up=True) # 创建中断对象
        self.interrupt.when_activated = self.callback

    def callback(self):
        print("interrupt")


    def loop(self):
        while True:
            x, y, z = self.accelerometer.acceleration
            print((x, y, z))
            print("freefall:",self.accelerometer.events["freefall"])
            sleep(0.5)



if __name__ == "__main__":
    app = APP()
    app.loop()