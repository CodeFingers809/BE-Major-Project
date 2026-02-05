"""
Flux 2.1 Klein 4B - Local Generation for M4 MacBook Air
Uses MFLUX CLI (MLX-optimized) for Apple Silicon

Model: black-forest-labs/FLUX.2-klein-4B (4-bit quantized)
- Optimized for Apple Silicon with MLX
- ~4GB VRAM usage with 4-bit quantization
- Supports img2img for revisions and colorization

Supports three modes:
1. Sketch Generation - B&W pencil sketch style
2. Revision/Edit - Modify existing images (img2img)
3. Colorization - Add color to sketches
"""

import os
import time
import subprocess
from typing import Optional

# Default model - Flux 2.1 Klein 4B
DEFAULT_MODEL = "flux2-klein-4b"
DEFAULT_QUANTIZE = 4  # 4-bit quantization for M4 MacBook Air


def _run_mflux_generate(
    prompt: str,
    output_path: str,
    num_steps: int = 8,
    guidance: float = 3.5,
    width: int = 1024,
    height: int = 1024,
    model: str = DEFAULT_MODEL,
    quantize: int = DEFAULT_QUANTIZE,
    init_image_path: Optional[str] = None,
    strength: float = 0.75,
) -> str:
    """
    Run mflux-generate CLI command with Flux 2.1 Klein 4B
    
    Args:
        prompt: Text prompt for generation
        output_path: Where to save the generated image
        num_steps: Number of diffusion steps (8-20 recommended for Klein)
        guidance: CFG guidance scale
        width: Image width
        height: Image height
        model: Model name (default: flux2-klein-4b)
        quantize: Quantization level (4-bit default for M4 Air)
        init_image_path: Optional path to init image for img2img
        strength: Denoising strength for img2img (0.0-1.0)
    
    Returns:
        Path to generated image
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"[MFLUX] Generating with Flux 2.1 Klein 4B ({num_steps} steps, {quantize}-bit)...")
    print(f"[MFLUX] Prompt: {prompt[:100]}...")
    start_time = time.time()
    
    # Build mflux-generate command
    cmd = [
        'mflux-generate',
        '--model', model,
        '--quantize', str(quantize),
        '--prompt', prompt,
        '--steps', str(num_steps),
        '--height', str(height),
        '--width', str(width),
        '--output', output_path,
        '--guidance', str(guidance),
    ]
    
    # Add img2img parameters if init image provided
    if init_image_path and os.path.exists(init_image_path):
        cmd.extend([
            '--image-path', init_image_path,
            '--image-strength', str(strength),
        ])
        print(f"[MFLUX] Using init image with strength {strength}")
    
    try:
        print(f"[MFLUX] Running command: {' '.join(cmd[:8])}...")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error"
            print(f"[MFLUX] Error output: {error_msg}")
            raise Exception(f"mflux-generate failed: {error_msg}")
        
        # Check if file was created
        if not os.path.exists(output_path):
            raise Exception(f"Output file not created: {output_path}")
        
        elapsed = time.time() - start_time
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"[MFLUX] Generation completed in {elapsed:.2f}s")
        print(f"[MFLUX] Output: {output_path} ({file_size:.2f} MB)")
        
        return output_path
        
    except subprocess.TimeoutExpired:
        raise Exception("Generation timed out after 10 minutes")
    except FileNotFoundError:
        raise Exception(
            "mflux-generate not found. Install with: pip install mflux"
        )
    except Exception as e:
        print(f"[MFLUX] Error: {str(e)}")
        raise


def generate_sketch_fast(prompt: str, output_path: str, quality: str = "fast") -> str:
    """
    Generate a pencil sketch using Flux 2.1 Klein 4B
    
    Args:
        prompt: Generation prompt (features description)
        output_path: Output file path
        quality: "fast" (8 steps), "balanced" (12 steps), or "best" (20 steps)
    
    Returns:
        Path to generated image
    """
    steps_map = {
        "fast": 8,        # ~15-20s on M4 Air with Klein
        "balanced": 12,   # ~25-35s on M4 Air  
        "best": 20,       # ~45-60s on M4 Air
    }
    
    steps = steps_map.get(quality, 8)
    
    # Build sketch-optimized prompt
    sketch_prompt = (
        f"black and white pencil sketch on white paper, "
        f"detailed police sketch artist drawing, "
        f"graphite pencil texture, monochrome, "
        f"Indian person, {prompt}, "
        f"realistic facial features, South Asian features, "
        f"harsh lighting, frontal mugshot view, "
        f"hand-drawn criminal identification sketch, "
        f"NOT a photograph, authentic sketch style"
    )
    
    return _run_mflux_generate(
        prompt=sketch_prompt,
        output_path=output_path,
        num_steps=steps,
        guidance=3.5,  # Lower for sketch style
        model=DEFAULT_MODEL,
        quantize=DEFAULT_QUANTIZE,
    )


def revise_sketch(
    prompt: str,
    init_image_path: str,
    output_path: str,
    strength: float = 0.6,
    quality: str = "balanced"
) -> str:
    """
    Revise/edit an existing sketch based on new prompt (img2img)
    
    Args:
        prompt: Description of changes/refinements
        init_image_path: Path to the sketch to revise
        output_path: Output file path
        strength: How much to change (0.0=no change, 1.0=complete regeneration)
        quality: "fast", "balanced", or "best"
    
    Returns:
        Path to revised image
    """
    steps_map = {
        "fast": 8,
        "balanced": 12,
        "best": 20,
    }
    
    steps = steps_map.get(quality, 12)
    
    revision_prompt = (
        f"black and white pencil sketch, police sketch artist drawing, "
        f"Indian person, {prompt}, "
        f"graphite on paper, detailed line art, mugshot style, "
        f"monochrome criminal identification sketch"
    )
    
    print(f"[MFLUX] Revising sketch with strength {strength}...")
    
    return _run_mflux_generate(
        prompt=revision_prompt,
        output_path=output_path,
        num_steps=steps,
        guidance=4.0,
        model=DEFAULT_MODEL,
        quantize=DEFAULT_QUANTIZE,
        init_image_path=init_image_path,
        strength=strength,
    )


def colorize_sketch(
    prompt: str,
    sketch_path: str,
    output_path: str,
    quality: str = "balanced"
) -> str:
    """
    Colorize a black and white sketch while preserving structure
    
    Args:
        prompt: Description of coloring (skin tone, hair color, etc.)
        sketch_path: Path to the B&W sketch
        output_path: Output file path
        quality: "fast", "balanced", or "best"
    
    Returns:
        Path to colorized image
    """
    steps_map = {
        "fast": 10,
        "balanced": 15,
        "best": 25,
    }
    
    steps = steps_map.get(quality, 15)
    
    # Colorization prompt - preserve structure, add realistic colors
    color_prompt = (
        f"realistic police mugshot photograph, "
        f"Indian person, {prompt}, "
        f"harsh police station lighting, plain gray background, "
        f"realistic Indian skin tone, detailed skin texture, "
        f"frontal view, neutral expression, "
        f"high resolution photograph, sharp focus, "
        f"documentary criminal booking photo style"
    )
    
    print(f"[MFLUX] Colorizing sketch...")
    
    # Use lower strength to preserve sketch structure
    return _run_mflux_generate(
        prompt=color_prompt,
        output_path=output_path,
        num_steps=steps,
        guidance=5.0,  # Higher guidance for color accuracy
        model=DEFAULT_MODEL,
        quantize=DEFAULT_QUANTIZE,
        init_image_path=sketch_path,
        strength=0.55,  # Lower strength preserves more structure
    )
