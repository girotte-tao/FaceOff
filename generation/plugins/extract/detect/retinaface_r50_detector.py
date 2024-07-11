# 在retinaface_r50_detector.py文件中
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# class RetinaFaceR50Detector(_base.Detector):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.model = RetinaFace('/new_models/retinaface-R50/R50-symbol.json')  # 加载你的模型

#     def detect_faces(self, image):
#         # 使用你的模型检测人脸
#         detector = insightface.model_zoo.get_model('/new_models/buffalo_l/det_10g.onnx')
#         detector.prepare(ctx_id=0, input_size=(640, 640))
#         boxes = self.model.detect_faces(image)
#         return boxes

app = FaceAnalysis(allowed_modules=['detection']) # enable detection model only
app.prepare(ctx_id=0, det_size=(640, 640))
# detector = insightface.model_zoo.get_model('/userhome/cs2/u3619674/faceswap/new_models/buffalo_l/det_10g.onnx')
# detector.prepare(ctx_id=0, input_size=(640, 640))
img = ins_get_image('/userhome/cs2/u3619674/faceswap/swap_videos/group1/A_images/A_000001_0')
faces = app.get(img)
print(faces)
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)
