# 图像采集

import cv2
from datetime import datetime

cap = cv2.VideoCapture(0) # 打开摄像头
ret, frame = cap.read()   # 读取帧

time_stamp = datetime.now().isoformat() # 获取当前时间
cv2.imwrite(f"image_{time_stamp}.jpg", frame) # 保存图像

cap.release() # 释放摄像头