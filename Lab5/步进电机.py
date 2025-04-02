from gpiozero import OutputDevice, Button
from time import sleep
from signal import pause


A1 = OutputDevice(17) # A+
A0 = OutputDevice(18) # A-
B1 = OutputDevice(27) # B+
B0 = OutputDevice(22) # B-

motor = [A1, B1, A0, B0]                # 电机引脚
button = Button(21, bounce_time=0.05)   # 按键
stopped = False                  # 停止标志

def step(steps=1000, speed=100, direction=1):
    # 速度转化为延时
    delay = 1/speed
    # 归零
    for i in motor:
        i.off()
    # 开始转动
    index = 0
    while steps and not stopped:
        motor[index-1].off()
        motor[index].on()
        index = (index + direction)%4
        steps -= 1
        sleep(delay)

def toggle_stopped():
    global stopped
    stopped = not stopped

button.when_pressed = toggle_stopped

if __name__ == "__main__":
    step()
