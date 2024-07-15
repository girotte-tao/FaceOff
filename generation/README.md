
# Generation README

## Environment Setup

1. **Create Conda Environment**

   First, create a Conda environment with Python 3.10:

   ```bash
   conda create -n faceswap_env python=3.10
   conda activate faceswap_env
   ```

2. **Install Dependencies**

   Next, install the required dependencies using the provided `requirements_nvidia.txt` file:

   ```bash
   pip install -r requirements_nvidia.txt
   ```

## Download GFPGAN Model

Download the GFPGAN model using the following command:

```bash
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -P gfpgan/pretrained_models
```

## Preparing Videos

1. **Add Source and Destination Videos**

   In the `/swap_videos` directory, create subfolders for each video pair. Each subfolder should contain a source video and a destination video.

   ```
   swap_videos/
   ├── pair1/
   │   ├── source.mp4
   │   └── destination.mp4
   ├── pair2/
   │   ├── source.mp4
   │   └── destination.mp4
   └── ...
   ```

## Run the Pipeline

Start the face swap and super-resolution process by running the `fs_pipeline`. This will process each video pair in the subfolders:

```bash
python fs_pipeline.py
```

The pipeline will automatically swap faces and apply super-resolution to each video pair.

## Common Issues

### GFPGAN Runtime Error

When running GFPGAN, you may encounter the following error:

```
File "/lib/python3.10/site-packages/basicsr/data/degradations.py", line 8, in <module>
    from torchvision.transforms.functional_tensor import rgb_to_grayscale
ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor'
```

To resolve this issue, edit the `degradations.py` file in the `basicsr` package. Change the line:

```python
from torchvision.transforms.functional_tensor import rgb_to_grayscale
```

to:

```python
from torchvision.transforms.functional import rgb_to_grayscale
```
