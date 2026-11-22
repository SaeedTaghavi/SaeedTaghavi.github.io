"""
scripts/palette_check.py

Motivation
----------
The figures on this site share one palette (see CLAUDE.md). The goal is to
check, with numbers instead of by eye, that its colours stay apart for
colour-blind readers and in greyscale, and that thin lines and small markers
stand out from the page. It is pursued by converting each colour to CIELAB,
simulating the three kinds of dichromacy, and measuring distances and
contrast.

What it measures
----------------
For the light and the dark theme separately:
* L*: CIELAB lightness, 0 to 100, which is what remains in greyscale.
* Contrast ratio against the page background (WCAG 2). Lines and markers
  need at least 3:1, text at least 4.5:1.
* Delta E (CIE 1976) between every pair of plot colours, for normal vision
  and for simulated protanopia, deuteranopia and tritanopia (Machado,
  Oliveira and Fernandes 2009, severity 1). Below about 20, small marks are
  hard to tell apart; above about 40 they are clearly different.

Usage
-----
    python scripts/palette_check.py
    python scripts/palette_check.py --light "#d8452a,#1f5f99,#f2c14e"
"""

import argparse
import itertools

import numpy as np

# Plot colours in the order c1 (vermilion), c2 (blue), c3 (amber), as in
# docs/assets/stylesheets/site.css, with the background figures sit on.
THEMES = {
    "light": {"colours": "#cf3e24,#1a5188,#efb93a", "background": "#ffffff"},
    "dark": {"colours": "#f26a3d,#6cb6f0,#ffd770", "background": "#10212d"},
}
NAMES = ("vermilion", "blue", "amber")
SIMULATIONS = {
    "normal": np.eye(3),
    "protan": np.array(
        [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]
    ),
    "deutan": np.array(
        [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]
    ),
    "tritan": np.array(
        [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]
    ),
}


def linear_rgb(hex_colour):
    """sRGB hex string to linear RGB in [0, 1]."""
    c = np.array([int(hex_colour[i : i + 2], 16) for i in (1, 3, 5)]) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lab(rgb_linear):
    """Linear RGB to CIELAB under D65."""
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    x, y, z = m @ rgb_linear / np.array([0.95047, 1.0, 1.08883])

    def f(t):
        return np.where(t > 0.008856, np.cbrt(t), 7.787 * t + 16 / 116)

    return np.array([116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))])


def contrast(a, b):
    """WCAG 2 contrast ratio between two hex colours."""
    ya, yb = (float(np.dot([0.2126, 0.7152, 0.0722], linear_rgb(c))) for c in (a, b))
    hi, lo = max(ya, yb), min(ya, yb)
    return (hi + 0.05) / (lo + 0.05)


def check(theme, colours, background):
    print(f"== {theme} theme, background {background}")
    for name, c in zip(NAMES, colours):
        L = lab(linear_rgb(c))[0]
        print(f"   {name:9s} {c}  L* {L:4.0f}  contrast {contrast(c, background):4.1f}:1")
    for sim, matrix in SIMULATIONS.items():
        points = [lab(np.clip(matrix @ linear_rgb(c), 0, 1)) for c in colours]
        pairs = [
            f"{NAMES[i][:4]}-{NAMES[j][:4]} {np.linalg.norm(points[i] - points[j]):3.0f}"
            for i, j in itertools.combinations(range(len(colours)), 2)
        ]
        print(f"   {sim:7s} delta E: " + "   ".join(pairs))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    for theme, spec in THEMES.items():
        parser.add_argument(f"--{theme}", default=spec["colours"], help="three comma-separated hex colours")
    args = parser.parse_args()
    for theme, spec in THEMES.items():
        check(theme, getattr(args, theme).split(","), spec["background"])


if __name__ == "__main__":
    main()
