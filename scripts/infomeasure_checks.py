"""
scripts/infomeasure_checks.py

Motivation
----------
Figure for the blog post "Mutual information and transfer entropy in Python
with infomeasure". The goal is to show, on data whose answer is known, that
the library's estimators find what correlation misses and agree with theory.
It is pursued with two small experiments taken from the notebook
https://github.com/SaeedTaghavi/infomeasure_tutorial, both estimated with
the same infomeasure call that the notebook uses.

What it measures
----------------
* A noisy circle: Pearson's r against the mutual information I(X; Y).
* A linear driven process with white-noise input x,

      y[t] = beta * y[t-1] + gamma * x[t-1] + eps[t],

  for a range of couplings gamma: the transfer entropy TE(x -> y) against
  the analytical value 0.5 * log(1 + gamma^2 sigma_x^2 / sigma_y^2), with the
  reverse direction TE(y -> x) and an uncoupled control TE(x -> x2).
  Information is in nats.

Usage
-----
    pip install -r scripts/requirements.txt
    python scripts/infomeasure_checks.py
    python scripts/infomeasure_checks.py --T 20000 --approach metric
    python scripts/infomeasure_checks.py --out /tmp/im.png --dpi 600
"""

import argparse
from pathlib import Path

import infomeasure as im
import matplotlib.pyplot as plt
import numpy as np

INK = "#0f172a"
MUTED = "#9ba8bf"
ACCENT = "#1e3a8a"
DEFAULT_OUT = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "writing"
    / "posts"
    / "img"
    / "infomeasure-checks.png"
)


def noisy_circle(n, noise, rng):
    """Points on the unit circle with Gaussian jitter on both coordinates."""
    theta = rng.uniform(0.0, 2.0 * np.pi, n)
    x = np.cos(theta) + noise * rng.standard_normal(n)
    y = np.sin(theta) + noise * rng.standard_normal(n)
    return x, y


def driven_pair(T, beta, gamma, sigma_x, sigma_y, rng, burn_in=10):
    """Source x, driven target y and an independent control x2."""
    x = sigma_x * rng.standard_normal(T + burn_in)
    x2 = sigma_x * rng.standard_normal(T + burn_in)
    eps = sigma_y * rng.standard_normal(T + burn_in)
    y = np.zeros(T + burn_in)
    for t in range(1, T + burn_in):
        y[t] = beta * y[t - 1] + gamma * x[t - 1] + eps[t]
    return x[burn_in:], y[burn_in:], x2[burn_in:]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--n-circle", type=int, default=2000)
    parser.add_argument("--noise", type=float, default=0.05)
    parser.add_argument("--T", type=int, default=5000)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("--sigma-x", type=float, default=1.0)
    parser.add_argument("--sigma-y", type=float, default=1.0)
    parser.add_argument("--gamma-max", type=float, default=1.4)
    parser.add_argument("--n-gamma", type=int, default=15)
    parser.add_argument("--approach", default="renyi")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--dpi", type=int, default=300)
    return parser.parse_args()


def main():
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    kw = {"approach": args.approach}
    if args.approach in ("renyi", "tsallis"):
        kw["alpha" if args.approach == "renyi" else "q"] = 1.0

    # Experiment 1: a dependence that correlation cannot see.
    cx, cy = noisy_circle(args.n_circle, args.noise, rng)
    r = np.corrcoef(cx, cy)[0, 1]
    mi = im.mutual_information(cx, cy, **kw)
    slope, intercept = np.polyfit(cx, cy, 1)

    # Experiment 2: directed information flow against the analytical value.
    gammas = np.linspace(0.0, args.gamma_max, args.n_gamma)
    te_xy, te_yx, te_ctrl = [], [], []
    for gamma in gammas:
        x, y, x2 = driven_pair(
            args.T, args.beta, gamma, args.sigma_x, args.sigma_y, rng
        )
        te_xy.append(im.transfer_entropy(x, y, **kw))
        te_yx.append(im.transfer_entropy(y, x, **kw))
        te_ctrl.append(im.transfer_entropy(x, x2, **kw))
    g_fine = np.linspace(0.0, args.gamma_max, 200)
    te_theory = 0.5 * np.log(1.0 + g_fine**2 * args.sigma_x**2 / args.sigma_y**2)

    fig, ax = plt.subplot_mosaic(
        [["circle", "te"]],
        figsize=(10, 4.2),
        width_ratios=[1, 1.35],
        layout="constrained",
    )

    a = ax["circle"]
    a.scatter(cx, cy, s=3, color=INK, alpha=0.5, linewidths=0)
    xs = np.array([-1.3, 1.3])
    a.plot(xs, slope * xs + intercept, color=ACCENT, lw=1.4, ls="--")
    a.set_aspect("equal")
    a.set_xlim(-1.35, 1.35)
    a.set_ylim(-1.35, 1.35)
    a.set_xlabel(r"$X$")
    a.set_ylabel(r"$Y$")
    a.set_title(
        rf"Pearson $r = {r:.2f}$,   $I(X;Y) = {mi:.2f}$ nats",
        loc="left",
        fontsize=10,
    )

    a = ax["te"]
    a.plot(g_fine, te_theory, color=INK, lw=1.4, label="analytical")
    a.plot(
        gammas,
        te_xy,
        "o",
        color=ACCENT,
        ms=5,
        label=r"$TE_{x \to y}$, estimated",
    )
    a.plot(gammas, te_yx, "s", color=MUTED, ms=4, label=r"$TE_{y \to x}$, reverse")
    a.plot(
        gammas,
        te_ctrl,
        "^",
        mfc="none",
        color=MUTED,
        ms=5,
        label=r"$TE_{x \to x_2}$, uncoupled control",
    )
    a.axhline(0.0, color=MUTED, lw=0.6)
    a.set_xlabel(r"coupling $\gamma$")
    a.set_ylabel("transfer entropy (nats)")
    a.legend(loc="upper left", frameon=False)

    for a in ax.values():
        a.spines[["top", "right"]].set_visible(False)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=args.dpi)

    ratio = args.sigma_x**2 / args.sigma_y**2
    err = np.abs(np.array(te_xy) - 0.5 * np.log(1.0 + gammas**2 * ratio))
    print(f"saved {args.out}")
    print(f"estimator: {kw}")
    print(f"circle: Pearson r = {r:.3f}, MI = {mi:.3f} nats")
    print(f"TE x->y: max |estimate - theory| = {err.max():.3f} nats")
    print(
        f"TE y->x: max |value| = {np.abs(te_yx).max():.3f}; "
        f"control: max |value| = {np.abs(te_ctrl).max():.3f}"
    )


if __name__ == "__main__":
    main()
