import subprocess
import os

class DeepfakeModel:
    def __init__(self, name, conda_env, script_path):
        self.name = name
        self.conda_env = conda_env
        self.script_path = script_path

    def run(self, video_path):
        command = f"conda run -n {self.conda_env} python {self.script_path} {video_path}"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error running model {self.name}: {result.stderr}")
                return False

            output = result.stdout.strip()
            return output.lower() == "true"
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
adapter.add_model("ICT", "VFD0", "/path/to/model1/predict.py")
adapter.add_model("VFD", "env_model2", "")

video_path = "/path/to/video.mp4"
model_name = "model1"
is_deepfake = adapter.detect(model_name, video_path)
print(f"Is the video a deepfake? {is_deepfake}")
