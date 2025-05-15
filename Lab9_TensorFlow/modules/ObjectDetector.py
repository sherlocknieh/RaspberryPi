"""
Run object detection on images, Press ESC to exit the program
For Raspberry PI, please use `import tflite_runtime.interpreter as tflite` instead
"""
import re
import cv2
import numpy as np
from PIL import Image
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import tflite_runtime.interpreter as tflite  # Raspberry PI
# import tensorflow.lite as tflite  # Windows

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class ObjectDetector:
    def __init__(self, model_path, label_path):
        """初始化对象检测器
        Args:
            model_path: TFLite模型路径
            label_path: 标签文件路径
        """
        self.interpreter = self._load_model(model_path)
        self.labels = self._load_labels(label_path)
        
        # 获取模型输入详情
        self.input_details = self.interpreter.get_input_details()
        self.input_index = self.input_details[0]['index']
        
        # 获取期望的输入尺寸
        self.input_shape = self.input_details[0]['shape']
        self.height = self.input_shape[1]
        self.width = self.input_shape[2]

    def _load_labels(self, label_path):
        """加载标签文件"""
        with open(label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels

    def _load_model(self, model_path):
        """加载TFLite模型"""
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def process_image(self, image):
        """处理图像
        Args:
            image: PIL Image对象
        Returns:
            检测到的对象列表，每个对象包含位置和类别ID
        """
        input_data = np.expand_dims(image, axis=0)

        self.interpreter.set_tensor(self.input_index, input_data)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        positions = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))
        classes = np.squeeze(self.interpreter.get_tensor(output_details[1]['index']))
        scores = np.squeeze(self.interpreter.get_tensor(output_details[2]['index']))

        result = []
        for idx, score in enumerate(scores):
            if score > 0.5:
                result.append({'pos': positions[idx], '_id': classes[idx]})

        return result

    def draw_results(self, frame, result, camera_width=640, camera_height=480):
        """在图像上绘制检测结果
        Args:
            frame: OpenCV图像帧
            result: 检测结果列表
            camera_width: 相机宽度
            camera_height: 相机高度
        Returns:
            添加了检测框的图像帧
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        size = 0.6
        color = (255, 0, 0)
        thickness = 1

        for obj in result:
            pos = obj['pos']
            _id = obj['_id']

            x1 = int(pos[1] * camera_width)
            x2 = int(pos[3] * camera_width)
            y1 = int(pos[0] * camera_height)
            y2 = int(pos[2] * camera_height)

            cv2.putText(frame, self.labels[_id], (x1, y1), font, size, color, thickness)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

        return frame

    def detect_frame(self, frame):
        """处理单帧图像
        Args:
            frame: OpenCV格式的图像帧
        Returns:
            处理后的图像帧
        """
        # 转换图像格式
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((self.width, self.height))
        
        # 检测物体
        result = self.process_image(image)
        
        # 绘制结果
        frame = self.draw_results(frame, result)

        # 猫咪位置跟踪
        offsets = (0, 0)
        for obj in result:
            if obj['_id'] == 16:  # cat id
                pos = obj['pos']
                print("cat position: ", pos)
                # 计算猫中心点坐标
                center_x = int((pos[1] + pos[3]) / 2 * CAMERA_WIDTH)
                center_y = int((pos[0] + pos[2]) / 2 * CAMERA_HEIGHT)
                print("cat center: ", center_x, center_y)
                # 计算猫中心点偏离屏幕中心点的坐标
                offset_x = int(center_x - CAMERA_WIDTH / 2)
                offset_y = -int(center_y - CAMERA_HEIGHT / 2)
                print("cat offset: ", offset_x, offset_y)
                offsets = (offset_x, offset_y)

        return offsets, frame

if __name__ == "__main__":

    detector = ObjectDetector(
        model_path = 'data/detect.tflite',
        label_path = 'data/coco_labels.txt'
        )

    cap = cv2.VideoCapture(0)
    pos = None
    while True:
        ret, frame = cap.read()

        result,frame = detector.detect_frame(frame)
        

        cv2.imshow('Object Detection', frame)
        key = cv2.waitKey(1)
        if key == 27:  # esc
            break

    cap.release()
    cv2.destroyAllWindows()