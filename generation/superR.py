import os
import cv2
import subprocess
from gfpgan import GFPGANer

class VideoEnhancer:
    def __init__(self):
        pass

    def extract_frames(self,video_path, output_folder,fps=60):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        cmd = f'ffmpeg -i {video_path} -vf fps={fps} {output_folder}/frame_%04d.png'
        subprocess.run(cmd, shell=True)

    def enhance_frames(self,input_folder, output_folder,gfpgan_model_path):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        gfpgan = GFPGANer(model_path=gfpgan_model_path)
        frame_files = sorted(os.listdir(input_folder))

        for frame_file in frame_files:
            input_path = os.path.join(input_folder, frame_file)
            output_path = os.path.join(output_folder, frame_file)

            img = cv2.imread(input_path)
            _, _, restored_img = gfpgan.enhance(img, has_aligned=False, only_center_face=False)
            cv2.imwrite(output_path, restored_img)

    def rebuild_video(self,input_folder, output_video_path, fps=60):
        cmd = f'ffmpeg -framerate {fps} -i {input_folder}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p {output_video_path}'
        subprocess.run(cmd, shell=True)

    def enhance_video(self,input_video_path, output_video_path,gfpgan_model_path):
        # Step 1: Extract frames
        base_dir = os.path.dirname(input_video_path)
        frames_folder = os.path.join(base_dir,'frames')
        enhanced_frames_folder = os.path.join(base_dir,'enhanced_frames')
        self.extract_frames(input_video_path, frames_folder)
        
        # Step 2: Enhance frames
        self.enhance_frames(frames_folder, enhanced_frames_folder,gfpgan_model_path)
        
        # Step 3: Rebuild video
        self.rebuild_video(enhanced_frames_folder, output_video_path)

        # Cleanup
        subprocess.run(f'rm -rf {frames_folder}', shell=True)
        subprocess.run(f'rm -rf {enhanced_frames_folder}', shell=True)

# Example usage
# input_video = './B_converted_150000.MOV'
# output_video = './B_SP2.mp4'
# gfpgan_model = './gfpgan/pretrained_models/GFPGANv1.3.pth'
# VE = VideoEnhancer()
# VE.enhance_video(input_video, output_video, gfpgan_model)