from flask import Flask, render_template, Response
import cv2

class WEBCAM:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route('/')(self.index)
        self.app.route('/stream')(self.stream)
        self.filters = []  # 存储帧处理器
        self.cap = None
        
    def add_filters(self, processor):
        """添加帧处理器"""
        self.filters.append(processor)
    
    def index(self):
        return render_template('camera.html')
    
    def stream(self):
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def gen_frames(self):
        self.cap = cv2.VideoCapture(0)
        frame_count = 0
        while True:
            success, frame = self.cap.read()
            frame_count = (frame_count + 1) % 3
            if not success or frame_count < 2:  # 跳帧
                continue
                
            # 依次调用所有帧处理器
            for processor in self.filters:
                frame = processor(frame)
                
            # 编码和传输
            ret, buffer = cv2.imencode('.jpg', frame) # 编码成jpg格式
            frame = buffer.tobytes()                  # 转换成字节流
            frame = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n' # 添加头部和尾部
            yield (frame)
    
    def cleanup(self):
        """清理资源"""
        if self.cap:
            self.cap.release()
            
    def __del__(self):
        self.cleanup()
        
    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    webcam = WEBCAM()
    webcam.run(debug=True)