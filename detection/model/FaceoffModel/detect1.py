import os
import numpy as np
import torch
from torch.nn import functional as F
from python_speech_features import logfbank
from scipy.io import wavfile
import model.avhubert.utils as custom_utils

import cv2
import torch
import sys
import numpy as np
from torch.utils.data import DataLoader, Dataset
from pytorch_lightning import LightningModule
from model import FOM_CE

def load_video(video_name, scale_percent, image_mean, image_std):
    feats = custom_utils.load_video(video_name, scale_percent)
    transform = custom_utils.Compose([
        custom_utils.Normalize(0.0, 255.0),
        custom_utils.CenterCrop((100, 100)),
        custom_utils.Normalize(image_mean, image_std)])
    feats = transform(feats)
    return feats

def stacker(feats, stack_order):
    feat_dim = feats.shape[1]
    if len(feats) % stack_order != 0:
        res = stack_order - len(feats) % stack_order
        res = np.zeros([res, feat_dim]).astype(feats.dtype)
        feats = np.concatenate([feats, res], axis=0)
    feats = feats.reshape((-1, stack_order, feat_dim)).reshape(-1, stack_order * feat_dim)
    return feats

def crop_to_max_size(wav, target_size, random_crop=False):
    size = len(wav)
    diff = size - target_size
    if diff <= 0:
        return wav, 0
    start = 0
    if random_crop:
        start = np.random.randint(0, diff + 1)
    end = start + target_size
    return wav[start:end], start

def collater_audio(audios, audio_size, pad_audio=False):
    audio_feat_shape = list(audios[0].shape[1:])
    collated_audios = audios[0].new_zeros([len(audios), audio_size]+audio_feat_shape)
    padding_mask = torch.BoolTensor(len(audios), audio_size).fill_(False)
    for i, audio in enumerate(audios):
        diff = len(audio) - audio_size
        if diff == 0:
            collated_audios[i] = audio
        elif diff < 0:
            collated_audios[i] = torch.cat(
                [audio, audio.new_full([-diff]+audio_feat_shape, 0.0)]
            )
            padding_mask[i, diff:] = True
        else:
            collated_audios[i], _ = crop_to_max_size(audio, audio_size)
    if len(audios[0].shape) == 2:
        collated_audios = collated_audios.transpose(1, 2)  # [B, T, F] -> [B, F, T]
    else:
        collated_audios = collated_audios.permute((0, 4, 1, 2, 3)).contiguous()  # [B, T, H, W, C] -> [B, C, T, H, W]
    return collated_audios, padding_mask

def process_video_audio(video_path: str, root: str = "data", stack_order_audio: int = 4, 
                        image_mean: float = 0.421, image_std: float = 0.165, scale_percent: float = 0.5, pad_audio = False) -> dict:
    
    video_fn = video_path
    audio_fn = video_fn.replace('.mp4', '.wav')

    video_feats = load_video(video_fn, scale_percent, image_mean, image_std)

    sample_rate, wav_data = wavfile.read(audio_fn)
    audio_feats = logfbank(wav_data, samplerate=sample_rate).astype(np.float32)
    audio_feats = stacker(audio_feats, stack_order_audio)

    if audio_feats is not None and video_feats is not None:
        diff = len(audio_feats) - len(video_feats)
        if diff < 0:
            audio_feats = np.concatenate([audio_feats, np.zeros([-diff, audio_feats.shape[-1]], dtype=audio_feats.dtype)])
        elif diff > 0:
            audio_feats = audio_feats[:-diff]

    audio_tensor = torch.from_numpy(audio_feats.astype(np.float32)) if audio_feats is not None else None
    video_tensor = torch.from_numpy(video_feats.astype(np.float32)) if video_feats is not None else None

    audio_size = len(audio_tensor) if audio_tensor is not None else len(video_tensor)
    
    if audio_tensor is not None:
        with torch.no_grad():
            audio_tensor = F.layer_norm(audio_tensor, audio_tensor.shape[1:])

    max_sample_size = 500
    audio_size = min(audio_size, max_sample_size)

    collated_audio, padding_mask = collater_audio([audio_tensor], audio_size) if audio_tensor is not None else (None, None)
    collated_video, padding_mask = collater_audio([video_tensor], audio_size) if video_tensor is not None else (None, None)

    return {"video": collated_video, "audio": collated_audio, "padding_mask": padding_mask}

def evaluate_model(video_audio_data, model_checkpoint_path):
    model = FOM_CE.load_from_checkpoint(model_checkpoint_path)
    model.eval()
    logits, _, _, _, _ = model(video_audio_data['video'], video_audio_data['audio'], video_audio_data['padding_mask'])
    preds = torch.argmax(torch.nn.Softmax(dim=1)(logits), dim=1)
    res = preds.cpu().numpy().tolist()
    return res

def is_Deepfake(res):
    return res[0] != 1


if __name__ == '__main__':
    
    video_path = sys.argv[2]
    checkpoint_path = ''

    result = process_video_audio(video_path)
    res = evaluate_model(result, checkpoint_path)

    is_real = is_Deepfake(res)
    print(is_real)
