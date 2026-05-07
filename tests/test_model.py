"""
tests/test_model.py
Run: python -m pytest tests/test_model.py -v
"""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocess import preprocess_image, detect_faces, annotate_frame
from src.predict import load_model, predict_single, predict_faces_in_frame


# ─────────────────────────────────────────────
# Preprocessing Tests
# ─────────────────────────────────────────────

def test_preprocess_output_shape():
    dummy = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    result = preprocess_image(dummy)
    assert result.shape == (1, 128, 128, 3), "Preprocessed shape should be (1,128,128,3)"


def test_preprocess_normalization():
    dummy = np.full((128, 128, 3), 255, dtype=np.uint8)
    result = preprocess_image(dummy)
    assert result.max() <= 1.0, "Pixel values should be normalized to [0,1]"
    assert result.min() >= 0.0


def test_annotate_no_crash():
    dummy = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    results = [{"label": "With Mask 😷", "confidence": 0.95, "box": (50, 50, 100, 100)}]
    annotated = annotate_frame(dummy, results)
    assert annotated.shape == dummy.shape


# ─────────────────────────────────────────────
# Model Tests
# ─────────────────────────────────────────────

@pytest.fixture(scope="module")
def model():
    try:
        return load_model()
    except FileNotFoundError:
        pytest.skip("Model file not found. Train model in Colab first.")


def test_model_loads(model):
    assert model is not None, "Model should load successfully"


def test_predict_single_output(model):
    dummy = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    label, conf, prob = predict_single(model, dummy)
    assert label in ["With Mask 😷", "Without Mask 😶"]
    assert 0.0 <= conf <= 1.0
    assert 0.0 <= prob <= 1.0


def test_predict_confidence_range(model):
    for _ in range(5):
        dummy = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        _, conf, _ = predict_single(model, dummy)
        assert 0.5 <= conf <= 1.0, "Confidence should always be >= 0.5"


def test_predict_faces_returns_results(model):
    dummy_frame = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    annotated, results = predict_faces_in_frame(model, dummy_frame)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert annotated.shape == dummy_frame.shape


def test_model_input_shape(model):
    expected = (None, 128, 128, 3)
    actual = tuple(model.input_shape)
    assert actual == expected, f"Expected input shape {expected}, got {actual}"


def test_model_output_shape(model):
    expected = (None, 1)
    actual = tuple(model.output_shape)
    assert actual == expected, f"Expected output shape {expected}, got {actual}"