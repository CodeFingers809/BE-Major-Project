"""
Black Forest Labs Flux API - Cloud Generation
Uses the BFL API for high-quality image generation

API Documentation: https://docs.bfl.ai/

Models used:
- Flux Dev: Initial sketch generation (text-to-image, fast & cheap)
- Flux Kontext Pro: Revision/editing and colorization (image-to-image)

Supports three modes:
1. Sketch Generation - B&W pencil sketch style (Flux Dev)
2. Revision/Edit - Modify existing images (Kontext Pro)
3. Colorization - Add color to sketches (Kontext Pro)
"""

import os
import time
import requests
import base64
from typing import Optional
from django.conf import settings as django_settings


# BFL API endpoints - correct base URL
BFL_API_BASE = "https://api.bfl.ai/v1"
BFL_RESULT_ENDPOINT = f"{BFL_API_BASE}/get_result"

# Max time (seconds) to keep retrying when status is "Task not found"
# BFL sometimes reports this while the task is still queued / processing.
TASK_NOT_FOUND_PATIENCE = 90


def _get_text2img_endpoint() -> str:
    """Get the text-to-image endpoint from settings"""
    model = django_settings.BFL_TEXT2IMG_MODEL
    return f"{BFL_API_BASE}/{model}"


def _get_img2img_endpoint() -> str:
    """Get the image editing endpoint from settings"""
    model = django_settings.BFL_IMG2IMG_MODEL
    return f"{BFL_API_BASE}/{model}"


# Request timeout (connect, read) in seconds
REQUEST_TIMEOUT = (15, 60)

# Image dimensions - portrait mugshot, under 1MP (786,432 pixels)
MUGSHOT_WIDTH = 768
MUGSHOT_HEIGHT = 1024


def _get_api_key() -> str:
    """Get BFL API key from Django settings"""
    api_key = django_settings.BFL_API_KEY
    if not api_key or api_key == "your_api_key_here":
        raise ValueError("BFL_API_KEY not configured. Set it in your .env file.")
    return api_key


def _poll_for_result(
    request_id: str, timeout: int = 180, polling_url: str | None = None
) -> dict:
    """
    Poll BFL API for generation result.

    Args:
        request_id: The task ID returned from generation request
        timeout: Maximum time to wait in seconds
        polling_url: Optional polling URL returned by the submit response

    Returns:
        Result dict with image URL
    """
    api_key = _get_api_key()
    start_time = time.time()

    poll_endpoint = polling_url or BFL_RESULT_ENDPOINT
    poll_params = {} if polling_url else {"id": request_id}

    # Brief initial delay — BFL backend sometimes needs a moment
    time.sleep(2)

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                poll_endpoint,
                headers={"x-key": api_key},
                params=poll_params,
                timeout=REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException as e:
            print(f"[BFL API] Poll request error: {e}, retrying...")
            time.sleep(3)
            continue

        # Try to parse JSON regardless of status code
        try:
            result = response.json()
        except Exception:
            print(
                f"[BFL API] Non-JSON response ({response.status_code}): {response.text[:200]}"
            )
            time.sleep(3)
            continue

        poll_status = result.get("status")

        if poll_status == "Ready":
            return result
        elif poll_status in ["Error", "Failed", "Request Moderated"]:
            raise Exception(f"Generation failed ({poll_status}): {result}")
        elif poll_status == "Task not found":
            # BFL reports this while the task is still queued/processing.
            # Keep retrying until TASK_NOT_FOUND_PATIENCE is exceeded.
            elapsed = time.time() - start_time
            if elapsed > TASK_NOT_FOUND_PATIENCE:
                raise Exception(
                    f"Task not found after {elapsed:.0f}s — job may have failed silently"
                )
            print(f"[BFL API] Task not found yet ({elapsed:.0f}s), retrying...")
            time.sleep(3)
            continue

        # Pending / Processing — keep waiting
        print(f"[BFL API] Status: {poll_status} ({time.time() - start_time:.0f}s)")
        time.sleep(2)

    raise Exception(f"Generation timed out after {timeout} seconds")


def _download_image(url: str, output_path: str) -> str:
    """Download image from URL to local path"""
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def _image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _run_dev_generate(
    prompt: str,
    output_path: str,
    width: int = MUGSHOT_WIDTH,
    height: int = MUGSHOT_HEIGHT,
) -> str:
    """
    Run BFL Flux Dev API for text-to-image generation.

    Args:
        prompt: Text prompt for generation
        output_path: Where to save the generated image
        width: Image width (default: 768)
        height: Image height (default: 1024)

    Returns:
        Path to generated image
    """
    api_key = _get_api_key()
    endpoint = _get_text2img_endpoint()
    model_name = django_settings.BFL_TEXT2IMG_MODEL

    print(f"[BFL API] Generating with {model_name}...")
    print(f"[BFL API] Prompt: {prompt[:120]}...")
    start_time = time.time()

    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }

    try:
        response = requests.post(
            endpoint,
            headers={"x-key": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            error_msg = response.text
            print(f"[BFL API] Error: {error_msg}")
            raise Exception(
                f"BFL API request failed ({response.status_code}): {error_msg}"
            )

        result = response.json()
        request_id = result.get("id")
        polling_url = result.get("polling_url")

        if not request_id:
            raise Exception(f"No request ID in response: {result}")

        print(f"[BFL API] Request submitted, ID: {request_id}")

        result = _poll_for_result(request_id, polling_url=polling_url)
        image_url = result.get("result", {}).get("sample")

        if not image_url:
            raise Exception(f"No image URL in result: {result}")

        _download_image(image_url, output_path)

        elapsed = time.time() - start_time
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"[BFL API] Generation completed in {elapsed:.1f}s")
        print(f"[BFL API] Output: {output_path} ({file_size:.2f} MB)")

        return output_path

    except requests.exceptions.Timeout:
        raise Exception("BFL API request timed out. Check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to BFL API. Check your internet connection.")
    except Exception as e:
        print(f"[BFL API] Error: {str(e)}")
        raise


def _run_kontext_generate(
    prompt: str,
    output_path: str,
    init_image_path: str,
) -> str:
    """
    Run BFL Flux Kontext Pro API for image editing/transformation.

    Args:
        prompt: Text prompt describing the edit/transformation
        output_path: Where to save the generated image
        init_image_path: Path to the source image to edit

    Returns:
        Path to generated image
    """
    api_key = _get_api_key()
    endpoint = _get_img2img_endpoint()
    model_name = django_settings.BFL_IMG2IMG_MODEL

    print(f"[BFL API] Editing with {model_name}...")
    print(f"[BFL API] Prompt: {prompt[:120]}...")
    start_time = time.time()

    if not os.path.exists(init_image_path):
        raise Exception(f"Source image not found: {init_image_path}")

    image_b64 = _image_to_base64(init_image_path)
    img_size_mb = len(image_b64) * 3 / 4 / 1024 / 1024
    print(f"[BFL API] Input image: {init_image_path} ({img_size_mb:.2f} MB base64)")

    payload = {
        "prompt": prompt,
        "input_image": image_b64,
        "output_format": "png",
    }

    try:
        response = requests.post(
            endpoint,
            headers={"x-key": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            error_msg = response.text
            print(f"[BFL API] Error ({response.status_code}): {error_msg[:300]}")
            raise Exception(
                f"BFL API request failed ({response.status_code}): {error_msg}"
            )

        result = response.json()
        request_id = result.get("id")
        polling_url = result.get("polling_url")

        if not request_id:
            raise Exception(f"No request ID in response: {result}")

        print(f"[BFL API] Request submitted, ID: {request_id}")

        result = _poll_for_result(request_id, polling_url=polling_url)
        image_url = result.get("result", {}).get("sample")

        if not image_url:
            raise Exception(f"No image URL in result: {result}")

        _download_image(image_url, output_path)

        elapsed = time.time() - start_time
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"[BFL API] Edit completed in {elapsed:.1f}s")
        print(f"[BFL API] Output: {output_path} ({file_size:.2f} MB)")

        return output_path

    except requests.exceptions.Timeout:
        raise Exception("BFL API request timed out. Check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to BFL API. Check your internet connection.")
    except Exception as e:
        print(f"[BFL API] Error: {str(e)}")
        raise


# ── System prompt template (style/format constraints we always enforce) ──
SKETCH_SYSTEM_PROMPT = (
    "A raw hand-drawn police forensic sketch on textured white paper. "
    "Visible pencil strokes, graphite smudges, rough crosshatching for shading, "
    "eraser marks, uneven line weight typical of a real sketch artist working quickly. "
    "The subject wears a plain white collared shirt visible at the bottom edge. "
    "Frontal mugshot composition, head and upper chest only. "
    "NOT a digital render, NOT clean or polished. "
    "This looks like a scan of an actual paper sketch from an Indian police station — "
    "imperfect, gritty, with visible paper grain and pencil texture throughout. "
    "Strictly black and white, no color, monochrome graphite drawing."
)


def generate_sketch(
    features_description: str,
    output_path: str,
    user_prompt: str = "",
    reference_image_path: str | None = None,
) -> str:
    """
    Generate a police-style pencil sketch mugshot.

    Args:
        features_description: Structured facial features from selectors
        output_path: Output file path
        user_prompt: Optional free-form user description (extra details)
        reference_image_path: Optional path to a reference photo (CCTV, blurry, etc.)

    Returns:
        Path to generated image
    """
    # Build the person description from features + optional user text
    person_desc = f"The sketch shows an Indian person with the following features: {features_description}."
    if user_prompt:
        person_desc += f" Additional details from witness: {user_prompt}."

    full_prompt = f"{SKETCH_SYSTEM_PROMPT} {person_desc}"

    if reference_image_path and os.path.exists(reference_image_path):
        # Use Kontext (img2img) to recreate sketch from reference photo
        reference_prompt = (
            f"Recreate this person as a hand-drawn police forensic pencil sketch. "
            f"Accurately capture the facial structure, proportions, and features visible in this image. "
            f"The person has: {features_description}. "
        )
        if user_prompt:
            reference_prompt += f"Additional details: {user_prompt}. "
        reference_prompt += SKETCH_SYSTEM_PROMPT

        print(f"[BFL API] Generating sketch FROM reference image...")
        return _run_kontext_generate(
            prompt=reference_prompt,
            output_path=output_path,
            init_image_path=reference_image_path,
        )
    else:
        # Text-to-image generation (no reference)
        return _run_dev_generate(
            prompt=full_prompt,
            output_path=output_path,
        )


def revise_sketch(
    edit_instruction: str,
    init_image_path: str,
    output_path: str,
    conversation_history: list[str] | None = None,
    **kwargs,
) -> str:
    """
    Revise/edit an existing sketch using Flux Kontext Pro.

    Args:
        edit_instruction: What to change in the sketch
        init_image_path: Path to the sketch to revise
        output_path: Output file path
        conversation_history: List of previous revision prompts for context

    Returns:
        Path to revised image
    """
    # Build context from conversation history if available
    context_prefix = ""
    if conversation_history:
        past_edits = "; ".join(conversation_history)
        context_prefix = (
            f"Previous edits already applied to this sketch: [{past_edits}]. "
            f"Now additionally: "
        )

    # IMPORTANT: Strong style enforcement at the END of the prompt so the model
    # doesn't drift toward photorealism or lose the sketch aesthetic.
    revision_prompt = (
        f"{context_prefix}{edit_instruction}. "
        f"CRITICAL STYLE RULES — the output MUST remain a raw pencil sketch on paper: "
        f"visible graphite pencil strokes, crosshatching, paper texture, smudge marks, "
        f"black and white only, NO color, NO photorealism, NO digital rendering. "
        f"Only change what was requested — preserve the sketch style and all other details exactly as-is."
    )

    print(f"[BFL API] Revising sketch with Kontext Pro...")

    return _run_kontext_generate(
        prompt=revision_prompt,
        output_path=output_path,
        init_image_path=init_image_path,
    )


def colorize_sketch(
    features_description: str,
    sketch_path: str,
    output_path: str,
    **kwargs,
) -> str:
    """
    Colorize a black-and-white sketch into a realistic mugshot using Kontext Pro.

    Args:
        features_description: Facial features for color accuracy
        sketch_path: Path to the B&W sketch
        output_path: Output file path

    Returns:
        Path to colorized image
    """
    color_prompt = (
        f"Transform this pencil sketch into a real unedited police booking photograph. "
        f"The person is an Indian suspect with these features: {features_description}. "
        f"Wearing a plain white collared shirt. "
        f"This must look like a real raw mugshot photo taken at an Indian police station - "
        f"unflattering harsh fluorescent overhead light, washed out, slightly grainy, "
        f"plain dirty gray wall background, no retouching or beautification. "
        f"Realistic imperfect skin with pores, blemishes, uneven tone. "
        f"Natural South Asian skin color, real hair texture. "
        f"The person looks tired with a blank neutral expression, direct eye contact. "
        f"Preserve the exact face shape, nose, eyes, mouth, and all features from the sketch. "
        f"NOT idealized, NOT stylized, NOT a portrait photo - this is a gritty criminal booking photo."
    )

    print(f"[BFL API] Colorizing sketch with Kontext Pro...")

    return _run_kontext_generate(
        prompt=color_prompt,
        output_path=output_path,
        init_image_path=sketch_path,
    )
