# Face Mask Detection

## Project Structure

```
face_mask_detection/
├── model/
│   └── face_mask_model.keras      ← place trained model here
├── src/
│   ├── __init__.py
│   ├── predict.py                 ← prediction logic
│   └── preprocess.py              ← image utilities
├── static/
│   └── sample_images/             ← test images
├── pages/
│   ├── 1_Image_Detection.py
│   ├── 2_Video_Detection.py
│   └── 3_Webcam_Detection.py
├── tests/
│   └── test_model.py
├── app.py
└── requirements.txt
```

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Train model in Google Colab and download face_mask_model.keras
   Place it inside the model/ folder.

3. Run the app:
   streamlit run app.py

4. Run tests:
   python -m pytest tests/test_model.py -v