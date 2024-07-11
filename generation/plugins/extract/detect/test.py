from PIL import Image
from retinaface_r50_detector import RetinaFaceR50Detector

# 加载你的模型
detector = RetinaFaceR50Detector()

# 加载一张测试图像
image = Image.open('/swap_videos/group1/A_images/A_000001_0.png')

# 使用你的模型检测图像中的人脸
boxes = detector.detect_faces(image)

# 打印检测到的人脸的边界框
for box in boxes:
    print(box)
