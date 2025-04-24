from gpiozero import PWMLED, LineSensor, Button
from signal import pause
from time import time

class APP:
    # 硬件引脚定义
    def __init__(self):
        self.line_sensor = LineSensor(0,threshold = 0.9) # 白线探测器
        self.button = Button(21, pull_up=False, bounce_time=0.1) # 按键
        self.red = PWMLED(2)
        self.green = PWMLED(3)
        self.blue = PWMLED(4)

        # 状态变量
        self.mesuring = False   # 测量开关
        self.start_time = 0     # 开始时间
        self.end_time = 0       # 结束时间
        self.n_circle = 0       # 圈数
        self.average_speed = 0  # 平均转速

        # 事件绑定
        self.line_sensor.when_line = self.leaving
        self.line_sensor.when_no_line = self.entering
        self.button.when_pressed = self.mesure_switch

    # 主循环
    def loop(self):
        pause()

    # 事件处理函数
    # 测量开关
    def mesure_switch(self):
        self.mesuring = not self.mesuring
        if self.mesuring:
            print("测量开始")
        else:
            self.end_time = time()
            self.n_circle = 0
            print("测量结束")
            print("平均转速: %.2f 圈/秒" % self.average_speed)
    # 进入黑色区域时
    def entering(self): 
        self.green.value = 0    # 绿灯亮
        if not self.mesuring:   # 如果没有开启测量，则不做任何事情
            return
        if self.n_circle == 0:  # 第 1 次碰到黑线,计录开始时间
            print('计时开始\t t = 0.00 秒')
            self.n_circle += 1
            self.start_time = time()
        else:                   # 第 n 次碰到黑线,记录结束时间,计算平均速度
            self.end_time = time()
            delta_t = self.end_time - self.start_time
            self.average_speed = self.n_circle / delta_t
            print(f'完成第{self.n_circle}圈\t t = {delta_t:.2f}秒\t{self.average_speed:.2f}圈/秒')
            self.n_circle += 1
    # 离开黑色区域时
    def leaving(self):
        self.green.value = 1   # 绿灯灭


if __name__ == '__main__':
    app = APP()
    app.loop()