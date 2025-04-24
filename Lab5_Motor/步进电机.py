from gpiozero import OutputDevice
from time import sleep

A1 = OutputDevice(17) # A+
A0 = OutputDevice(18) # A-
B1 = OutputDevice(27) # B+
B0 = OutputDevice(22) # B-

motor = [A1, B1, A0, B0] # 轮转顺序

# steps: 前进步数
# speed: 速度(步/秒)
# direction: 方向(1正转，-1反转)
def step(steps=1000, speed=100, direction=1):
    delay = 1/speed    # 速度转化为延时
    # 开始转动
    i = 0
    while steps > 0:
        for j in range(4):
            motor[j].off() # 先全部关闭
        motor[i].on()      # 再打开当前引脚
        i = (i + direction)%4
        steps -= 1
        sleep(delay)

if __name__ == "__main__":

    step(steps=22, speed=10, direction=-1) # 转360°
