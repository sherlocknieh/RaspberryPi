from flask import Flask, render_template, Response
from .Camera import Camera
import threading
import cv2


class ClientCounter:
    def __init__(self):
        self.active_clients = 0
        self.lock = threading.Lock()

    def add_client(self):
        """增加客户端计数"""
        with self.lock:
            self.active_clients += 1
            print(f"客户端连接，当前活动客户端数：{self.active_clients}")
            return self.active_clients

    def remove_client(self):
        """减少客户端计数"""
        with self.lock:
            if self.active_clients > 0:
                self.active_clients -= 1
                print(f"客户端断开，当前活动客户端数：{self.active_clients}")
            return self.active_clients

class Stream:
    def __init__(self, camera=None, source=None):
        # 创建 Flask 应用
        self.app = Flask(__name__)
        self.counter = ClientCounter()

        self.camera = camera
        self.source = source

        # 定义路由
        self.app.route('/')(self.index)
        self.app.route('/stream')(self.stream)
        self.app.route('/close', methods=['POST'])(self.close)
        
    # 主页响应函数
    def index(self):
        self.counter.add_client()
        return render_template('camera.html')

    # 视频流响应函数
    def stream(self):
        #self.camera.open()
        return Response(
            self.stream_gen(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    
    # 关闭网页响应函数
    def close(self):
        self.counter.remove_client()
        # if self.counter.active_clients == 0:
        #     self.camera.close()
        return 'OK'

    # 视频流生成器
    def stream_gen(self):
        while self.counter.active_clients > 0:
            if self.source is None:
                frame = self.camera.get_frame()
            else:
                frame = self.source.pop()
            if frame is not None:
                frame = cv2.imencode('.jpg', frame)[1].tobytes()    # 编码为 jpg 字节流格式
                frame = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                yield frame

    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    stream = Stream()
    stream.run()
