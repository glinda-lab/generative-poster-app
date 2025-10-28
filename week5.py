# poster_app.py
import random, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import pandas as pd
import streamlit as st

# --- 고정 팔레트 데이터 ---
palette_df = pd.DataFrame([
    {"name": "ocean",  "r": 0.1, "g": 0.3, "b": 0.8},
    {"name": "sand",   "r": 0.9, "g": 0.8, "b": 0.5},
    {"name": "sunset", "r": 0.9, "g": 0.4, "b": 0.3},
    {"name": "forest", "r": 0.2, "g": 0.6, "b": 0.3},
    {"name": "cloud",  "r": 0.9, "g": 0.9, "b": 0.95},
])

# --- Blob shape ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 팔레트 생성 ---
def make_palette(k=6, mode="pastel", base_h=0.60, fixed_color=None):
    cols = []
    if fixed_color:  # 고정 색상 선택 시
        return [fixed_color] * k

    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15,0.35); v = random.uniform(0.9,1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8,1.0); v = random.uniform(0.8,1.0)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.2,0.6); v = random.uniform(0.5,1.0)
        else:
            h = random.random(); s = random.uniform(0.3,1.0); v = random.uniform(0.5,1.0)
        cols.append(tuple(hsv_to_rgb([h,s,v])))
    return cols

# --- 포스터 그리기 ---
def draw_poster(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0, fixed_color=None):
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor((0.97, 0.97, 0.97))

    palette = make_palette(6, mode=palette_mode, fixed_color=fixed_color)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    ax.text(0.05, 0.95, f"Interactive Poster • {palette_mode}",
            transform=ax.transAxes, fontsize=12, weight="bold")
    return fig

# --- Streamlit UI ---
st.title("🎨 Interactive Generative Poster")
st.write("Choose colors and play with randomness to generate your own poster.")

# 사이드바 옵션
n_layers = st.sidebar.slider("Layers", 3, 20, 8)
wobble = st.sidebar.slider("Wobble", 0.01, 1.0, 0.15)
palette_mode = st.sidebar.selectbox("Palette Mode", ["pastel", "vivid", "mono", "random", "custom"])
seed = st.sidebar.number_input("Seed", 0, 9999, 0)

# custom 모드일 때만 색상 선택
fixed_color = None
if palette_mode == "custom":
    color_name = st.sidebar.selectbox("Choose a base color", palette_df["name"].tolist())
    row = palette_df[palette_df["name"] == color_name].iloc[0]
    fixed_color = (row.r, row.g, row.b)

# 포스터 생성 버튼
if st.button("Generate Poster"):
    fig = draw_poster(n_layers, wobble, palette_mode, seed, fixed_color)
    st.pyplot(fig)

    # 다운로드 버튼
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button("💾 Download Poster", buf.getvalue(), "poster.png", "image/png")
