
# Faceoff

## Project Introduction
Faceoff is a comprehensive pipeline for deepfake generation and detection. You can use this project for either generation or detection. The project is divided into four main parts: generation, generation evaluation, detection, and prototype system (including server and UI). You can run the project directly or find our repository on GitHub: [https://github.com/girotte-tao/FaceOff](https://github.com/girotte-tao/FaceOff).

This project utilizes multiple projects/features/submodules, requiring multiple environments. Different environments depend on different packages, making it impossible to run all project contents in a single environment.

To clone the repository from GitHub and use VFD or ICT, run:

```
git submodule update --init --recursive
```

## 1. Generation
For detailed operation instructions, refer to `generation/README.md`. This feature leverages some code from faceswap.

## 2. Generation Evaluation
This part uses the LLAVA visual language model for evaluation, depending on Ollama.

```
pip install ollama
```

Run the following command in the terminal:

```
ollama run llava:7b
```

Then, place the videos to be evaluated in `FaceOff/evaluation/ollama/videos` and run:

```
python FaceOff/evaluation/ollama/llava_evaluation.py
```

A `results.jsonl` file will be generated in the `FaceOff/evaluation/ollama` directory. To get insights, run:

```
python FaceOff/evaluation/ollama/get_insights.py
```

This will generate a `statistics_llava_evaluation_generated_deepfake.txt` file in the `FaceOff/evaluation/ollama` directory.

## 3. Detection
Three models are available for detection. Install the corresponding environment based on the model you choose. The environment files are located in:

```
conda env create -f environment.yml
```

Subsequent operations need to be performed in the corresponding model environment.
download the dataset from [here]

### Faceoff Model
To train the Faceoff model, download the dataset from [here](https://connecthkuhk-my.sharepoint.com/:u:/g/personal/u3619603_connect_hku_hk/ET83jROEKxRKv39-UDLB-ncBCYkxUcFT8BUcDj8gNl17eQ?e=0TtvYd) and place it in `FaceOff/detection/model/FaceoffModel/data/FakeAVCeleb_v1.2/FakeAVCeleb`.

Run the training script:

```
bash FaceOff/detection/model/FaceoffModel/run_train.sh
```

### VFD Model
Refer to the official README at `FaceOff/detection/model/VFD/README.md`.
1. Download the pretrained model from [this link](https://drive.google.com/drive/folders/17ij0gv4EVYtE0580s7oSZVQtiJzWIiK6) and put them in ./checkpoints/VFD

2. Download the sample dataset from [this link](https://drive.google.com/drive/folders/1lCUQvIfAoGKY9SkVzp85POccMhkARyMo?usp=sharing) and unzip it to ./Dataset/FakeAVCeleb

3. Run the test.py

   ```
   python test_DF.py --dataroot ./Dataset/FakeAVCeleb --dataset_mode DFDC --model DFD --no_flip --checkpoints_dir ./checkpoints  --name VFD
   ```


### ICT Model
Refer to the official README at `FaceOff/detection/model/ICT/README.md`.


1. Download pretrained [ICT Base](https://drive.google.com/drive/folders/1z-dBM4lkR6oizsRH6kXQBIw_8ZSpAs8d) and move it to `PRETRAIN/ICT_BASE`. For the ICT-Reference, download our already bulit [reference set](https://github.com/LightDXY/ICT_DeepFake/releases/download/v0.1.0/ref.pkl) and move it to `PRETRAIN/ICT_BASE`.

2. Extract faces from videos and align them.
    ```
    python -u preprosee.py
    ```
   This is a simple example, modify the input/output path for different datasets.
Download our pretrained [ICT Base](https://github.com/LightDXY/ICT_DeepFake/releases/download/v0.1.0/ICT_Base.pth) and move it to `PRETRAIN/ICT_BASE`. For the ICT-Reference, download our already bulit [reference set](https://github.com/LightDXY/ICT_DeepFake/releases/download/v0.1.0/ref.pkl) and move it to `PRETRAIN/ICT_BASE`.

3. Run the test script.
```
   bash ict_test.sh
      --name           pretrain model name
      --aug_test       test robustness toward different image aumentation
```
### Run with Adapter
To use the adapter for inference, ensure to switch environments and update the video path. Run:

```
python FaceOff/evaluation/adapter/modelAdapter.py
```

To perform an overall detect using the adapter, run:

```
python FaceOff/evaluation/adapter/modelAdapterEval.py
```

## 4. Prototype System
The backend uses Python Flask:

```
pip install flask==1.1.2
python FaceOff/server/app.py
```

The frontend uses React. Install Node.js, npm, and Yarn:

- Node.js: v22.4.1
- npm: v10.8.1
- Yarn: v1.22.21

Navigate to the UI directory and start the frontend:

```
cd FaceOff/ui
yarn install 
yarn start
```

For any questions, please contact [taowarewt@gmail.com](mailto:taowarewt@gmail.com).
