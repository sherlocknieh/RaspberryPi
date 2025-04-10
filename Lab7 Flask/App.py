import cv2
from flask import Flask, render_template, Response
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
led_status = 'off'

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("摄像头打开失败")
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n\r\n'
        return
    logger.info("摄像头打开成功")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            success, frame = cap.read()
            if not success:
                logger.warning("读取帧失败")
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                logger.warning("编码帧失败")
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        logger.info("客户端断开（刷新或离开）")
    except Exception as e:
        logger.error(f"生成器异常: {e}")
    finally:
        if cap.isOpened():
            cap.release()
            logger.info("摄像头已释放")
        else:
            logger.warning("摄像头已在释放前关闭")
        time.sleep(0.5)  # 确保设备重置

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/motor')
def motor():
    return render_template('motor.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/sensor')
def sensor():
    return render_template('sensor.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', threaded=False)
    except KeyboardInterrupt:
        logger.info("程序手动终止")
    finally:
        logger.info("程序结束，检查摄像头状态")