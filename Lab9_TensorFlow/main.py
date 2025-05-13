from modules.ImageClassifier import ImageClassifier
from modules.ObjectDetector import ObjectDetector
from modules.WEBCAM import WEBCAM

# 创建图像分类器
classifier = ImageClassifier(
    model_path='data/mobilenet_v1_1.0_224_quant.tflite',
    label_path='data/labels_mobilenet_quant_v1_224.txt'
)

# 创建对象检测器
detector = ObjectDetector(
    model_path='data/detect.tflite',
    label_path='data/coco_labels.txt'
)

# 创建网络摄像头
webcam = WEBCAM()

# 添加物体分类处理器
webcam.add_filters(classifier.classify_frame)

# 添加物体检测处理器
webcam.add_filters(detector.detect_frame)

# 运行服务器
webcam.run()