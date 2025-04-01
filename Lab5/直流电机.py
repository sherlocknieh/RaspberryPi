from gpiozero import PWMOutputDevice
from time import sleep

Pin1 = PWMOutputDevice(17)
Pin2 = PWMOutputDevice(18)

def 正转(速度):
    Pin1.value = 速度
    Pin2.value = 0
    print("正转")

def 反转(速度):
    Pin1.value = 0
    Pin2.value = 速度
    print("反转")

def 停止():
    Pin1.value = 0
    Pin2.value = 0
    print("停止")

if __name__ == "__main__":
    正转(0.1)
    sleep(1)

    停止()
    sleep(1)
    
    反转(0.1)
    sleep(1)
    
    停止()