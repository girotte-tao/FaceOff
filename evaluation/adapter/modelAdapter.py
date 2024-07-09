import subprocess
import os

class DeepfakeModel:
    def __init__(self, name, conda_env, script_path):
        self.name = name
        self.conda_env = conda_env
        self.script_path = script_path

    def run(self, video_path):
        command = f"conda run -n {self.conda_env} python {self.script_path} --video_path {video_path}"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error running model {self.name}: {result.stderr}")
                return False

            output_lines = result.stdout.strip().splitlines()
            last_line = output_lines[-1]
            return last_line.lower() == "true"
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False


class DeepfakeDetectionAdapter:
    def __init__(self):
        self.models = {}

    def add_model(self, name, conda_env, script_path):
        self.models[name] = DeepfakeModel(name, conda_env, script_path)

    def detect(self, model_name, video_path):
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} is not configured.")

        model = self.models[model_name]
        return model.run(video_path)


# 示例使用
adapter = DeepfakeDetectionAdapter()
# adapter.add_model("ICT", "VFD0", "/path/to/model1/predict.py")
adapter.add_model("VFD", "VFD0", "/userhome/cs2/u3619712/VFD/detect1.py")
adapter.add_model("MRDF", "mrdf2", "/userhome/cs2/u3619712/MRDF/detect1.py")
adapter.add_model("ICT", "ICT0", "/userhome/cs2/u3619712/ICT_DeepFake/detect1.py")

video_path = "'/userhome/cs2/u3619712/MRDF/data/FakeAVCeleb_v1.2/FakeAVCeleb/RealVideo-RealAudio/Asian-South/men/id00032/00028.mp4'"
model_name = "VFD"
model_name = "MRDF"
model_name = 'ICT'

is_deepfake = adapter.detect(model_name, video_path)
print(f"Is the video a deepfake? {model_name}: {is_deepfake}")
