#!/usr/bin/env python3
# raspi_controller.py - 树莓派硬件控制模块

import time

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    # 在非树莓派环境下运行时提供模拟功能
    GPIO_AVAILABLE = False
    print("警告: RPi.GPIO 库不可用。使用模拟模式。")

# GPIO引脚定义
LED_PIN = 17
MOTOR_PIN_1 = 18  # 直流电机控制引脚1
MOTOR_PIN_2 = 23  # 直流电机控制引脚2
STEP_PINS = [24, 25, 8, 7]  # 步进电机控制引脚
DISTANCE_TRIG = 20  # 超声波传感器Trig引脚
DISTANCE_ECHO = 21  # 超声波传感器Echo引脚
TEMP_PIN = 4       # 温度传感器引脚
LINE_SENSOR_PIN = 16  # 巡线传感器引脚

# 初始化GPIO
def init():
    if GPIO_AVAILABLE:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # LED设置
        GPIO.setup(LED_PIN, GPIO.OUT)
        # 电机设置
        GPIO.setup(MOTOR_PIN_1, GPIO.OUT)
        GPIO.setup(MOTOR_PIN_2, GPIO.OUT)
        for pin in STEP_PINS:
            GPIO.setup(pin, GPIO.OUT)
        # 传感器设置
        GPIO.setup(DISTANCE_TRIG, GPIO.OUT)
        GPIO.setup(DISTANCE_ECHO, GPIO.IN)
        GPIO.setup(LINE_SENSOR_PIN, GPIO.IN)
        print("GPIO初始化完成")
    else:
        print("模拟模式: GPIO初始化被跳过")

# LED控制
def led_on():
    if GPIO_AVAILABLE:
        GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED已打开")

def led_off():
    if GPIO_AVAILABLE:
        GPIO.output(LED_PIN, GPIO.LOW)
    print("LED已关闭")

# 直流电机控制
def motor_forward(speed=100):
    if GPIO_AVAILABLE:
        # 假设使用PWM控制电机速度
        pwm1 = GPIO.PWM(MOTOR_PIN_1, 100)
        pwm1.start(speed)
        GPIO.output(MOTOR_PIN_2, GPIO.LOW)
    return {"direction": "forward", "speed": speed}

def motor_backward(speed=100):
    if GPIO_AVAILABLE:
        GPIO.output(MOTOR_PIN_1, GPIO.LOW)
        pwm2 = GPIO.PWM(MOTOR_PIN_2, 100)
        pwm2.start(speed)
    return {"direction": "backward", "speed": speed}

def motor_stop():
    if GPIO_AVAILABLE:
        GPIO.output(MOTOR_PIN_1, GPIO.LOW)
        GPIO.output(MOTOR_PIN_2, GPIO.LOW)
    return {"direction": "stopped", "speed": 0}

# 步进电机控制
def stepper_move(steps, direction=1, delay=0.01):
    if GPIO_AVAILABLE:
        # 步进电机步进序列
        seq = [[1, 0, 0, 0],
               [1, 1, 0, 0],
               [0, 1, 0, 0],
               [0, 1, 1, 0],
               [0, 0, 1, 0],
               [0, 0, 1, 1],
               [0, 0, 0, 1],
               [1, 0, 0, 1]]
        
        for _ in range(steps):
            for i in range(8):
                for pin in range(4):
                    GPIO.output(STEP_PINS[pin], seq[i if direction > 0 else 7-i][pin])
                time.sleep(delay)
    return {"steps": steps, "direction": "clockwise" if direction > 0 else "counterclockwise"}

# 距离传感器
def get_distance():
    if GPIO_AVAILABLE:
        # 发送10us的触发脉冲
        GPIO.output(DISTANCE_TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(DISTANCE_TRIG, GPIO.LOW)
        
        # 等待回波
        pulse_start = time.time()
        timeout = pulse_start + 0.1  # 设置超时
        while GPIO.input(DISTANCE_ECHO) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return -1
        
        pulse_end = time.time()
        timeout = pulse_end + 0.1  # 设置超时
        while GPIO.input(DISTANCE_ECHO) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return -1
        
        # 计算距离
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # 声速 * 时间 / 2
        return round(distance, 2)
    else:
        # 模拟模式返回随机距离
        import random
        return round(random.uniform(10, 100), 2)

# 巡线传感器
def get_line_status():
    if GPIO_AVAILABLE:
        return GPIO.input(LINE_SENSOR_PIN)
    else:
        import random
        return random.choice([0, 1])

# 温度传感器
def get_temperature():
    if GPIO_AVAILABLE:
        # 此处应实现读取温度传感器的代码
        # 这里只是简单模拟
        pass
    
    import random
    return round(random.uniform(20, 30), 1)

# 清理GPIO
def cleanup():
    if GPIO_AVAILABLE:
        GPIO.cleanup()
        print("GPIO已清理")
    else:
        print("模拟模式: GPIO清理被跳过")

# 在导入时自动初始化
init()