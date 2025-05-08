import requests
import json


address = "https://open.iot.10086.cn/fuse/http/device/thing/property/post"

parameters = "?topic=$sys/DuE2rcXUKn/PC/thing/property/post&protocol=http"

headers = {
    "Content-Type": "application/json",
    "token": "version=2018-10-31&res=products%2FDuE2rcXUKn%2Fdevices%2FPC&et=1757334264&method=md5&sign=QO%2BCXWoE6p3AnQTe%2B2KBPg%3D%3D"
}

data = {
    "id": "123",
    "version": "1.0",
    "params": {
        "temp":{
            "value": 36.50989,
        },
        "humi":{
            "value": 50.234,
        }
    }   
}


response = requests.post(address+parameters, headers=headers, data=json.dumps(data))

print(response.json())