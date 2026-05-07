"""pages/3_Webcam_Detection.py"""

import streamlit as st
import numpy as np
from PIL import Image
from src.predict import load_model, predict_faces_in_frame

st.set_page_config(page_title="Webcam Detection", page_icon="📹", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; font-family: 'DM Sans', sans-serif; color: #f0f0f5;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 50% 0%, #33001a 0%, #0a0a0f 55%);
}
[data-testid="stSidebar"] { background: rgba(15,10,30,0.95) !important; border-right: 1px solid rgba(150,80,255,0.2) !important; }
[data-testid="stSidebar"] * { color: #d0c0ff !important; }

.page-title { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; padding: 36px 0 6px;
    background: linear-gradient(135deg, #ff80b4, #ff4488);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub { color: #666688; font-size: 15px; margin-bottom: 28px; }

.result-card {
    border-radius: 16px; padding: 18px 22px; margin: 8px 0;
    border-left: 4px solid transparent;
}
.result-card.mask   { background: rgba(34,221,136,0.07);  border-left-color: #22dd88; }
.result-card.nomask { background: rgba(255,68,102,0.07);  border-left-color: #ff4466; }
.result-label { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; }
.result-label.mask   { color: #22dd88; }
.result-label.nomask { color: #ff4466; }
.result-conf { color: #666688; font-size: 13px; margin-top: 4px; }
.conf-bar-wrap { background: rgba(255,255,255,0.06); border-radius: 99px; height: 6px; margin-top: 10px; overflow: hidden; }
.conf-bar.mask   { height:100%; border-radius:99px; background: linear-gradient(90deg,#22dd88,#00ffaa); }
.conf-bar.nomask { height:100%; border-radius:99px; background: linear-gradient(90deg,#ff4466,#ff8866); }

[data-testid="stCameraInput"] > div { border-radius: 16px !important; }
[data-testid="stImage"] img { border-radius: 14px !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>

<div class="page-title">📹 Webcam Detection</div>
<div class="page-sub">Capture a live photo from your camera for instant mask detection.</div>
""", unsafe_allow_html=True)


@st.cache_resource
def get_model():
    return load_model()


try:
    model = get_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

webcam_img = st.camera_input("📸 Click to take a photo")

if webcam_img:
    image = Image.open(webcam_img).convert("RGB")
    img_array = np.array(image)

    with st.spinner("🔍 Analyzing..."):
        annotated, results = predict_faces_in_frame(model, img_array)

    col1, col2 = st.columns(2, gap="large")
    col1.markdown("**Captured**")
    col1.image(image, use_column_width=True)
    col2.markdown("**Detection**")
    col2.image(annotated, use_column_width=True)

    st.markdown("---")
    st.markdown("#### Results")
    for i, r in enumerate(results):
        label = r["label"]
        conf = r["confidence"]
        has_mask = "With Mask" in label
        css = "mask" if has_mask else "nomask"
        emoji = "✅" if has_mask else "❌"
        st.markdown(f"""
        <div class="result-card {css}">
            <div class="result-label {css}">{emoji} Face {i+1}: {label}</div>
            <div class="result-conf">Confidence: {conf:.1%}</div>
            <div class="conf-bar-wrap"><div class="conf-bar {css}" style="width:{conf*100:.1f}%"></div></div>
        </div>""", unsafe_allow_html=True)