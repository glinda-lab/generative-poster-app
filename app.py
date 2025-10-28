# poster_app.py

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---- Functions ----
def random_palette(k=5):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ---- Streamlit UI ----
st.title("🎨 Generative Abstract Poster")
st.write("Experiment with randomness, layering, and palettes in Python + Streamlit.")

# Sidebar controls
n_layers = st.sidebar.slider("Number of layers", 3, 20, 8)
wobble_range = st.sidebar.slider("Wobble range", 0.0, 0.5, (0.05, 0.25))
palette_size = st.sidebar.slider("Palette size", 3, 10, 6)
seed = st.sidebar.number_input("Random seed (0 for random)", 0, 99999, 0)

if seed != 0:
    random.seed(seed)
else:
    random.seed()

# ---- Generate poster ----
palette = random_palette(palette_size)
fig, ax = plt.subplots(figsize=(7, 10))
ax.axis("off")
ax.set_facecolor((0.98, 0.98, 0.97))

for i in range(n_layers):
    cx, cy = random.random(), random.random()
    rr = random.uniform(0.15, 0.45)
    x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(*wobble_range))
    color = random.choice(palette)
    alpha = random.uniform(0.25, 0.6)
    ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

# Text labels
ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight="bold", transform=ax.transAxes)
ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

# ---- Display & Download ----
st.pyplot(fig)

# Save to file
import io
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
st.download_button("💾 Download Poster", buf.getvalue(), "poster.png", "image/png")
