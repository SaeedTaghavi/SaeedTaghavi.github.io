"""
scripts/post_covers.py

Motivation
----------
Thumbnails for the list of posts on the Blog page. Each post names its
cover in the front matter, as `cover: img/<name>-cover.png`,
and the list shows it next to the title. The goal is one small, text-free
picture per post that matches the navy banner of the site. It is pursued by
drawing each post's central object on the banner gradient and dot texture.

What it measures
----------------
Nothing new. It redraws, at thumbnail scale:
* euler-maruyama-cover.png: one noisy path of the harmonic oscillator in the
  phase plane, over the closed orbit without noise.
* infomeasure-cover.png: a noisy circle, with its flat least-squares line,
  the dependence that correlation misses and mutual information finds.
* lenet-web-app-cover.png: one MNIST test digit, smooth on the left and as the
  28 x 28 grid of pixels that LeNet-5 receives on the right. The digit is
  test image 30, a 3, stored in scripts/data/.

Usage
-----
    python scripts/post_covers.py
    python scripts/post_covers.py --only infomeasure
    python scripts/post_covers.py --dpi 600
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch

from euler_maruyama_sho import euler_maruyama_sho

NAVY = "#1e3a8a"
NAVY_DEEP = "#0f1f4d"
LIGHT = "#93b4ff"
OUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "writing" / "posts" / "img"
DIGIT = Path(__file__).resolve().parent / "data" / "mnist-test-00030.png"
SIZE = (4.0, 3.0)  # 4:3, the aspect the Blog list crops to


def banner_axes(fig):
    """Navy diagonal gradient with a faint dot grid, and a clear axes on top."""
    bg = fig.add_axes([0, 0, 1, 1])
    u, v = np.meshgrid(np.linspace(0, 1, 400), np.linspace(0, 1, 300))
    cmap = LinearSegmentedColormap.from_list("banner", [NAVY, NAVY_DEEP])
    bg.imshow(0.5 * (u + v), cmap=cmap, extent=(0, 4, 0, 3), aspect="auto")
    gx, gy = np.meshgrid(np.arange(0.1, 4, 0.2), np.arange(0.1, 3, 0.2))
    bg.scatter(gx, gy, s=0.6, color="white", alpha=0.12, linewidths=0)
    bg.set_xlim(0, 4)
    bg.set_ylim(0, 3)
    bg.axis("off")

    ax = fig.add_axes([0.08, 0.08, 0.84, 0.84])
    ax.set_facecolor("none")
    ax.axis("off")
    return ax


def cover_euler_maruyama(out, dpi, seed=5):
    omega, sigma, dt, T = 2.0, 0.6, 0.01, 25.0
    n = int(round(T / dt))
    x_det, v_det = euler_maruyama_sho(
        1.0, 0.0, omega, 0.0, dt, n, 1, np.random.default_rng(0)
    )
    x, v = euler_maruyama_sho(
        1.0, 0.0, omega, sigma, dt, n, 1, np.random.default_rng(seed)
    )

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    ax.plot(x[:, 0], v[:, 0], color=LIGHT, lw=0.9, alpha=0.85)
    ax.plot(x_det[:, 0], v_det[:, 0], color="white", lw=2.6)
    lim_x = 1.15 * np.abs(x).max()
    lim_v = 1.15 * np.abs(v).max()
    ax.set_xlim(-lim_x, lim_x)
    ax.set_ylim(-lim_v, lim_v)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_infomeasure(out, dpi, seed=0):
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0.0, 2.0 * np.pi, 1500)
    x = np.cos(theta) + 0.05 * rng.standard_normal(theta.size)
    y = np.sin(theta) + 0.05 * rng.standard_normal(theta.size)
    slope, intercept = np.polyfit(x, y, 1)

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    ax.scatter(x, y, s=6, color="white", alpha=0.8, linewidths=0)
    xs = np.array([-1.9, 1.9])
    ax.plot(xs, slope * xs + intercept, color=LIGHT, lw=2.6, ls=(0, (3, 2)))
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.35, 1.35)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_lenet(out, dpi, cell=12, gap=2):
    digit = plt.imread(DIGIT)  # 28 x 28 grayscale, values in [0, 1]
    if digit.ndim == 3:
        digit = digit[..., 0]
    n = digit.shape[0]
    white = LinearSegmentedColormap.from_list("ink", [(1, 1, 1, 0), (1, 1, 1, 1)])
    white.set_bad((0, 0, 0, 0))

    # Every pixel becomes a cell x cell block with a transparent gap around it.
    # Empty pixels keep a faint floor so the 28 x 28 grid stays visible.
    grid = np.full((n * cell, n * cell), np.nan)
    for i in range(n):
        for j in range(n):
            r, c = i * cell, j * cell
            grid[r : r + cell - gap, c : c + cell - gap] = 0.1 + 0.9 * digit[i, j]

    fig = plt.figure(figsize=SIZE)
    banner_axes(fig)
    side = 0.4 * SIZE[0] / SIZE[1]  # square panels in figure coordinates
    left = fig.add_axes([0.04, 0.5 - side / 2, 0.4, side])
    right = fig.add_axes([0.56, 0.5 - side / 2, 0.4, side])
    left.imshow(digit, cmap=white, interpolation="bicubic", vmin=0, vmax=1)
    right.imshow(grid, cmap=white, interpolation="nearest", vmin=0, vmax=1)
    for a in (left, right):
        a.set_facecolor("none")
        a.axis("off")
    fig.add_artist(
        FancyArrowPatch(
            (0.455, 0.5),
            (0.545, 0.5),
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=16,
            lw=2.4,
            color=LIGHT,
        )
    )
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


COVERS = {
    "euler": ("euler-maruyama-cover.png", cover_euler_maruyama),
    "infomeasure": ("infomeasure-cover.png", cover_infomeasure),
    "lenet": ("lenet-web-app-cover.png", cover_lenet),
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", choices=sorted(COVERS), default=None)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--dpi", type=int, default=300)
    return parser.parse_args()


def main():
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for key, (name, draw) in COVERS.items():
        if args.only and key != args.only:
            continue
        out = args.out_dir / name
        draw(out, args.dpi)
        print(f"saved {out}")


if __name__ == "__main__":
    main()
