"""
src/preprocess.py - Image preprocessing utilities
"""

import cv2
import numpy as np

IMG_SIZE = 128


def load_image_from_path(image_path):
    """Load image from file path and convert to RGB."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def preprocess_image(img_array):
    """Resize and normalize a single image for model input."""
    img = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    img = img.astype('float32') / 255.0
    return np.expand_dims(img, axis=0)


def detect_faces(frame_rgb):
    """
    Detect faces in an RGB frame using Haar Cascade.
    Returns list of (x, y, w, h) bounding boxes.
    """
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )
    return faces


def annotate_frame(frame_rgb, results):
    """
    Draw bounding boxes and labels on frame.
    results: list of dicts with keys: label, confidence, box
    """
    annotated = frame_rgb.copy()
    for r in results:
        if r["box"] is None:
            continue
        x, y, w, h = r["box"]
        label = r["label"]
        conf = r["confidence"]
        color = (0, 200, 0) if "With Mask" in label else (220, 50, 50)
        cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 3)
        text = f"{label} ({conf:.0%})"
        cv2.putText(
            annotated, text,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65, color, 2
        )
    return annotated