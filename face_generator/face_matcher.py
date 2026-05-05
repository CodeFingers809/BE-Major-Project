"""
Face Matching Module
Compares a generated face against criminal database images using OpenCV.

Uses histogram comparison + SSIM structural similarity for matching.
No heavy ML dependencies — works with cv2 + numpy already installed.
"""

import os
import cv2
import numpy as np
from typing import Optional


# Cache for pre-computed criminal DB data
_criminal_cache: dict = {}


def _compute_face_histogram(image_path: str) -> Optional[np.ndarray]:
    """Compute a normalized color histogram for a face image."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    # Resize to standard size for fair comparison
    img = cv2.resize(img, (256, 256))

    # Convert to HSV for better color-based matching
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Compute histogram (H: 50 bins, S: 60 bins)
    hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
    return hist


def _load_grayscale_structural_image(image_path: str) -> Optional[np.ndarray]:
    """Load grayscale image resized for structural similarity (SSIM)."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Resize to standard dimensions for fair SSIM comparison
    img = cv2.resize(img, (128, 128))
    return img


def _compute_ssim(gray_a: np.ndarray, gray_b: np.ndarray) -> float:
    """Compute SSIM score between two grayscale images using OpenCV + numpy."""
    img1 = gray_a.astype(np.float32)
    img2 = gray_b.astype(np.float32)

    # SSIM constants for L=255
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    kernel_size = (11, 11)
    sigma = 1.5

    mu1 = cv2.GaussianBlur(img1, kernel_size, sigma)
    mu2 = cv2.GaussianBlur(img2, kernel_size, sigma)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv2.GaussianBlur(img1 * img1, kernel_size, sigma) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(img2 * img2, kernel_size, sigma) - mu2_sq
    sigma12 = cv2.GaussianBlur(img1 * img2, kernel_size, sigma) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / (
        (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
    )

    score = float(np.mean(ssim_map))
    return max(0.0, min(1.0, score))


def _load_criminal_db(criminal_db_path: str) -> dict:
    """
    Load and cache criminal DB image data.
    Returns dict of {criminal_id: {path, histogram, gray_image}}
    """
    global _criminal_cache

    if _criminal_cache:
        return _criminal_cache

    print(f"[FaceMatcher] Loading criminal DB from {criminal_db_path}...")

    for filename in os.listdir(criminal_db_path):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        criminal_id = os.path.splitext(filename)[0]
        filepath = os.path.join(criminal_db_path, filename)

        hist = _compute_face_histogram(filepath)
        gray_image = _load_grayscale_structural_image(filepath)

        if hist is not None and gray_image is not None:
            _criminal_cache[criminal_id] = {
                "path": filepath,
                "filename": filename,
                "histogram": hist,
                "gray_image": gray_image,
            }

    print(f"[FaceMatcher] Loaded {len(_criminal_cache)} criminal images")
    return _criminal_cache


def match_face(
    query_image_path: str,
    criminal_db_path: str,
    top_k: int = 10,
) -> list[dict]:
    """
    Match a query face image against the criminal database.

    Args:
        query_image_path: Path to the generated/colorized face image
        criminal_db_path: Path to the criminalDB folder
        top_k: Number of top matches to return

    Returns:
        List of dicts: [{criminal_id, filename, similarity}, ...]
        sorted by similarity (highest first)
    """
    # Compute query features
    query_hist = _compute_face_histogram(query_image_path)
    query_gray = _load_grayscale_structural_image(query_image_path)

    if query_hist is None or query_gray is None:
        print(f"[FaceMatcher] Could not process query image: {query_image_path}")
        return []

    # Load criminal DB
    criminals = _load_criminal_db(criminal_db_path)

    if not criminals:
        print(f"[FaceMatcher] No criminal images found in {criminal_db_path}")
        return []

    scores = []

    for criminal_id, data in criminals.items():
        # Histogram comparison (color similarity) — correlation method
        hist_score = cv2.compareHist(query_hist, data["histogram"], cv2.HISTCMP_CORREL)

        # Structural similarity via SSIM on grayscale images
        struct_score = _compute_ssim(query_gray, data["gray_image"])

        # Combined score: weight structural features more for face matching
        combined = 0.4 * max(hist_score, 0) + 0.6 * max(struct_score, 0)

        scores.append(
            {
                "criminal_id": criminal_id,
                "filename": data["filename"],
                "similarity": float(combined),
            }
        )

    # Sort by similarity descending
    scores.sort(key=lambda x: x["similarity"], reverse=True)

    return scores[:top_k]


def clear_cache():
    """Clear the criminal DB cache (useful if DB images change)."""
    global _criminal_cache
    _criminal_cache = {}
