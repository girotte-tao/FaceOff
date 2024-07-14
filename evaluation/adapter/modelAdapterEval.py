import subprocess
import os
import pandas as pd
from tqdm import tqdm 

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
                return None

            output_lines = result.stdout.strip().splitlines()
            last_line = output_lines[-1]
            return last_line.lower() == "true"
        except Exception as e:
            print(f"Exception occurred: {e}")
            return None


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

    def detect_all(self, folder_path):
        results = []
        videos = [f for f in os.listdir(folder_path) if f.endswith(('.mp4'))]

     
        total_tasks = len(videos) * len(self.models)
        with tqdm(total=total_tasks) as pbar:
            for video in videos:
                video_path = os.path.join(folder_path, video)
                for model_name in self.models:
                    is_deepfake = self.detect(model_name, video_path)
                    results.append({
                        'video': video,
                        'model': model_name,
                        'is_deepfake': is_deepfake
                    })
                    
                    pbar.update(1)

        return results

# examples
adapter = DeepfakeDetectionAdapter()
adapter.add_model("VFD", "VFD", "/userhome/cs2/u3619712/VFD/detect1.py")
adapter.add_model("MRDF", "mrdf2", "/userhome/cs2/u3619712/MRDF/detect1.py")
adapter.add_model("ICT", "ICT0", "/userhome/cs2/u3619712/ICT_DeepFake/detect1.py")

folder_path = "/userhome/cs2/u3619712/FaceOff/evaluation/video_test" 
folder_path = "/userhome/cs2/u3619712/FaceOff/evaluation/video_eval" 

results = adapter.detect_all(folder_path)

# result
df = pd.DataFrame(results)
output_path = "/userhome/cs2/u3619712/FaceOff/evaluation/detection_results3.csv"
df.to_csv(output_path, index=False)
print(f"detection result save in {output_path}")

