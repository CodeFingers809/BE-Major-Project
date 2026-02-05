#!/usr/bin/env python
"""
Download Flux models before running the app
This will download:
- Flux Schnell base model (~17GB)
- Indo-Realism LoRA (~2GB)
"""

import subprocess
import os

print("=" * 60)
print("DOWNLOADING FLUX MODELS FOR M4")
print("=" * 60)
print("\nThis will download approximately 19GB of models.")
print("Please be patient, this may take 5-10 minutes.\n")

# Create test output directory
os.makedirs("media/test", exist_ok=True)
output_path = "media/test/test_download.png"

# Simple test prompt
test_prompt = "black and white pencil sketch, test image"

print("[1/2] Downloading Flux Schnell base model...")
print("      Size: ~17GB")
print("      This is a one-time download\n")

# Build mflux command with extended timeout
cmd = [
    'mflux-generate',
    '--model', 'schnell',
    '--prompt', test_prompt,
    '--steps', '4',  # Minimal steps for quick test
    '--height', '512',  # Smaller size for faster test
    '--width', '512',
    '--output', output_path,
]

print(f"Running: {' '.join(cmd[:6])}...\n")

try:
    # Run with no timeout for initial download
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=None  # No timeout for model download
    )

    if result.returncode == 0:
        print("\n✅ SUCCESS! Flux Schnell model downloaded")
        print(f"   Test image created: {output_path}")

        # Now download Indo-Realism LoRA
        print("\n[2/2] Downloading Indo-Realism LoRA...")
        print("      Size: ~2GB\n")

        lora_output = "media/test/test_lora.png"
        cmd_lora = [
            'mflux-generate',
            '--model', 'schnell',
            '--prompt', 'black and white pencil sketch, Indian person',
            '--steps', '4',
            '--height', '512',
            '--width', '512',
            '--output', lora_output,
            '--lora-repo-id', 'prithivMLmods/Flux.1-Dev-Indo-Realism-LoRA',
            '--lora-name', 'flux_realism_lora.safetensors',
            '--lora-scales', '1.0',
        ]

        result_lora = subprocess.run(
            cmd_lora,
            capture_output=True,
            text=True,
            timeout=None
        )

        if result_lora.returncode == 0:
            print("\n✅ SUCCESS! Indo-Realism LoRA downloaded")
            print(f"   Test image created: {lora_output}")
            print("\n" + "=" * 60)
            print("ALL MODELS DOWNLOADED SUCCESSFULLY!")
            print("=" * 60)
            print("\nYou can now use the Django app for fast generation.")
            print("Typical generation time: 15-20 seconds\n")
        else:
            print(f"\n❌ LoRA download failed: {result_lora.stderr}")

    else:
        print(f"\n❌ Model download failed: {result.stderr}")

except subprocess.TimeoutExpired:
    print("\n❌ Download timed out")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\nYou can delete media/test/ folder after download completes.")
