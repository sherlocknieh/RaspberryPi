"""
Run classification on Camera, Press ESC to exit the program
For Raspberry PI, please use `import tflite_runtime.interpreter as tflite` instead
"""
import cv2
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class ImageClassifier:
    def __init__(self, model_path, label_path):
        """初始化分类器"""
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
        with open(label_path, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def _load_model(self, model_path):
        """加载TFLite模型"""
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def process_frame(self, frame, k=3):
        """处理单帧图像"""
        # 转换图像格式和大小
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((self.width, self.height))
        
        # 处理图像
        input_data = np.expand_dims(image, axis=0)
        self.interpreter.set_tensor(self.input_index, input_data)
        self.interpreter.invoke()

        # 获取输出
        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        output_data = np.squeeze(output_data)

        # 获取top-k结果
        top_k = output_data.argsort()[-k:][::-1]
        results = []
        for _id in top_k:
            score = float(output_data[_id] / 255.0)
            label = self.labels[_id]
            results.append((label, score))

        return results

    def draw_results(self, frame, results):
        """在图像上绘制分类结果"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        size = 0.6
        color = (255, 0, 0)  # 蓝色
        thickness = 1

        for idx, (label, score) in enumerate(results):
            x = 12
            y = 24 * idx + 24
            cv2.putText(frame, f'{label} - {score:.4f}',
                      (x, y), font, size, color, thickness)
        
        return frame

    def classify_frame(self, frame):
        """处理单帧图像"""
        results = self.process_frame(frame)
        frame = self.draw_results(frame, results)
        return frame

if __name__ == "__main__":

    model_path = 'data/mobilenet_v1_1.0_224_quant.tflite'
    label_path = 'data/labels_mobilenet_quant_v1_224.txt'
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 15)

    classifier = ImageClassifier(model_path, label_path)

    # Process Stream
    while True:
        ret, frame = cap.read()

        frame = classifier.classify_frame(frame)

        cv2.imshow('Image Classification', frame)

        key = cv2.waitKey(1)
        if key == 27:  # esc
            break

    cap.release()
    cv2.destroyAllWindows()