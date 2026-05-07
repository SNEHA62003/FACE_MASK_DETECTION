"""pages/2_Video_Detection.py"""

import streamlit as st
import numpy as np
import cv2
import tempfile
import os
from src.predict import load_model, predict_faces_in_frame

st.set_page_config(page_title="Video Detection", page_icon="🎬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; font-family: 'DM Sans', sans-serif; color: #f0f0f5;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 90% 10%, #001a33 0%, #0a0a0f 55%);
}
[data-testid="stSidebar"] { background: rgba(15,10,30,0.95) !important; border-right: 1px solid rgba(150,80,255,0.2) !important; }
[data-testid="stSidebar"] * { color: #d0c0ff !important; }

.page-title { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; padding: 36px 0 6px;
    background: linear-gradient(135deg, #50b4ff, #00e5ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub { color: #666688; font-size: 15px; margin-bottom: 28px; }

.metric-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 22px 20px; text-align: center;
}
.metric-val { font-family: 'Syne', sans-serif; font-size: 34px; font-weight: 800; }
.metric-val.green { color: #22dd88; }
.metric-val.red   { color: #ff4466; }
.metric-val.blue  { color: #50b4ff; }
.metric-lbl { font-size: 12px; color: #555577; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }

[data-testid="stImage"] img { border-radius: 12px !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>

<div class="page-title">🎬 Video Detection</div>
<div class="page-sub">Upload a video for frame-by-frame mask compliance analysis.</div>
""", unsafe_allow_html=True)


@st.cache_resource
def get_model():
    return load_model()


try:
    model = get_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    tfile.close()

    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    st.info(f"📹 {total_frames} frames &nbsp;·&nbsp; {fps:.1f} FPS")

    sample_interval = max(1, int(fps // 2))
    frames_to_show, frame_count = [], 0
    mask_count, no_mask_count = 0, 0

    progress = st.progress(0, text="Starting analysis...")
    status = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % sample_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            annotated, results = predict_faces_in_frame(model, frame_rgb)
            for r in results:
                if "With Mask" in r["label"]:
                    mask_count += 1
                else:
                    no_mask_count += 1
            if len(frames_to_show) < 6:
                frames_to_show.append(annotated)
            pct = min(frame_count / max(total_frames, 1), 1.0)
            progress.progress(pct, text=f"Processing frame {frame_count}/{total_frames}...")
        frame_count += 1

    cap.release()
    os.unlink(tfile.name)
    progress.empty()
    status.empty()

    st.success("✅ Analysis complete!")
    st.markdown("---")

    total = mask_count + no_mask_count
    if total > 0:
        compliance = mask_count / total
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-val green">{mask_count}</div>
                <div class="metric-lbl">😷 With Mask</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-val red">{no_mask_count}</div>
                <div class="metric-lbl">😶 Without Mask</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-val blue">{compliance:.0%}</div>
                <div class="metric-lbl">✅ Compliance Rate</div></div>""", unsafe_allow_html=True)

    if frames_to_show:
        st.markdown("#### Sample Frames")
        cols = st.columns(3)
        for i, f in enumerate(frames_to_show[:6]):
            cols[i % 3].image(f, use_column_width=True)