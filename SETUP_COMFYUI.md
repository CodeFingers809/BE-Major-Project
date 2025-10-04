# ComfyUI Setup for M4 MacBook Air - Sketch to Photo with Face Preservation

## 1. Install ComfyUI

```bash
# Navigate to your project
cd "/Users/ayush/dev/BE PROJECT"

# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install dependencies (optimized for Apple Silicon)
pip install torch torchvision torchaudio
pip install -r requirements.txt

# Install ComfyUI Manager (for easy model downloads)
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..
```

## 2. Download Required Models

### Base Model (Choose ONE for Indian faces):
```bash
# Option A: Realistic Vision (Best for Indian faces)
# Download from: https://civitai.com/models/4201/realistic-vision-v60-b1
# Place in: ComfyUI/models/checkpoints/

# Option B: DreamShaper (Good alternative)
# Download: https://civitai.com/models/4384/dreamshaper
# Place in: ComfyUI/models/checkpoints/
```

### ControlNet Models (REQUIRED for sketch preservation):
```bash
# Create ControlNet directory
mkdir -p ComfyUI/models/controlnet

# Download these models:
# 1. Scribble ControlNet (for sketches)
#    URL: https://huggingface.co/lllyasviel/control_v11p_sd15_scribble
#    File: diffusion_pytorch_model.safetensors
#    Save as: ComfyUI/models/controlnet/control_v11p_sd15_scribble.safetensors

# 2. Lineart ControlNet (for clean lines)
#    URL: https://huggingface.co/lllyasviel/control_v11p_sd15_lineart
#    File: diffusion_pytorch_model.safetensors
#    Save as: ComfyUI/models/controlnet/control_v11p_sd15_lineart.safetensors

# Download helper script
curl -o download_models.sh https://gist.githubusercontent.com/example/controlnet_download.sh
chmod +x download_models.sh
./download_models.sh
```

## 3. Start ComfyUI

```bash
cd ComfyUI
python main.py

# ComfyUI will start on http://127.0.0.1:8188
```

## 4. Workflow Configuration

### Import Workflow JSON (see workflow.json below)
1. Open ComfyUI at http://127.0.0.1:8188
2. Drag and drop the workflow.json file
3. Adjust nodes as needed

### Key Settings for Face Preservation:
- **ControlNet Strength**: 0.9-1.0 (maximum sketch adherence)
- **CFG Scale**: 7-9 (prompt following)
- **Denoising Strength**: 0.75-0.85 (balance detail vs preservation)
- **Steps**: 25-35 (quality)

## 5. Prompt Template for Indian Faces

```
Positive Prompt:
"photorealistic portrait, Indian person, {description}, professional police mugshot, frontal view, neutral expression, harsh overhead lighting, plain gray background, detailed Indian facial features, natural skin texture, sharp focus, high quality photograph, documentary style"

Negative Prompt:
"cartoon, anime, drawing, painting, sketch, deformed face, distorted features, multiple faces, blurry, low quality, watermark, signature, different face structure, modified proportions, unrealistic, artistic style"
```

## 6. Install ComfyUI Custom Nodes (Optional but Recommended)

```bash
cd ComfyUI/custom_nodes

# Face detailer for better faces
git clone https://github.com/Gourieff/comfyui-reactor-node.git

# Better upscaling
git clone https://github.com/city96/ComfyUI-GGUF.git

# ControlNet preprocessors
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

## 7. API Integration with Flask

See `comfyui_client.py` for Python API client to call ComfyUI from your Flask backend.

## Performance Tips for M4 Air:
- Use `--lowvram` flag if running out of memory
- Reduce batch size to 1
- Use SD1.5 models (lighter than SDXL)
- Close other apps when generating
- Expected generation time: 10-30 seconds per image
