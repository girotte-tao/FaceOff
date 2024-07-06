import random
import cv2
import json
import os
import shutil
from evaluation.ollama.ollama_client import OllamaClient


prompt = """
Please evaluate a given image for deepfake evaluation based on the following criteria. Provide a score for each criterion (1-5) and return the results in a JSON format.
Higher score means it is a better deepfake.

Facial Feature Consistency: Facial features such as eyes, nose, and mouth remain consistent throughout the video without significant distortion or misalignment. A high score indicates excellent consistency of facial features.
Skin Texture Clarity: The skin texture in the video is clear and natural-looking, with detailed and realistic appearances. A higher score signifies a natural and detailed presentation of skin texture.
Edge Naturalness: The edges of objects in the video blend smoothly with the background, without jagged lines or unnatural outlines. A higher score indicates seamless and natural edge transitions.
Artifacts: The video exhibits minimal visual artifacts, with effective compression, smooth color gradients, and minimal pixelation or mosaic-like areas, ensuring a high-quality and clear video appearance.
Overall Quality: The final overall quality score is determined by the combined scores of these criteria. A higher overall score reflects a higher-quality deepfake video. The maximum overall score is 5.

The final output should be a JSON object with the scores(maximum 5 points) for each criterion.
Example JSON output:

{
  "Facial Feature Consistency": X,
  "Skin Texture Clarity": X,
  "Edge Naturalness": X,
  "Artifacts": X
  "Overall Quality": X
}

Note: Replace 'X' with the appropriate score points(0-5). Don't output anything except the JSON object.
"""


def create_tmp_dir():
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def get_random_frame_from_video(video_path, tmp_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    random_frame = random.randint(0, frame_count - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
    ret, frame = cap.read()
    cap.release()
    if ret:
        temp_img_path = os.path.join(tmp_dir, 'random_frame.jpg')
        cv2.imwrite(temp_img_path, frame)
        return temp_img_path
    else:
        raise Exception("Failed to read frame from video")


def process_media_path(media_path, tmp_dir):
    if media_path.lower().endswith(('.mp4', '.avi', '.mov')):
        return get_random_frame_from_video(media_path, tmp_dir)
    return media_path


def get_response_from_client(media_path, prompt):
    client = OllamaClient("llava:7b")
    client.set_instruct(prompt)
    return client.one_round_chat_with_image(prompt, media_path)


def validate_response(response):
    try:
        clean_response = clean_json_string(response)
        json.loads(clean_response)
        return True
    except json.JSONDecodeError:
        return False


def clean_json_string(response):
    start_index = response.find("{")
    end_index = response.rfind("}") + 1
    return response[start_index:end_index]

def process_media_and_get_response(media_path, prompt, max_retries=5):
    tmp_dir = create_tmp_dir()
    try:
        media_path = process_media_path(media_path, tmp_dir)

        for attempt in range(max_retries):
            response = get_response_from_client(media_path, prompt)
            if validate_response(response):
                return clean_json_string(response)
            print(f"Attempt {attempt + 1} failed. Retrying...")

        raise Exception("Failed to get a valid JSON response after maximum retries")
    finally:
        # Clean up the temporary directory
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)


# # 示例调用
# media_path = '/Users/weitao/dev/codeBase/deepfake/FaceOff/evaluation/ollama/1.jpg'
# # prompt = "Describe the content of the image"
# response = process_media_and_get_response(media_path, prompt)
# print(response)
