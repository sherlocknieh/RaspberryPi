from modules.ObjectDetector import ObjectDetector
from modules.ServoGimbal import ServoGimbal
from modules.Camera import Camera
from modules.Stream import Stream
from modules.Deque import Deque
import threading

raw_frames = Deque(maxlen=5)
frames = Deque(maxlen=5)
offsets = Deque(maxlen=5)

camera = Camera()
camera.open()
servo = ServoGimbal(14, 15)
detector = ObjectDetector(
    model_path='data/detect.tflite', 
    label_path='data/coco_labels.txt'
)

def capture_thread():
    while True:
        if not camera.isOpened():
            continue
        frame = camera.get_frame()
        raw_frames.append(frame)

def detect_thread():
    while True:
        frame = raw_frames.pop(30)
        result, marked_frame = detector.detect_frame(frame)
        offsets.append(result)
        frames.append(marked_frame)

def servo_thread():
    while True:
        dx, dy = offsets.pop(30)
        servo.track_to(dx, dy)


threading.Thread(target=capture_thread, daemon=True).start()
threading.Thread(target=detect_thread, daemon=True).start()
threading.Thread(target=servo_thread, daemon=True).start()
stream = Stream(camera=camera, source=frames).run()
