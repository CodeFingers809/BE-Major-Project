"""
Face Matching Module
Compares a generated face against criminal database images using OpenCV.

Uses histogram comparison + structural similarity for matching.
No heavy ML dependencies — works with cv2 + numpy already installed.
"""

import os
import cv2
import numpy as np
from typing import Optional


# Cache for pre-computed criminal DB data (histograms)
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


def _compute_structural_features(image_path: str) -> Optional[np.ndarray]:
    """Extract structural features using edge detection + pixel intensity."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Resize to standard
    img = cv2.resize(img, (128, 128))

    # Extract edge features (structural similarity for face shapes)
    edges = cv2.Canny(img, 50, 150)

    # Combine normalized grayscale + edges as feature vector
    gray_flat = img.flatten().astype(np.float32) / 255.0
    edge_flat = edges.flatten().astype(np.float32) / 255.0

    return np.concatenate([gray_flat, edge_flat])


def _load_criminal_db(criminal_db_path: str) -> dict:
    """
    Load and cache criminal DB image data.
    Returns dict of {criminal_id: {path, histogram, features}}
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
        features = _compute_structural_features(filepath)

        if hist is not None and features is not None:
            _criminal_cache[criminal_id] = {
                "path": filepath,
                "filename": filename,
                "histogram": hist,
                "features": features,
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
    query_features = _compute_structural_features(query_image_path)

    if query_hist is None or query_features is None:
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

        # Structural similarity via cosine similarity of feature vectors
        query_norm = np.linalg.norm(query_features)
        data_norm = np.linalg.norm(data["features"])

        if query_norm > 0 and data_norm > 0:
            struct_score = np.dot(query_features, data["features"]) / (
                query_norm * data_norm
            )
        else:
            struct_score = 0.0

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
