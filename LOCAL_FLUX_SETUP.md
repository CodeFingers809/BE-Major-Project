# Local Flux 2.1 Klein 4B Setup for M4 MacBook Air

## Overview

This project uses **Flux 2.1 Klein 4B** with 4-bit quantization via MFLUX (MLX-optimized) for local image generation on Apple Silicon.

**Model**: `black-forest-labs/FLUX.2-klein-4B`  
**Quantization**: 4-bit (fits in 16GB RAM)  
**No server needed!** MFLUX CLI is called directly for each generation.

## System Requirements

- **MacBook Air M4** with 16GB+ RAM
- **macOS 14.0+** (Sonoma or later)
- **Python 3.10+**

## Installation

### Step 1: Install Dependencies

```bash
# Activate your virtual environment
source .venv/bin/activate

# Install MFLUX and MLX
pip install mflux mlx mlx-lm
```

### Step 2: Verify Installation

```bash
# Check mflux is installed
mflux-generate --help

# Check MLX is working
python -c "import mlx; print(f'MLX version: {mlx.__version__}')"

# Check Metal (GPU) is available
python -c "import mlx.core as mx; print(f'Metal available: {mx.metal.is_available()}')"
```

### Step 3: First Run (Downloads Model)

The first generation will download Flux 2.1 Klein 4B (~16GB). This is a one-time download:

```bash
# Test generation with Flux 2.1 Klein 4B (downloads model on first run)
mflux-generate \
    --model flux2-klein-4b \
    --quantize 4 \
    --prompt "black and white pencil sketch of Indian person, frontal mugshot view" \
    --steps 8 \
    --output test_sketch.png
```

## Running the Django App

**No separate Flux server needed!** Just start Django:

```bash
# Start Django server
python manage.py runserver
```

Then open: http://localhost:8000

## Usage

### Generate Sketch

1. Select facial features in the web interface
2. Click "Generate Sketch"
3. Wait for MFLUX to generate (~10-20s)

### Revise Sketch

1. After generating, click "Revise"
2. Enter changes: "make the nose larger", "add facial hair"
3. Adjust strength (0.3-0.8 recommended)

### Colorize

1. After generating, click "Colorize"
2. Optionally add color details: "fair skin, black hair"
3. Wait for colorization

## Performance on M4 MacBook Air (16GB)

| Task     | Quality  | Steps | Time    |
| -------- | -------- | ----- | ------- |
| Sketch   | Fast     | 8     | ~15-20s |
| Sketch   | Balanced | 12    | ~25-35s |
| Sketch   | Best     | 20    | ~45-60s |
| Revision | Balanced | 12    | ~25-35s |
| Colorize | Balanced | 15    | ~35-45s |

## MFLUX CLI Reference

### Basic Generation with Flux 2.1 Klein 4B

```bash
mflux-generate \
    --model flux2-klein-4b \
    --quantize 4 \
    --prompt "your prompt here" \
    --steps 8 \
    --width 1024 \
    --height 1024 \
    --output output.png
```

### Image-to-Image (Revision/Colorization)

```bash
mflux-generate \
    --model flux2-klein-4b \
    --quantize 4 \
    --prompt "revised description" \
    --steps 12 \
    --image-path input.png \
    --image-strength 0.6 \
    --output revised.png
```

### Parameters

| Parameter          | Description                                                 | Default |
| ------------------ | ----------------------------------------------------------- | ------- |
| `--model`          | Model: `flux2-klein-4b`, `flux2-klein-9b`, `schnell`, `dev` | -       |
| `--quantize`       | Quantization: 3, 4, 5, 6, or 8 bit                          | None    |
| `--steps`          | Inference steps (8-50)                                      | varies  |
| `--guidance`       | CFG scale (1.0-10.0)                                        | 3.5     |
| `--width`          | Image width                                                 | 1024    |
| `--height`         | Image height                                                | 1024    |
| `--image-path`     | Input image for img2img                                     | None    |
| `--image-strength` | Denoising strength (0.0-1.0)                                | 0.4     |

## API Endpoints

The Django app provides three endpoints for face generation:

### 1. Generate Sketch

```bash
POST /api/compositions/{id}/generate_sketch/

# Generates B&W pencil sketch from selected features
```

### 2. Revise Sketch

```bash
POST /api/compositions/{id}/revise_sketch/
Content-Type: application/json

{
    "prompt": "make the nose slightly wider",
    "strength": 0.6,
    "quality": "balanced"
}

# Modifies existing sketch while preserving overall structure
# strength: 0.0 (no change) to 1.0 (complete regeneration)
```

### 3. Colorize Sketch

```bash
POST /api/compositions/{id}/colorize/
Content-Type: application/json

{
    "prompt": "medium brown skin tone, black hair",
    "quality": "balanced"
}

# Converts B&W sketch to realistic colored mugshot
# Preserves facial structure from sketch
```

## Workflow

```
1. Select Features → 2. Generate Sketch → 3. Revise (optional) → 4. Colorize → 5. Download
```

## Troubleshooting

### "mflux-generate not found"

```bash
pip install mflux

# Or if using venv:
source .venv/bin/activate
pip install mflux
```

### Slow First Generation

The first run downloads the Flux Schnell model (~12GB). Subsequent runs are much faster.

### Out of Memory

- Close other applications
- Use `--width 512 --height 512` for testing
- Use `quality="fast"` (fewer steps)

### "Metal device not found"

Ensure you're on macOS with Apple Silicon:

```bash
python -c "import mlx.core as mx; print(mx.metal.is_available())"
```

### Generation Fails

```bash
# Check model is downloaded
ls ~/.cache/huggingface/hub/models--*flux*

# Clear cache and re-download
rm -rf ~/.cache/huggingface/hub/models--black-forest-labs*
```

## Python Usage

```python
from face_generator.local_flux import (
    generate_sketch_fast,
    revise_sketch,
    colorize_sketch
)

# Generate sketch
generate_sketch_fast(
    prompt="male Indian person, oval face, thick eyebrows",
    output_path="media/test/sketch.png",
    quality="fast"  # "fast", "balanced", or "best"
)

# Revise sketch
revise_sketch(
    prompt="make the eyes smaller, add stubble",
    init_image_path="media/test/sketch.png",
    output_path="media/test/revised.png",
    strength=0.6,
    quality="balanced"
)

# Colorize
colorize_sketch(
    prompt="medium brown skin, black hair",
    sketch_path="media/test/revised.png",
    output_path="media/test/colored.png",
    quality="balanced"
)
```

## Model Information

| Model             | Parameters | Quantized Size | Description                       |
| ----------------- | ---------- | -------------- | --------------------------------- |
| Flux 2.1 Klein 4B | 4B         | ~4GB (4-bit)   | Optimized for speed, good quality |
| Flux 2.1 Klein 9B | 9B         | ~8GB (4-bit)   | Higher quality, slower            |

## Resources

- [MFLUX GitHub](https://github.com/filipstrand/mflux)
- [MLX Framework](https://github.com/ml-explore/mlx)
- [Flux 2.1 Klein on Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B)

