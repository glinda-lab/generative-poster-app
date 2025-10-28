import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import pandas as pd
import io
from matplotlib.colors import hsv_to_rgb

# ----- basic color palette -----
palette_df = pd.DataFrame([
    {"name": "ocean",  "r": 0.1, "g": 0.3, "b": 0.8},
    {"name": "sand",   "r": 0.9, "g": 0.8, "b": 0.5},
    {"name": "sunset", "r": 0.9, "g": 0.4, "b": 0.3},
    {"name": "forest", "r": 0.2, "g": 0.6, "b": 0.3},
    {"name": "cloud",  "r": 0.9, "g": 0.9, "b": 0.95},
])

# ----- generate palette -----
def make_palette(mode="pastel", k=6):
    """Return a list of RGB tuples."""
    cols = []

    if mode in palette_df["name"].tolist():
        row = palette_df[palette_df["name"] == mode].iloc[0]
        return [(row.r, row.g, row.b)]

    for _ in range(k):
        if mode == "pastel":
            h = random.random()
            s = random.uniform(0.2, 0.4)
            v = random.uniform(0.9, 1.0)
        elif mode == "vivid":
            h = random.random()
            s = random.uniform(0.8, 1.0)
            v = random.uniform(0.8, 1.0)
        elif mode == "mono":
            v = random.uniform(0.3, 0.9)
            s = 0
            h = 0
        else:
            h = random.random()
            s = random.uniform(0.3, 1.0)
            v = random.uniform(0.5, 1.0)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

# ----- shape function -----
def shape_circle(center=(0.5, 0.5), r=0.2, points=200):
    angles = np.linspace(0, 2 * math.pi, points)
    x = center[0] + r * np.cos(angles)
    y = center[1] + r * np.sin(angles)
    return x, y

def shape_square(center=(0.5, 0.5), size=0.3):
    x0, y0 = center
    half = size / 2
    x = [x0 - half, x0 + half, x0 + half, x0 - half, x0 - half]
    y = [y0 - half, y0 - half, y0 + half, y0 + half, y0 - half]
    return np.array(x), np.array(y)

def shape_star(center=(0.5, 0.5), r1=0.3, r2=0.15, num_points=5):
    angles = np.linspace(0, 2 * math.pi, num_points * 2 + 1)
    radii = np.empty_like(angles)
    radii[::2] = r1
    radii[1::2] = r2
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ----- 3Dlike -----
def draw_shape_3d(ax, shape_type, palette, n_layers=12):
    for i in range(n_layers):
        depth = i / (n_layers - 1 + 1e-6)
        cx, cy = random.random(), random.random()
        size = random.uniform(0.1, 0.35)

        # 도형 선택
        if shape_type == "circle":
            x, y = shape_circle((cx, cy), r=size)
        elif shape_type == "square":
            x, y = shape_square((cx, cy), size=size)
        elif shape_type == "star":
            x, y = shape_star((cx, cy), r1=size, r2=size*0.5)
        else:
            continue

        # shadow
        shadow_offset_x = random.uniform(0.01, 0.03) * (1 - depth)
        shadow_offset_y = random.uniform(-0.03, -0.01) * (1 - depth)
        shadow_alpha = random.uniform(0.1, 0.25) * (1 - depth)
        ax.fill(x + shadow_offset_x, y + shadow_offset_y, color=(0, 0, 0),
                alpha=shadow_alpha, zorder=i)

        # color transparency
        color = random.choice(palette)
        alpha = random.uniform(0.35, 0.7) * (1 - depth) + 0.2
        ax.fill(x, y, color=color, alpha=alpha, zorder=i+1)  # 윤곽선 제거됨

# ----- generate poster -----
def generate_poster(shape_type="circle", color_mode="pastel", n_layers=12, seed=0):
    random.seed(seed)
    np.random.seed(seed)

    palette = make_palette(color_mode, k=6)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor((0.93, 0.94, 0.97))

    draw_shape_3d(ax, shape_type, palette, n_layers)
    ax.text(0.05, 0.95, f"3D-like {shape_type.capitalize()} • {color_mode}",
            transform=ax.transAxes, fontsize=12, weight="bold")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# ----- Streamlit UI -----
st.title("🌀 Final generative abstract poster")
st.write("Create posters with 3D-like geometric depth illusion using colors and shadows.")

shape_type = st.sidebar.selectbox("Shape", ["circle", "square", "star"])
color_mode = st.sidebar.selectbox("Color Mode", 
    ["ocean", "sand", "sunset", "forest", "cloud", "pastel", "vivid", "mono"])
n_layers = st.sidebar.slider("Number of Layers (Depth)", 3, 20, 12)
seed = st.sidebar.number_input("Seed", 0, 9999, 0)

if st.button("🎨 Generate Poster"):
    fig = generate_poster(shape_type, color_mode, n_layers, seed)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button("💾 Download Poster", buf.getvalue(), "poster_3d.png", "image/png")
