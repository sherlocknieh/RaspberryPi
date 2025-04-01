from gpiozero import DigitalInputDevice, LED, Button
from adafruit_adxl34x import ADXL345
from time import sleep
import board


class APP:
    def __init__(self):

        # 引脚配置
        self.red_led = LED(17)   # 红色LED
        self.red_led.off()       # 红色LED默认熄灭
        self.green_led = LED(27) # 绿色LED
        self.green_led.on()      # 绿色LED默认点亮

        self.button = Button(10, bounce_time=0.05) # 按键
        self.intpin = DigitalInputDevice(21, pull_up=True) # 中断引脚

        self.accelerometer = ADXL345(board.I2C())                  # ADXL345对象
        self.accelerometer.enable_freefall_detection(threshold=12) # 自由落体检测, threshold越大越灵敏

        # 中断配置
        self.intpin.when_activated = self.danger
        self.button.when_pressed = self.safe


    def danger(self): # 坠落响应函数
        self.green_led.off()
        self.red_led.blink(0.5, 0.5) # 红色LED闪烁3次
        print("检测到坠落!")
    
    def safe(self): # 安全响应函数
        self.red_led.off()
        self.green_led.on()
        print("解除警报")


    def loop(self):
        while True:
            self.accelerometer.events["freefall"] # 检测自由落体事件
            sleep(0.1)



if __name__ == "__main__":
    app = APP()
    app.loop()