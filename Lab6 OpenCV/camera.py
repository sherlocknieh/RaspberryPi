# 实时摄像头

import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否打开成功
if not cap.isOpened():
    print("摄像头打开失败")
    exit()

while True:
    ret, frame = cap.read() # 获取帧
    if not ret:
        print("获取图像失败")
        break
    cv2.imshow("frame", frame) # 显示图像

    if cv2.waitKey(1) & 0xFF == ord('q'): # 按q键退出
        break

cap.release() # 关闭摄像头
cv2.destroyAllWindows() # 关闭所有窗口