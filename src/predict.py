"""
src/predict.py - Core prediction logic
"""

import os
import numpy as np
import tensorflow as tf
from src.preprocess import preprocess_image, detect_faces, annotate_frame

# ─────────────────────────────────────────────
# Model Loader
# ─────────────────────────────────────────────

def load_model():
    """Load model from /model folder. Supports .keras and .h5 formats."""
    keras_path = os.path.join("model", "face_mask_model.keras")
    h5_path    = os.path.join("model", "face_mask_model.h5")

    if os.path.exists(keras_path):
        return tf.keras.models.load_model(keras_path)
    elif os.path.exists(h5_path):
        return tf.keras.models.load_model(h5_path)
    else:
        raise FileNotFoundError(
            "No model found in /model folder.\n"
            "Expected: model/face_mask_model.keras  OR  model/face_mask_model.h5\n"
            "Train the model in Colab and place it here."
        )


# ─────────────────────────────────────────────
# Single Image Prediction
# ─────────────────────────────────────────────

def predict_single(model, img_array):
    """
    Predict mask status for a single image array (RGB).
    Returns: (label, confidence, raw_prob)
    """
    preprocessed = preprocess_image(img_array)
    prob = model.predict(preprocessed, verbose=0)[0][0]
    label = "With Mask 😷" if prob >= 0.5 else "Without Mask 😶"
    confidence = float(prob) if prob >= 0.5 else float(1 - prob)
    return label, confidence, float(prob)


# ─────────────────────────────────────────────
# Face-Region Prediction
# ─────────────────────────────────────────────

def predict_faces_in_frame(model, frame_rgb):
    """
    Detect faces in a frame and predict mask for each.
    Returns: (annotated_frame, results_list)
    results_list: [{"label": str, "confidence": float, "box": tuple|None}]
    """
    faces = detect_faces(frame_rgb)
    results = []

    if len(faces) == 0:
        # Fallback: predict on full image
        label, conf, prob = predict_single(model, frame_rgb)
        results.append({"label": label, "confidence": conf, "box": None})
        return frame_rgb.copy(), results

    for (x, y, w, h) in faces:
        face_roi = frame_rgb[y:y + h, x:x + w]
        label, conf, prob = predict_single(model, face_roi)
        results.append({"label": label, "confidence": conf, "box": (x, y, w, h)})

    annotated = annotate_frame(frame_rgb, results)
    return annotated, results