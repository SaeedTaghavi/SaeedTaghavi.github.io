"""
scripts/post_covers.py

Motivation
----------
Thumbnails for the list of posts on the Blog page. Each post names its
cover in the front matter, as `cover: img/<name>-cover.png`,
and the list shows it next to the title. The goal is one small, text-free
picture per post that matches the petrol-blue banner of the site. It is pursued by
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
* ml-intro-cover.png: three labelled clusters in the three plot colours
  among faint unlabelled points, split by dashed boundaries.
* devops-cover.png: the DevOps loop as an infinity sign, development in
  blue and operations in vermilion, with a dot for each of its eight phases.
* devops-voting-cover.png: the five parts of the voting app as boxes along
  the path a vote takes, services in blue and data stores in amber.
* ticket-routing-cover.png: a stack of tickets on the left, each drawn as a
  card with lines of text, routed by curved arrows into three queues on the
  right, in the three plot colours.
* local-llm-stack-cover.png: a laptop and a phone on the left, joined
  through one vermilion gate (nginx, the only open port) to a chat window and
  a GPU chip inside a dashed box (the Docker network nothing outside reaches).
* local-llms-metabase-mcp-cover.png: a chat bubble (the model's client) on
  the left, joined through a plug to a hub (the MCP server), which fans out to
  two tools in sky blue and a database in amber.

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

PETROL = "#1d4e6b"
PETROL_DEEP = "#0f2e42"
LIGHT = "#f26a3d"
SKY = "#8cc3e0"
AMBER = "#ffd770"
OUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "blog" / "posts" / "img"
DIGIT = Path(__file__).resolve().parent / "data" / "mnist-test-00030.png"
SIZE = (4.0, 3.0)  # 4:3, the aspect the Blog list crops to


def banner_axes(fig):
    """Petrol-blue diagonal gradient with a faint dot grid, and a clear axes on top."""
    bg = fig.add_axes([0, 0, 1, 1])
    u, v = np.meshgrid(np.linspace(0, 1, 400), np.linspace(0, 1, 300))
    cmap = LinearSegmentedColormap.from_list("banner", [PETROL, PETROL_DEEP])
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
    ax.scatter(x, y, s=6, color=SKY, alpha=0.85, linewidths=0)
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
    amber = LinearSegmentedColormap.from_list("amber", [(1, 1, 1, 0), AMBER])
    amber.set_bad((0, 0, 0, 0))

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
    right.imshow(grid, cmap=amber, interpolation="nearest", vmin=0, vmax=1)
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


def cover_ml_intro(out, dpi, seed=2):
    # Three labelled clusters in the three plot colours, a cloud of grey
    # unlabelled points around them, and the boundaries a learner would draw.
    rng = np.random.default_rng(seed)
    centres = [(-1.0, 0.55), (1.0, 0.55), (0.0, -0.85)]
    colours = [LIGHT, SKY, AMBER]

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    grey = rng.uniform((-2.2, -1.6), (2.2, 1.6), size=(160, 2))
    ax.scatter(grey[:, 0], grey[:, 1], s=7, color="white", alpha=0.25, linewidths=0)
    for (cx, cy), colour in zip(centres, colours):
        pts = rng.normal((cx, cy), 0.28, size=(45, 2))
        ax.scatter(pts[:, 0], pts[:, 1], s=16, color=colour, alpha=0.95, linewidths=0)
    dash = (0, (3, 2))
    ax.plot([0.0, 0.0], [1.6, -0.05], color="white", alpha=0.55, lw=1.4, ls=dash)
    ax.plot([-2.2, 0.0], [-0.55, -0.05], color="white", alpha=0.55, lw=1.4, ls=dash)
    ax.plot([0.0, 2.2], [-0.05, -0.55], color="white", alpha=0.55, lw=1.4, ls=dash)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.6, 1.6)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_devops(out, dpi):
    # The DevOps loop of scripts/devops_loop.py: a figure eight travelled with
    # t decreasing, development on the left lobe and operations on the right,
    # with a dot for each of the eight phases.
    t_dev = np.linspace(2 * np.pi, np.pi, 300)
    t_ops = np.linspace(np.pi, 0, 300)
    phases = np.array([1.9, 1.62, 1.38, 1.1, 0.9, 0.62, 0.38, 0.1]) * np.pi

    def lemniscate(t):
        return 1.85 * np.sin(t), 1.9 * np.sin(t) * np.cos(t)

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    for t, colour in ((t_dev, SKY), (t_ops, LIGHT)):
        ax.plot(*lemniscate(t), color=colour, lw=4.5, solid_capstyle="round")
    for t in phases:
        x, y = lemniscate(t)
        colour = SKY if t > np.pi else LIGHT
        ax.scatter(x, y, s=70, color=PETROL_DEEP, edgecolors=colour, linewidths=2.2, zorder=3)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.65, 1.65)
    ax.invert_yaxis()
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_devops_voting(out, dpi):
    # The voting app as a path of five nodes, the same Z as in
    # includes/voting-app.svg: vote, redis, worker on top, then postgres and
    # result below. Services in sky blue, data stores in amber.
    nodes = [(-1.3, 0.55, SKY), (0.0, 0.55, AMBER), (1.3, 0.55, SKY), (0.0, -0.55, AMBER), (-1.3, -0.55, SKY)]
    route = [(-1.3, 0.55), (0.0, 0.55), (1.3, 0.55), (1.3, -0.55), (0.0, -0.55), (-1.3, -0.55)]

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    xs, ys = zip(*route)
    ax.plot(xs, ys, color="white", alpha=0.45, lw=2.2, ls=(0, (3, 2)), zorder=1)
    for x, y, colour in nodes:
        ax.add_patch(
            plt.Rectangle((x - 0.42, y - 0.24), 0.84, 0.48, facecolor=PETROL_DEEP, edgecolor=colour, lw=3, zorder=2)
        )
        ax.add_patch(plt.Rectangle((x - 0.42, y - 0.24), 0.84, 0.48, facecolor=colour, alpha=0.18, lw=0, zorder=3))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.65, 1.65)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_ticket_routing(out, dpi):
    # Tickets on the left, as cards with lines of text, and three queues on
    # the right in the three plot colours. Each ticket is joined to the queue
    # it is routed to.
    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    queues = [(1.45, 0.95, LIGHT), (1.45, 0.0, SKY), (1.45, -0.95, AMBER)]
    tickets = [(-1.35, y) for y in (1.05, 0.35, -0.35, -1.05)]
    routes = [0, 1, 2, 1]
    for (tx, ty), q in zip(tickets, routes):
        qx, qy, colour = queues[q]
        ax.add_patch(
            FancyArrowPatch(
                (tx + 0.5, ty), (qx - 0.42, qy), connectionstyle="arc3,rad=-0.15",
                arrowstyle="-|>", mutation_scale=12, color=colour, lw=2, alpha=0.9, zorder=1,
            )
        )
    for tx, ty in tickets:
        ax.add_patch(
            plt.Rectangle((tx - 0.5, ty - 0.24), 1.0, 0.48, facecolor="white", alpha=0.92, lw=0, zorder=2)
        )
        for k, w in enumerate((0.75, 0.6, 0.68)):
            ax.plot([tx - 0.4, tx - 0.4 + w], [ty + 0.11 - 0.11 * k] * 2, color=PETROL, lw=1.6, alpha=0.6, zorder=3)
    for qx, qy, colour in queues:
        ax.add_patch(
            plt.Rectangle((qx - 0.4, qy - 0.3), 0.8, 0.6, facecolor=PETROL_DEEP, edgecolor=colour, lw=3, zorder=2)
        )
        ax.add_patch(plt.Rectangle((qx - 0.4, qy - 0.3), 0.8, 0.6, facecolor=colour, alpha=0.22, lw=0, zorder=3))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.65, 1.65)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def _chip(ax, x, y, half, colour, pins=4):
    """A square chip with pins on all four sides, centred at (x, y)."""
    for k in range(pins):
        p = -half + (k + 0.5) * 2 * half / pins
        for (x0, y0, x1, y1) in (
            (x + p, y + half, x + p, y + half + 0.13),
            (x + p, y - half, x + p, y - half - 0.13),
            (x + half, y + p, x + half + 0.13, y + p),
            (x - half, y + p, x - half - 0.13, y + p),
        ):
            ax.plot([x0, x1], [y0, y1], color=colour, lw=2.2, solid_capstyle="round", zorder=2)
    ax.add_patch(plt.Rectangle((x - half, y - half), 2 * half, 2 * half, facecolor=PETROL_DEEP, edgecolor=colour, lw=3, zorder=3))
    ax.add_patch(plt.Rectangle((x - half, y - half), 2 * half, 2 * half, facecolor=colour, alpha=0.22, lw=0, zorder=4))
    inner = 0.45 * half
    ax.add_patch(plt.Rectangle((x - inner, y - inner), 2 * inner, 2 * inner, facecolor=colour, alpha=0.9, lw=0, zorder=5))


def cover_local_llm_stack(out, dpi):
    # Devices on the LAN on the left, one vermilion gate (nginx), then the chat
    # window and the GPU chip inside the dashed Docker network.
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)
    dash = (0, (3, 2))

    # Docker network: everything behind the gate.
    ax.add_patch(
        FancyBboxPatch((-0.35, -1.25), 2.5, 2.5, boxstyle="round,pad=0,rounding_size=0.12",
                       facecolor="none", edgecolor="white", alpha=0.45, lw=1.6, ls=dash, zorder=1)
    )
    # Laptop: screen and base. Phone: a tall rounded rectangle.
    ax.add_patch(FancyBboxPatch((-2.05, 0.35), 0.85, 0.58, boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor="none", edgecolor="white", lw=2.4, zorder=3))
    ax.plot([-2.18, -1.07], [0.3, 0.3], color="white", lw=3, solid_capstyle="round", zorder=3)
    ax.add_patch(FancyBboxPatch((-1.88, -1.05), 0.45, 0.78, boxstyle="round,pad=0,rounding_size=0.07",
                                facecolor="none", edgecolor="white", lw=2.4, zorder=3))
    # Both devices reach the single gate.
    for (x0, y0) in ((-1.1, 0.62), (-1.38, -0.66)):
        ax.add_patch(FancyArrowPatch((x0, y0), (-0.72, 0.0), connectionstyle="arc3,rad=0.0",
                                     arrowstyle="-|>", mutation_scale=11, color="white", alpha=0.7, lw=1.8, zorder=2))
    # The gate: nginx, the only published port.
    ax.add_patch(FancyBboxPatch((-0.68, -0.62), 0.22, 1.24, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=LIGHT, edgecolor="none", zorder=4))
    ax.add_patch(FancyArrowPatch((-0.44, 0.0), (-0.12, 0.0), arrowstyle="-|>", mutation_scale=11,
                                 color=LIGHT, lw=2.2, zorder=4))
    # Chat window (Open WebUI) with two speech bubbles.
    ax.add_patch(FancyBboxPatch((-0.08, -0.62), 1.05, 1.24, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=PETROL_DEEP, edgecolor=SKY, lw=3, zorder=3))
    ax.add_patch(FancyBboxPatch((0.04, 0.12), 0.62, 0.3, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=SKY, alpha=0.9, edgecolor="none", zorder=4))
    ax.add_patch(FancyBboxPatch((0.27, -0.42), 0.58, 0.42, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="white", alpha=0.85, edgecolor="none", zorder=4))
    for k, w in enumerate((0.42, 0.32, 0.38)):
        ax.plot([0.35, 0.35 + w], [-0.1 - 0.1 * k] * 2, color=PETROL, lw=1.4, alpha=0.7, zorder=5)
    # Model on the GPU.
    ax.plot([0.99, 1.19], [0.0, 0.0], color="white", alpha=0.7, lw=2.4, solid_capstyle="round", zorder=2)
    _chip(ax, 1.62, 0.0, 0.3, AMBER)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.65, 1.65)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def cover_local_llms_metabase_mcp(out, dpi):
    # A chat bubble (the model's client) plugged into a hub (the MCP server),
    # which fans out to two tools and a database.
    from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon

    fig = plt.figure(figsize=SIZE)
    ax = banner_axes(fig)

    # Chat bubble with a tail and three dots.
    ax.add_patch(FancyBboxPatch((-2.0, -0.38), 1.0, 0.76, boxstyle="round,pad=0,rounding_size=0.18",
                                facecolor=LIGHT, edgecolor="none", zorder=3))
    ax.add_patch(Polygon([(-1.78, -0.36), (-1.9, -0.62), (-1.56, -0.36)], closed=True,
                         facecolor=LIGHT, edgecolor="none", zorder=3))
    for x in (-1.72, -1.5, -1.28):
        ax.scatter(x, 0.0, s=42, color="white", zorder=4, linewidths=0)

    # Plug: a socket on the bubble, two prongs on the hub side.
    ax.plot([-1.0, -0.62], [0, 0], color="white", lw=3, solid_capstyle="round", zorder=2)
    ax.add_patch(plt.Rectangle((-0.64, -0.17), 0.18, 0.34, facecolor="white", lw=0, zorder=3))
    for dy in (0.08, -0.08):
        ax.plot([-0.46, -0.32], [dy, dy], color="white", lw=2.4, solid_capstyle="butt", zorder=3)
    ax.plot([-0.26, -0.04], [0, 0], color="white", lw=3, alpha=0.8, solid_capstyle="round", zorder=2)

    # Hub: the MCP server.
    ax.scatter(0.25, 0.0, s=1500, color=PETROL_DEEP, edgecolors="white", linewidths=3, zorder=4)
    ax.scatter(0.25, 0.0, s=260, color="white", zorder=5, linewidths=0)

    # Spokes to two tools (sky) and a database (amber).
    targets = [(1.55, 0.95, SKY), (1.55, 0.0, AMBER), (1.55, -0.95, SKY)]
    for tx, ty, colour in targets:
        ax.add_patch(FancyArrowPatch((0.5, 0.0), (tx - 0.36, ty), connectionstyle="arc3,rad=-0.12",
                                     arrowstyle="<|-|>", mutation_scale=10, color=colour, lw=2, alpha=0.9, zorder=2))
    for tx, ty, colour in (targets[0], targets[2]):
        ax.add_patch(FancyBboxPatch((tx - 0.34, ty - 0.24), 0.68, 0.48, boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=PETROL_DEEP, edgecolor=colour, lw=3, zorder=3))
        ax.add_patch(FancyBboxPatch((tx - 0.34, ty - 0.24), 0.68, 0.48, boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=colour, alpha=0.22, edgecolor="none", zorder=4))
    # Database cylinder.
    dx, dy = targets[1][:2]
    w, h, e = 0.62, 0.5, 0.16
    ax.add_patch(plt.Rectangle((dx - w / 2, dy - h / 2), w, h, facecolor=PETROL_DEEP, lw=0, zorder=3))
    ax.add_patch(plt.Rectangle((dx - w / 2, dy - h / 2), w, h, facecolor=AMBER, alpha=0.22, lw=0, zorder=4))
    ax.plot([dx - w / 2] * 2, [dy - h / 2, dy + h / 2], color=AMBER, lw=3, zorder=5)
    ax.plot([dx + w / 2] * 2, [dy - h / 2, dy + h / 2], color=AMBER, lw=3, zorder=5)
    ax.add_patch(Ellipse((dx, dy - h / 2), w, e, facecolor=PETROL_DEEP, edgecolor=AMBER, lw=3, zorder=4))
    ax.add_patch(Ellipse((dx, dy + h / 2), w, e, facecolor=AMBER, edgecolor=AMBER, lw=3, zorder=6))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.65, 1.65)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


COVERS = {
    "euler": ("euler-maruyama-cover.png", cover_euler_maruyama),
    "infomeasure": ("infomeasure-cover.png", cover_infomeasure),
    "lenet": ("lenet-web-app-cover.png", cover_lenet),
    "ml-intro": ("ml-intro-cover.png", cover_ml_intro),
    "devops": ("devops-cover.png", cover_devops),
    "devops-voting": ("devops-voting-cover.png", cover_devops_voting),
    "ticket-routing": ("ticket-routing-cover.png", cover_ticket_routing),
    "local-llm-stack": ("local-llm-stack-cover.png", cover_local_llm_stack),
    "mcp-metabase": ("local-llms-metabase-mcp-cover.png", cover_local_llms_metabase_mcp),
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
