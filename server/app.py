import os
import sys
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设 app.py 文件位于 FaceOff/server/ 目录下）
project_root = os.path.abspath(os.path.join(current_dir, '../..'))

# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)

from flask import Flask, request, jsonify
from FaceOff.evaluation.adapter import modelAdapter

app = Flask(__name__)

adapter = modelAdapter.DeepfakeDetectionAdapter()
adapter.add_model("VFD", "VFD0", "/userhome/cs2/u3619712/VFD/detect1.py")
adapter.add_model("MRDF", "mrdf2", "/userhome/cs2/u3619712/MRDF/detect1.py")
adapter.add_model("ICT", "ICT0", "/userhome/cs2/u3619712/ICT_DeepFake/detect1.py")

video_path = "'/userhome/cs2/u3619712/MRDF/data/FakeAVCeleb_v1.2/FakeAVCeleb/RealVideo-RealAudio/Asian-South/men/id00032/00028.mp4'"


@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    model = data.get('model')
    # video_path = data.get('video_path')
    
    # 模拟深伪检测结果
    # is_deepfake = True
    is_deepfake = adapter.detect(model, video_path)

    
    response = {
        "message": f"Call detection model {model} successfully!",
        "data": {
            "model": model,
            "video_path": video_path,
            "is_deepfake": is_deepfake
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
