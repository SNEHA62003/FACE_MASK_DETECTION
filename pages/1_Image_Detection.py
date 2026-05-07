"""pages/1_Image_Detection.py"""

import streamlit as st
import numpy as np
from PIL import Image
from src.predict import load_model, predict_faces_in_frame

st.set_page_config(page_title="Image Detection", page_icon="📷", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; font-family: 'DM Sans', sans-serif; color: #f0f0f5;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 10% 10%, #1a0533 0%, #0a0a0f 55%);
}
[data-testid="stSidebar"] { background: rgba(15,10,30,0.95) !important; border-right: 1px solid rgba(150,80,255,0.2) !important; }
[data-testid="stSidebar"] * { color: #d0c0ff !important; }

.page-header { padding: 36px 0 24px; }
.page-title { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #d0b0ff 60%, #bf5fff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub { color: #666688; font-size: 15px; margin-top: 6px; }

.result-card {
    background: rgba(255,255,255,0.03); border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.07); padding: 16px 20px; margin: 8px 0;
    transition: border-color 0.3s;
}
.result-card.mask   { border-left: 4px solid #22dd88; background: rgba(34,221,136,0.06); }
.result-card.nomask { border-left: 4px solid #ff4466; background: rgba(255,68,102,0.06); }
.result-label { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; }
.result-label.mask   { color: #22dd88; }
.result-label.nomask { color: #ff4466; }
.result-conf { font-size: 13px; color: #666688; margin-top: 4px; }

.conf-bar-wrap { background: rgba(255,255,255,0.06); border-radius: 99px; height: 6px; margin-top: 10px; overflow: hidden; }
.conf-bar { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
.conf-bar.mask   { background: linear-gradient(90deg, #22dd88, #00ffaa); }
.conf-bar.nomask { background: linear-gradient(90deg, #ff4466, #ff8866); }

[data-testid="stFileUploader"] {
    background: rgba(191,95,255,0.05) !important;
    border: 2px dashed rgba(191,95,255,0.3) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
[data-testid="stImage"] img { border-radius: 14px !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>

<div class="page-header">
    <div class="page-title">📷 Image Detection</div>
    <div class="page-sub">Upload a face image — the model will locate faces and classify each one.</div>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def get_model():
    return load_model()


try:
    model = get_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

uploaded_file = st.file_uploader("Drop an image here or click to browse", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("**Original**")
        st.image(image, use_column_width=True)

    with st.spinner("🔍 Detecting faces and analyzing..."):
        annotated, results = predict_faces_in_frame(model, img_array)

    with col2:
        st.markdown("**Detection Result**")
        st.image(annotated, use_column_width=True)

    st.markdown("---")
    st.markdown("#### Results")

    for i, r in enumerate(results):
        label = r["label"]
        conf = r["confidence"]
        has_mask = "With Mask" in label
        css_class = "mask" if has_mask else "nomask"
        emoji = "✅" if has_mask else "❌"
        st.markdown(f"""
        <div class="result-card {css_class}">
            <div class="result-label {css_class}">{emoji} Face {i+1}: {label}</div>
            <div class="result-conf">Confidence: {conf:.1%}</div>
            <div class="conf-bar-wrap">
                <div class="conf-bar {css_class}" style="width:{conf*100:.1f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)