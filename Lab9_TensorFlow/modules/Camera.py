import threading
import cv2


class Camera:
    def __init__(self):
        self.camera = None
        self._lock = threading.Lock()  # 添加线程锁

    def open(self):
        with self._lock:
            if self.camera is None or not self.camera.isOpened():
                self.camera = cv2.VideoCapture(0)
                if not self.camera.isOpened():
                    print("错误：无法打开摄像头")
                    return None
            print('摄像头已打开')
            return self

    def get_frame(self):
        with self._lock:
            if self.camera is None or not self.camera.isOpened():
                print("错误：摄像头未打开")
                return None
            success, frame = self.camera.read()
            if not success:
                print("错误：无法读取帧")
                return None
            return frame
    
    def close(self):
        with self._lock:
            if self.camera is not None and self.camera.isOpened():
                self.camera.release()
                print("摄像头已释放")
                self.camera = None
    
    def isOpened(self):
        with self._lock:
            return self.camera is not None and self.camera.isOpened()

    def __del__(self):
        self.close()



if __name__ == '__main__':
    camera = Camera()
    camera.open()
    while True:
        frame = camera.get_frame()
        cv2.imshow("camera", frame)
        key = cv2.waitKey(1)
        if key == 27:  # esc
            break
    cv2.destroyAllWindows()