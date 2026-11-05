"""
scripts/euler_maruyama_sho.py

Motivation
----------
Figure for the blog post "Euler–Maruyama for a noisy harmonic oscillator".
The goal is to show what additive noise on the velocity does to a harmonic
oscillator and to check the numerical scheme against an exact result. It is
pursued by integrating

    dx = v dt,    dv = -omega^2 x dt + sigma dW

with the semi-implicit Euler–Maruyama scheme (velocity first, then position
with the new velocity), once without noise and once with noise, and by
averaging the energy over many independent sample paths.

What it measures
----------------
* x(t) and v(t) for one sample path at sigma = 0 and at the chosen sigma,
  showing that v is rough while x, its integral, stays smooth.
* The same paths in the phase plane (x, v).
* The mean energy <E(t)> = <v^2/2 + omega^2 x^2/2> over many paths, compared
  with the Itô prediction <E(t)> = E(0) + sigma^2 t / 2.

Usage
-----
    python scripts/euler_maruyama_sho.py
    python scripts/euler_maruyama_sho.py --sigma 0.9 --paths 2000
    python scripts/euler_maruyama_sho.py --out /tmp/em_sho.png --dpi 600
"""

import argparse
from pathlib import Path

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
    / "euler-maruyama-sho.png"
)


def euler_maruyama_sho(x0, v0, omega, sigma, dt, n_steps, n_paths, rng):
    """Integrate many independent paths of the noisy harmonic oscillator.

    Returns arrays x and v of shape (n_steps + 1, n_paths).
    """
    x = np.empty((n_steps + 1, n_paths))
    v = np.empty((n_steps + 1, n_paths))
    x[0], v[0] = x0, v0
    for n in range(n_steps):
        xi = rng.standard_normal(n_paths)  # one N(0, 1) draw per path
        v[n + 1] = v[n] - omega**2 * x[n] * dt + sigma * np.sqrt(dt) * xi
        x[n + 1] = x[n] + v[n + 1] * dt  # semi-implicit: use the new velocity
    return x, v


def energy(x, v, omega):
    """Mechanical energy v^2/2 + omega^2 x^2/2, elementwise."""
    return 0.5 * v**2 + 0.5 * omega**2 * x**2


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--omega", type=float, default=2.0)
    parser.add_argument("--sigma", type=float, default=0.6)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--T", type=float, default=20.0)
    parser.add_argument("--paths", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=5)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--dpi", type=int, default=300)
    return parser.parse_args()


def main():
    args = parse_args()
    n_steps = int(round(args.T / args.dt))
    t = np.arange(n_steps + 1) * args.dt
    x0, v0 = 1.0, 0.0

    # Deterministic reference and the noisy ensemble share the same scheme.
    x_det, v_det = euler_maruyama_sho(
        x0, v0, args.omega, 0.0, args.dt, n_steps, 1, np.random.default_rng(0)
    )
    rng = np.random.default_rng(args.seed)
    x_ens, v_ens = euler_maruyama_sho(
        x0, v0, args.omega, args.sigma, args.dt, n_steps, args.paths, rng
    )
    x_one, v_one = x_ens[:, 0], v_ens[:, 0]

    e0 = energy(x0, v0, args.omega)
    e_mean = energy(x_ens, v_ens, args.omega).mean(axis=1)
    e_theory = e0 + 0.5 * args.sigma**2 * t
    e_det = energy(x_det[:, 0], v_det[:, 0], args.omega)

    mosaic = [["x", "x", "phase"], ["v", "v", "phase"], ["E", "E", "E"]]
    fig, ax = plt.subplot_mosaic(
        mosaic,
        figsize=(10, 7.6),
        height_ratios=[1, 1, 1.15],
        layout="constrained",
    )

    ax["x"].plot(t, x_det[:, 0], color=MUTED, lw=1.0, label=r"$\sigma = 0$")
    ax["x"].plot(t, x_one, color=INK, lw=1.0, label=rf"$\sigma = {args.sigma}$")
    ax["x"].set_ylabel(r"$x$")
    ax["x"].legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), frameon=False, ncols=2)
    ax["x"].tick_params(labelbottom=False)

    ax["v"].plot(t, v_det[:, 0], color=MUTED, lw=1.0)
    ax["v"].plot(t, v_one, color=ACCENT, lw=0.8)
    ax["v"].set_ylabel(r"$v$")
    ax["v"].set_xlabel(r"time $t$")
    ax["v"].sharex(ax["x"])

    ax["phase"].plot(x_det[:, 0], v_det[:, 0], color=MUTED, lw=1.2)
    ax["phase"].plot(x_one, v_one, color=ACCENT, lw=0.5, alpha=0.9)
    ax["phase"].set_xlabel(r"$x$")
    ax["phase"].set_ylabel(r"$v$")
    ax["phase"].set_title("phase plane", loc="left", fontsize=10)

    ax["E"].plot(t, e_det, color=MUTED, lw=1.0, label=r"$\sigma = 0$, one path")
    ax["E"].plot(t, e_mean, color=INK, lw=1.4, label=rf"mean over {args.paths} paths")
    ax["E"].plot(
        t,
        e_theory,
        color=ACCENT,
        lw=1.4,
        ls="--",
        label=r"theory $E(0) + \sigma^2 t / 2$",
    )
    ax["E"].set_xlabel(r"time $t$")
    ax["E"].set_ylabel(r"$\langle E \rangle$")
    ax["E"].legend(loc="upper left", frameon=False)

    for a in ax.values():
        a.spines[["top", "right"]].set_visible(False)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=args.dpi)

    rel_err = np.abs(e_mean[-1] - e_theory[-1]) / e_theory[-1]
    print(f"saved {args.out}")
    print(f"E(0) = {e0:.3f}")
    print(f"<E(T)> simulated = {e_mean[-1]:.3f}, theory = {e_theory[-1]:.3f}")
    print(f"relative error at T = {rel_err:.2%}")
    print(
        f"max |x|: sigma=0 -> {np.abs(x_det).max():.3f}, one noisy path -> "
        f"{np.abs(x_one).max():.3f}"
    )


if __name__ == "__main__":
    main()
