import os
import subprocess
import logging
import smtplib
from email.message import EmailMessage
from superR import VideoEnhancer
import gc,re

# Description: 发送邮件（主题，正文）
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'sqw0510@gmail.com'
    msg['To'] = '1206199335@qq.com'

    # SMTP 服务器配置，Gmail 589端口发送邮件，993端口接收邮件
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # 登录邮箱，使用google应用专用密码
    server.login('sqw0510@gmail.com', 'nnxc ovvt hkhw inca')
    server.send_message(msg)
    server.quit()

def setup_logging():
    logging.basicConfig(filename='faceswap_pipeline_2.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_execute(command):
    logging.info(f"Executing: {command}")
    os.system(command)
    gc.collect()


def faceswap_pipeline(input_video_1, input_video_2, iterations):
    # Derive paths from the input video paths
    base_dir_1 = os.path.dirname(input_video_1)
    base_dir_2 = os.path.dirname(input_video_2)
    video_name_1 = os.path.splitext(os.path.basename(input_video_1))[0]
    video_name_2 = os.path.splitext(os.path.basename(input_video_2))[0]

    output_images_1 = os.path.join(base_dir_1, f"{video_name_1}_face")
    output_images_2 = os.path.join(base_dir_2, f"{video_name_2}_face")
    model_path = os.path.join(base_dir_2, "model_dfl-sae")
    convert_output = os.path.join(base_dir_2,"converted")
    superR_input = os.path.join(convert_output, f"{video_name_1}_converted.mp4")
    superR_output = os.path.join(convert_output, f"{video_name_1}_SP.mp4")

    # Print and log derived paths for debugging purposes
    logging.info(f"Input Video 1: {input_video_1}")
    logging.info(f"Input Video 2: {input_video_2}")
    logging.info(f"Output Images 1: {output_images_1}")
    logging.info(f"Output Images 2: {output_images_2}")
    logging.info(f"Model Path: {model_path}")
    logging.info(f"Convert Output: {base_dir_1}")
    logging.info(f"Iterations per Train Command: {iterations}")

    start="python faceswap.py"

    # Step 1: Extract faces from the first video
    extract_command_1 = f"{start} extract -i {input_video_1} -o {output_images_1}"
    log_and_execute(extract_command_1)
    send_email(f'extract部分', f'人脸{input_video_1}提取完成')

    # Step 2: Extract faces from the second video
    extract_command_2 = f"{start} extract -i {input_video_2} -o {output_images_2}"
    log_and_execute(extract_command_2)
    send_email(f'extract部分', f'人脸{input_video_2}提取完成')

    # Step 3: Train the model using the extracted images, repeating 10 times to reach 50000 iterations
    train_command = f"{start} train -A {output_images_1} -B {output_images_2} -m {model_path} -t dfl-sae -it {iterations}"
    for i in range(10):
        logging.info(f"Training iteration {(i+1)*iterations}")
        log_and_execute(train_command)
        send_email(f'train部分', f'模型迭代{(i+1)*iterations}完成')

    # Step 4: Convert the video using the trained model
    convert_command = f"{start} convert -i {input_video_1} -o {convert_output} -m {model_path} -w ffmpeg"
    log_and_execute(convert_command)
    send_email(f'convert部分', f'视频转换完成')

    # Step 5: Super-Resolution the converted video
    ve=VideoEnhancer()
    model_path = './gfpgan/pretrained_models/GFPGANv1.3.pth'
    ve.enhance_video(input_video_path=superR_input, output_video_path=superR_output,gfpgan_model_path=model_path)   
    logging.info(f"Super-Resolution Output: {superR_output}")


def main():
    setup_logging()
    # Define the input parameters
    input_video_1 = '/userhome/cs2/u3619674/FaceOff/generation/swap_videos/group4/Trump.mp4'
    input_video_2 = '/userhome/cs2/u3619674/FaceOff/generation/swap_videos/group4/Musk.mp4'
    iterations = 5000

    # Log the start of the process
    logging.info("Starting the faceswap pipeline")

    # Call the faceswap pipeline method with the parameters
    faceswap_pipeline(input_video_1, input_video_2, iterations)

    # Log the end of the process
    logging.info("Faceswap pipeline completed")

if __name__ == '__main__':
    main()
