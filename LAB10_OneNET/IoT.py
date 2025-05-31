"""
pip install requests adafruit-circuitpython-dht
"""

# 温湿度传感器
import adafruit_dht
import board
import time

# 物联网平台
import requests
import json

dhtDevice = adafruit_dht.DHT11(board.D18) # DHT11传感器, 连接到GPIO18


product_id = "DuE2rcXUKn"
device_name = "PC"
token = "version=2018-10-31&res=products%2FDuE2rcXUKn%2Fdevices%2FPC&et=1780220457&method=sha256&sign=wm%2FGRf8tq8aNbNspkNlHRCm9vxMB%2FqWWoJqD4KzACeQ%3D"


post_address = "https://open.iot.10086.cn/fuse/http/device/thing/property/post"
post_params = f"?topic=$sys/{product_id}/{device_name}/thing/property/post&protocol=http"


get_address = "https://iot-api.heclouds.com/thingmodel/query-device-property"
get_params = f"?device_name={device_name}&product_id={product_id}"

headers = {
    "Content-Type": "application/json",
    "token": token,
    "Authorization": token
}

# 从物联网平台获取数据

get_data = requests.get(get_address+get_params, headers=headers)
print(get_data.json())

# 返回结果:
# {
#     "code": 0,
#     "data": [
#         {
#             "identifier": "humi",
#             "time": 1748686065394,
#             "value": "51",
#             "data_type": "float",
#             "access_mode": "读写",
#             "name": "湿度"
#         },
#         {
#             "identifier": "temp",
#             "time": 1748686065394,
#             "value": "40",
#             "data_type": "float",
#             "access_mode": "读写",
#             "name": "温度"
#         }
#     ],
#     "msg": "succ",
#     "request_id": "23e51ce6203b4ada8949856eb69da2e3"
# }


while True:
    try:
        temperature = dhtDevice.temperature        # 温度
        humidity = dhtDevice.humidity                # 湿度
        print("Temp:  {:.1f} C    Humidity: {}% ".format(temperature, humidity))
        
        data = {
            "id": "123",
            "version": "1.0",
            "params": {
                "temp":{
                    "value": temperature,
                },
                "humi":{
                    "value": humidity,
                }
            }   
        }
        post_data = requests.post(post_address+post_params, headers=headers, data=json.dumps(data))
        print(post_data.json())  # {'errno': 0, 'error': 'succ'} 说明数据发送成功

    except RuntimeError as error:               # 读取数据出错
        print(error.args[0])                    # 打印错误信息
        time.sleep(2.0)                         # 等待2秒后继续
        continue                                # 跳过本次循环
    except Exception as error:                # 其他错误
        dhtDevice.exit()                      # 释放资源
        raise error                           # 抛出错误
    time.sleep(2.0)                # 2秒更新一次数据


