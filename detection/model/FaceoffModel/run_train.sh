#!/bin/bash
# 获取当前时间，格式为YYYYMMDD-HHMMSS

mkdir -p log/train

current_time=$(date +"%Y%m%d-%H%M%S")
# 构建日志文件名
log_file="log/train/log_train_FOM_${current_time}.log"
# 运行python命令并将输出重定向到日志文件
CUDA_VISIBLE_DEVICES=0 python train.py \
  --model_type FOM_CE --save_name FOM_CE \
  --data_root /userhome/cs2/u3619712/MRDF/data/FakeAVCeleb_v1.2 \
  --batch_size 8\
  --dataset fakeavceleb > "${log_file}" 2>&1

    # --data_root ./data/FakeAVCeleb_v1.2/ \
