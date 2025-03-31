# 实时摄像头

import cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("摄像头打开失败")
    exit()

while cap.isOpened():
    ret, frame = cap.read() # 读取帧
    if not ret:
        print("摄像头读取失败")
        break
    cv2.imshow("frame", frame) # 显示图像
    if cv2.waitKey(1) & 0xFF == ord('q'): # 按q键退出
        break

cap.release()
cv2.destroyAllWindows()