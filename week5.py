# poster_app.py
import random, math, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import pandas as pd
import streamlit as st

# --- Blob shape ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- CSV palette loader ---
def read_palette(filename="colors20_palette.csv"):
    if not os.path.exists(filename):
        st.warning("⚠️ No CSV palette found. Using random colors instead.")
        return pd.DataFrame({"r": [], "g": [], "b": []})
    return pd.read_csv(filename)

def load_csv_palette(filename="colors20_palette.csv"):
    df = read_palette(filename)
    if df.empty:
        return [(random.random(), random.random(), random.random()) for _ in range(6)]
    return [(row.r, row.g, row.b) for row in df.itertuples()]

# --- Palette generator ---
def make_palette(k=6, mode="pastel", base_h=0.60):
    cols = []
    if mode == "csv":
        return load_csv_palette()
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

# --- Draw poster ---
def draw_poster(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0):
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor((0.97, 0.97, 0.97))

    palette = make_palette(6, mode=palette_mode)
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
st.write("Explore color palettes, randomness, and shape layering.")

# Sidebar controls
n_layers = st.sidebar.slider("Layers", 3, 20, 8)
wobble = st.sidebar.slider("Wobble", 0.01, 1.0, 0.15)
palette_mode = st.sidebar.selectbox("Palette Mode", ["pastel", "vivid", "mono", "random", "csv"])
seed = st.sidebar.number_input("Seed", 0, 9999, 0)

# Generate poster
if st.button("Generate Poster"):
    fig = draw_poster(n_layers=n_layers, wobble=wobble, palette_mode=palette_mode, seed=seed)
    st.pyplot(fig)

    # Download button
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button("💾 Download Poster", buf.getvalue(), "poster.png", "image/png")
