# poster_app.py
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---- Helper functions ----
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(mode="pastel", k=5):
    if mode.lower() == "vivid":
        return [(random.random(), random.random(), random.random()) for _ in range(k)]
    elif mode.lower() == "muted":
        return [(random.uniform(0.2, 0.7), random.uniform(0.2, 0.7), random.uniform(0.2, 0.7)) for _ in range(k)]
    elif mode.lower() == "pastel":
        return [(0.7 + 0.3*random.random(), 0.7 + 0.3*random.random(), 0.7 + 0.3*random.random()) for _ in range(k)]
    else:
        return [(random.random(), random.random(), random.random()) for _ in range(k)]

# ---- Main generator ----
def generate_poster(style="Pastel", figsize=(7,10), seed=None, filename=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    else:
        random.seed()
        np.random.seed(None)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    ax.set_facecolor((0.98, 0.98, 0.97))

    # Styles
    if style.lower() == "minimal":
        n_layers = 4
        wobble_range = (0.02, 0.1)
        palette = make_palette("muted", k=5)
    elif style.lower() == "vivid":
        n_layers = 12
        wobble_range = (0.05, 0.2)
        palette = make_palette("vivid", k=8)
    elif style.lower() == "noisetouch":
        n_layers = 10
        wobble_range = (0.15, 0.4)
        palette = make_palette("pastel", k=6)
    else:  # pastel default
        n_layers = 8
        wobble_range = (0.05, 0.25)
        palette = make_palette("pastel", k=6)

    # Draw blobs
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        wobble = random.uniform(*wobble_range)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    # Labels
    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, f"Style: {style}, Seed: {seed}", fontsize=11, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    if filename:
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    return fig


# ---- Streamlit interface ----
st.title("🎨 Generative Abstract Poster")
st.write("Create your own randomized art poster using different visual styles.")

style = st.sidebar.selectbox("Choose a Style", ["Pastel", "Vivid", "Minimal", "NoiseTouch"])
seed_input = st.sidebar.text_input("Seed (optional)", "")
generate_btn = st.sidebar.button("🎲 Generate Poster")

if generate_btn:
    seed = int(seed_input) if seed_input.strip().isdigit() else None
    fig = generate_poster(style=style, seed=seed)

    # Show the result
    st.pyplot(fig)

    # Download button
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button("💾 Download Poster", buf.getvalue(), f"{style}_poster.png", "image/png")
