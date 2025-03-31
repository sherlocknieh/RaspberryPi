from gpiozero import Button, PWMLED
from time import sleep

class TrafficLight:
    def __init__(self, button_pin, red_pin, green_pin, blue_pin):

        # 引脚初始化
        self.button = Button(button_pin, bounce_time=0.05)  # 防抖动
        self.red = PWMLED(red_pin)                         # 红灯
        self.green = PWMLED(green_pin)                     # 绿灯
        self.blue = PWMLED(blue_pin)                       # 蓝灯
        self.lights = [self.red, self.green, self.blue]    # 三色灯列表
        # 状态初始化
        self.running = False   # 交通灯效果开关
        self.current_color = 0 # 当前颜色: 0=红灯，1=绿灯，2=蓝灯
        self.brightness = 0.0  # 当前亮度
        self.direction = 1     # 亮度变化方向: 1=淡入，-1=淡出
        # 事件绑定
        self.button.when_pressed = self.change_state

    def change_state(self):
        self.running = not self.running
        if self.running:
            self.current_color = 0
            self.brightness = 0.0
            print("交通灯效果 开启")
        else:
            print("交通灯效果 关闭")

    def loop(self):
        while True:
            if self.running:            # 交通灯效果开启
                self.brightness += 0.01 * self.direction
                if self.brightness >= 1.0:    # 亮度增加到1,开始减少亮度
                    self.direction = -1
                    self.brightness = 1.0
                elif self.brightness <= 0.0:  # 亮度减少到0,切换颜色,开始增加亮度
                    self.direction = 1
                    self.brightness = 0.0
                    self.current_color = (self.current_color + 1) % 3
                self.lights[self.current_color].value = self.brightness # 设置当前颜色的亮度

            else:            # 交通灯效果关闭
                for light in self.lights: # 关闭所有灯
                    light.value = 0

            sleep(0.01)            # 等待0.01秒

if __name__ == '__main__':
    traffic_light = TrafficLight(button_pin=21, red_pin=17, green_pin=27, blue_pin=22)
    traffic_light.loop()
