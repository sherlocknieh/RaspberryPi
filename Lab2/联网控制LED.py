# dweet.io 联网控制树莓派LED

# 需要的库
import requests
from gpiozero import LED
from time import sleep

URL = 'https://dweet.io'

class DweetLED:
    def __init__(self, led_pin, thing_name='my_thing'):
        self.thing_name = thing_name
        self.led = LED(led_pin)
        self.led.off()
        self.state = None
        self.info()     # 打印初始信息

    def info(self):     # 初始化
        print("LED Control URLs - Try them in your web browser:")
        print("  On    : " + URL + "/dweet/for/" + self.thing_name + "?state=on")
        print("  Off   : " + URL + "/dweet/for/" + self.thing_name + "?state=off")
        print("  Blink : " + URL + "/dweet/for/" + self.thing_name + "?state=blink\n")

    def get(self):      # 状态更新
        resource = URL + '/get/latest/dweet/for/' + self.thing_name

        try:
            r = requests.get(resource)
            r.raise_for_status()

            dweet = r.json()  # return a Python dict.

            dweet_content = None

            if dweet['this'] == 'succeeded':
                # We're just interested in the dweet content property.
                dweet_content = dweet['with'][0]['content']

            self.state = dweet_content

        except requests.exceptions.RequestException as e:
            print(f'Error getting last dweet: {e}')

    def set(self):      # 执行
        if not self.state:
            return
        led_state = self.state.get('led_state')
        if led_state == 'on':
            self.led.on()
        elif led_state == 'off':
            self.led.off()
        elif led_state == 'blinking':
            self.led.blink()

    def run(self):      # 主循环
        while True:
            self.get()
            self.set()
            sleep(1)


if __name__ == '__main__':
    dweet_led = DweetLED(3)
    dweet_led.run()