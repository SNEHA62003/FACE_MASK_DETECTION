"""
Face Mask Detection - Main Entry Point (Redesigned UI)
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Face Mask Detector",
    page_icon="😷",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
    color: #f0f0f5;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0533 0%, #0a0a0f 50%),
                radial-gradient(ellipse at 80% 80%, #001a33 0%, transparent 60%);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: rgba(15, 10, 30, 0.95) !important;
    border-right: 1px solid rgba(150, 80, 255, 0.2) !important;
}
[data-testid="stSidebar"] * { color: #d0c0ff !important; font-family: 'DM Sans', sans-serif !important; }

.hero-section { text-align: center; padding: 60px 20px 40px; }

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(191,95,255,0.15), rgba(80,180,255,0.15));
    border: 1px solid rgba(191,95,255,0.4);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #bf5fff;
    margin-bottom: 24px;
    animation: fadeDown 0.6s ease both;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(42px, 6vw, 82px);
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 20px;
    animation: fadeDown 0.75s ease both;
}
.grad1 {
    background: linear-gradient(135deg, #ffffff 0%, #d0b0ff 50%, #bf5fff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.grad2 {
    background: linear-gradient(135deg, #50b4ff 0%, #00e5ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero-sub {
    font-size: 17px; color: #8888aa; max-width: 520px;
    margin: 0 auto 48px; line-height: 1.7;
    animation: fadeDown 0.9s ease both;
}

.stats-row {
    display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;
    margin-bottom: 60px; animation: fadeUp 0.9s ease both;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 20px 32px; text-align: center; min-width: 130px;
    transition: transform 0.3s, border-color 0.3s;
}
.stat-card:hover { transform: translateY(-5px); border-color: rgba(191,95,255,0.5); }
.stat-number {
    font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800;
    background: linear-gradient(135deg, #bf5fff, #50b4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 11px; color: #555577; margin-top: 4px; text-transform: uppercase; letter-spacing: 1.5px; }

.cards-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
    max-width: 960px; margin: 0 auto 60px; padding: 0 20px;
    animation: fadeUp 1s ease both;
}
.feature-card {
    border-radius: 22px; padding: 32px 26px; position: relative; overflow: hidden;
    cursor: pointer; transition: transform 0.35s cubic-bezier(.22,.68,0,1.2), box-shadow 0.35s;
    text-decoration: none; display: block;
}
.feature-card:hover { transform: translateY(-9px) scale(1.02); }

.card-purple {
    background: linear-gradient(140deg, rgba(100,30,180,0.55) 0%, rgba(50,10,110,0.75) 100%);
    border: 1px solid rgba(191,95,255,0.35);
    box-shadow: 0 8px 40px rgba(150,50,255,0.15);
}
.card-purple:hover { box-shadow: 0 24px 64px rgba(150,50,255,0.4); border-color: rgba(191,95,255,0.7); }

.card-cyan {
    background: linear-gradient(140deg, rgba(0,80,160,0.55) 0%, rgba(0,40,100,0.75) 100%);
    border: 1px solid rgba(80,180,255,0.35);
    box-shadow: 0 8px 40px rgba(0,150,255,0.12);
}
.card-cyan:hover { box-shadow: 0 24px 64px rgba(0,150,255,0.35); border-color: rgba(80,180,255,0.7); }

.card-pink {
    background: linear-gradient(140deg, rgba(180,30,100,0.55) 0%, rgba(100,10,60,0.75) 100%);
    border: 1px solid rgba(255,80,160,0.35);
    box-shadow: 0 8px 40px rgba(255,50,150,0.12);
}
.card-pink:hover { box-shadow: 0 24px 64px rgba(255,50,150,0.4); border-color: rgba(255,80,160,0.7); }

.card-icon { font-size: 44px; margin-bottom: 18px; display: block; }
.card-title { font-family: 'Syne', sans-serif; font-size: 21px; font-weight: 700; color: #fff; margin-bottom: 10px; }
.card-desc { font-size: 13.5px; color: rgba(255,255,255,0.5); line-height: 1.7; }
.card-tag {
    display: inline-block; margin-top: 18px;
    background: rgba(255,255,255,0.08); border-radius: 50px;
    padding: 4px 14px; font-size: 11px; color: rgba(255,255,255,0.5);
    letter-spacing: 1px; text-transform: uppercase;
}
.card-arrow {
    position: absolute; bottom: 22px; right: 26px; font-size: 22px;
    opacity: 0; transform: translateX(-8px);
    transition: opacity 0.3s, transform 0.3s; color: rgba(255,255,255,0.7);
}
.feature-card:hover .card-arrow { opacity: 1; transform: translateX(0); }

.section-wrap { max-width: 960px; margin: 0 auto 56px; padding: 0 20px; animation: fadeUp 1.05s ease both; }
.section-label {
    font-family: 'Syne', sans-serif; font-size: 11px;
    letter-spacing: 3.5px; text-transform: uppercase;
    color: #bf5fff; margin-bottom: 18px;
}
.info-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.info-pill {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 16px 18px;
    transition: border-color 0.3s, background 0.3s;
}
.info-pill:hover { background: rgba(191,95,255,0.08); border-color: rgba(191,95,255,0.35); }
.info-pill-label { font-size: 10px; color: #444466; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
.info-pill-value { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 600; color: #e0d0ff; }

.pipeline-wrap { max-width: 960px; margin: 0 auto 56px; padding: 0 20px; animation: fadeUp 1.1s ease both; }
.pipeline-label {
    font-family: 'Syne', sans-serif; font-size: 11px;
    letter-spacing: 3.5px; text-transform: uppercase;
    color: #50b4ff; margin-bottom: 18px;
}
.pipeline-steps { display: flex; align-items: center; gap: 4px; overflow-x: auto; padding-bottom: 6px; }
.p-step {
    flex: 1; min-width: 105px;
    background: rgba(80,180,255,0.05); border: 1px solid rgba(80,180,255,0.15);
    border-radius: 14px; padding: 16px 10px; text-align: center;
    transition: background 0.3s, border-color 0.3s;
}
.p-step:hover { background: rgba(80,180,255,0.12); border-color: rgba(80,180,255,0.45); }
.p-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: linear-gradient(135deg, #50b4ff, #00e5ff);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #000;
    margin: 0 auto 8px; font-family: 'Syne', sans-serif;
}
.p-label { font-size: 11px; color: #6688aa; line-height: 1.45; }
.p-arrow { color: rgba(80,180,255,0.25); font-size: 18px; padding: 0 2px; flex-shrink: 0; }

.footer { text-align: center; padding: 28px; font-size: 12px; color: #2a2a44; border-top: 1px solid rgba(255,255,255,0.04); }
.footer span { color: #bf5fff; }

/* Fixed background orbs */
.orb { position: fixed; border-radius: 50%; filter: blur(90px); pointer-events: none; z-index: -1; }
.orb1 { width: 500px; height: 500px; background: #3d0088; top: -150px; left: -150px; opacity: 0.35; }
.orb2 { width: 350px; height: 350px; background: #003399; bottom: 50px; right: -80px; opacity: 0.3; }
.orb3 { width: 250px; height: 250px; background: #880040; top: 50%; left: 50%; transform: translate(-50%,-50%); opacity: 0.15; }

@keyframes fadeDown { from { opacity: 0; transform: translateY(-22px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeUp   { from { opacity: 0; transform: translateY(22px);  } to { opacity: 1; transform: translateY(0); } }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>

<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>

<div class="hero-section">
    <div class="hero-badge">🧠 Deep Learning &nbsp;·&nbsp; CNN &nbsp;·&nbsp; TensorFlow</div>
    <div class="hero-title">
        <span class="grad1">Face Mask</span><br>
        <span class="grad2">Detection System</span>
    </div>
    <p class="hero-sub">
        Real-time mask compliance powered by a custom Convolutional Neural Network.
        Analyze images, videos, and live webcam feeds instantly.
    </p>
</div>

<div class="stats-row">
    <div class="stat-card"><div class="stat-number">128²</div><div class="stat-label">Input Size</div></div>
    <div class="stat-card"><div class="stat-number">3</div><div class="stat-label">Conv Blocks</div></div>
    <div class="stat-card"><div class="stat-number">2</div><div class="stat-label">Classes</div></div>
    <div class="stat-card"><div class="stat-number">~95%</div><div class="stat-label">Val Accuracy</div></div>
    <div class="stat-card"><div class="stat-number">Adam</div><div class="stat-label">Optimizer</div></div>
</div>

<div class="cards-grid">
    <a class="feature-card card-purple" href="/Image_Detection">
        <span class="card-icon">📷</span>
        <div class="card-title">Image Detection</div>
        <p class="card-desc">Upload any photo. Detects all faces in the frame and classifies mask status per face with bounding boxes.</p>
        <span class="card-tag">JPG · PNG · JPEG</span>
        <span class="card-arrow">→</span>
    </a>
    <a class="feature-card card-cyan" href="/Video_Detection">
        <span class="card-icon">🎬</span>
        <div class="card-title">Video Detection</div>
        <p class="card-desc">Frame-by-frame analysis of uploaded video files with compliance rate metrics and annotated sample frames.</p>
        <span class="card-tag">MP4 · AVI · MOV</span>
        <span class="card-arrow">→</span>
    </a>
    <a class="feature-card card-pink" href="/Webcam_Detection">
        <span class="card-icon">📹</span>
        <div class="card-title">Webcam Detection</div>
        <p class="card-desc">Snap a live photo from your camera for instant mask detection with real-time confidence scores.</p>
        <span class="card-tag">Live Camera</span>
        <span class="card-arrow">→</span>
    </a>
</div>

<div class="section-wrap">
    <div class="section-label">⚙ Model Architecture</div>
    <div class="info-grid">
        <div class="info-pill"><div class="info-pill-label">Framework</div><div class="info-pill-value">TensorFlow / Keras</div></div>
        <div class="info-pill"><div class="info-pill-label">Architecture</div><div class="info-pill-value">Custom CNN</div></div>
        <div class="info-pill"><div class="info-pill-label">Optimizer</div><div class="info-pill-value">Adam + LR Decay</div></div>
        <div class="info-pill"><div class="info-pill-label">Loss</div><div class="info-pill-value">Binary Crossentropy</div></div>
        <div class="info-pill"><div class="info-pill-label">Regularization</div><div class="info-pill-value">BatchNorm + Dropout</div></div>
        <div class="info-pill"><div class="info-pill-label">Augmentation</div><div class="info-pill-value">Rotation / Flip / Zoom</div></div>
        <div class="info-pill"><div class="info-pill-label">Face Detection</div><div class="info-pill-value">Haar Cascade</div></div>
        <div class="info-pill"><div class="info-pill-label">Output Layer</div><div class="info-pill-value">Sigmoid (Binary)</div></div>
    </div>
</div>

<div class="pipeline-wrap">
    <div class="pipeline-label">⚡ Detection Pipeline</div>
    <div class="pipeline-steps">
        <div class="p-step"><div class="p-num">1</div><div class="p-label">Input Image / Frame</div></div>
        <div class="p-arrow">›</div>
        <div class="p-step"><div class="p-num">2</div><div class="p-label">Face Detection (Haar)</div></div>
        <div class="p-arrow">›</div>
        <div class="p-step"><div class="p-num">3</div><div class="p-label">Crop & Resize 128×128</div></div>
        <div class="p-arrow">›</div>
        <div class="p-step"><div class="p-num">4</div><div class="p-label">Normalize Pixels 0–1</div></div>
        <div class="p-arrow">›</div>
        <div class="p-step"><div class="p-num">5</div><div class="p-label">CNN Inference</div></div>
        <div class="p-arrow">›</div>
        <div class="p-step"><div class="p-num">6</div><div class="p-label">Mask / No Mask + Confidence</div></div>
    </div>
</div>

<div class="footer">
    Built with <span>TensorFlow</span> &nbsp;·&nbsp; <span>Streamlit</span> &nbsp;·&nbsp; <span>OpenCV</span> &nbsp;·&nbsp; <span>Keras</span>
</div>
""", unsafe_allow_html=True)