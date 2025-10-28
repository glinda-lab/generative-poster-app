# poster_app.py
import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---- Blob Shape ----
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * np.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ---- Poster Function ----
def natural_3d_poster(n_layers=12, seed=None):
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')
    ax.set_facecolor((0.93, 0.94, 0.97))

    # Random Palette
    palette = [(random.random(), random.random(), random.random()) for _ in range(6)]

    for i in range(n_layers):
        depth = i / (n_layers - 1 + 1e-6)

        # Random position, size, wobble
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.1, 0.35)
        wobble = random.uniform(0.05, 0.25)
        x, y = blob(center=(cx, cy), r=rr, wobble=wobble)

        # Shadow
        shadow_offset_x = random.uniform(0.01, 0.04) * (1 - depth)
        shadow_offset_y = random.uniform(-0.04, -0.01) * (1 - depth)
        shadow_alpha = random.uniform(0.1, 0.3) * (1 - depth)
        ax.fill(x + shadow_offset_x, y + shadow_offset_y, color=(0, 0, 0),
                alpha=shadow_alpha, edgecolor="none", zorder=i)

        # Color + transparency
        alpha = random.uniform(0.3, 0.7) * (1 - depth) + 0.2
        color = random.choice(palette)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor="none", zorder=i + 1)

    # Title
    ax.text(0.05, 0.95, "3D-Like Generative Poster", fontsize=16, weight="bold",
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    return fig


# ---- Streamlit UI ----
st.title("🌀 Natural 3D Generative Poster")
st.write("Create abstract, layered 3D-like posters with random colors and depth effects.")

# Sidebar controls
n_layers = st.sidebar.slider("Number of Layers", 3, 20, 12)
seed_input = st.sidebar.text_input("Random Seed (optional)", "")
generate_btn = st.sidebar.button("🎨 Generate Poster")

# Generate poster
if generate_btn:
    seed = int(seed_input) if seed_input.strip().isdigit() else None
    fig = 3d_poster(n_layers=n_layers, seed=seed)

    # Show image
    st.pyplot(fig)

    # Save to PNG for download
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button("💾 Download Poster", buf.getvalue(), "3D_poster.png", "image/png")
