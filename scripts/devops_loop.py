"""
scripts/devops_loop.py

Motivation
----------
The DevOps loop appears twice on the site: as the Engineering tile on the
home page and, larger and annotated, in the post "DevOps notes, part 1". The
goal is one drawing of the loop that both share, so the two never drift
apart. It is pursued by computing the loop once, as a figure eight, and
writing it out as two inline SVG files that take their colours from the
site's CSS variables and so follow the light and dark themes.

What it measures
----------------
Nothing. It draws the eight phases of the loop on a Gerono lemniscate,

    x = A sin t,   y = B sin t cos t,

travelled with t decreasing: plan, code, build and test on the left lobe
(development, blue), release, deploy, operate and monitor on the right lobe
(operations, vermilion), and back to plan through the crossing. The post
version adds a dashed ring for continuous testing and two arrows for shift
left and shift right.

Usage
-----
    python scripts/devops_loop.py
    python scripts/devops_loop.py --only tile
"""

import argparse
import math
from pathlib import Path

INCLUDES = Path(__file__).resolve().parents[1] / "includes"
MONO = "font-family: 'IBM Plex Mono', monospace"
ARIA = (
    "The DevOps loop as an infinity sign: plan, code, build and test on the "
    "development side, release, deploy, operate and monitor on the operations "
    "side, and back to plan"
)
# Phase, position on the curve as a fraction of pi, lobe colour, above or below.
PHASES = [
    ("plan", 1.9, "c2", "top"),
    ("code", 1.62, "c2", "top"),
    ("build", 1.38, "c2", "bottom"),
    ("test", 1.1, "c2", "bottom"),
    ("release", 0.9, "c1", "top"),
    ("deploy", 0.62, "c1", "top"),
    ("operate", 0.38, "c1", "bottom"),
    ("monitor", 0.1, "c1", "bottom"),
]

# Sizes for the small home tile and the larger diagram in the post.
TILE = dict(
    A=78, B=88, cx=100, cy=94, line=2.6, dot=4, dot_line=2, chev=4.5,
    label=9.5, label_gap=(8, 15), lobe=9, lobe_dx=48,
)
POST = dict(
    A=130, B=130, cx=260, cy=140, line=3.4, dot=5.5, dot_line=2.4, chev=6,
    label=13, label_gap=(11, 21), lobe=11, lobe_dx=80,
)


def loop_elements(g):
    """SVG elements of the loop itself: the two lobes, arrows, dots, labels."""
    A, B, cx, cy = g["A"], g["B"], g["cx"], g["cy"]

    def pt(t):
        return cx + A * math.sin(t), cy + B * math.sin(t) * math.cos(t)

    def path(t0, t1, n=120):
        pts = [pt(t0 + (t1 - t0) * k / n) for k in range(n + 1)]
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    def chevron(t, colour):
        # Points down: at both outer ends the loop runs from top to bottom.
        x, y = pt(t)
        c = g["chev"]
        return (
            f'<path d="M{x - c:.1f} {y - 2 * c / 3:.1f} L {x:.1f} {y + 4 * c / 9:.1f} '
            f'L {x + c:.1f} {y - 2 * c / 3:.1f}" style="stroke: var(--st-{colour})"></path>'
        )

    top = cy - 0.5 * B - g["label_gap"][0]
    bottom = cy + 0.5 * B + g["label_gap"][1]
    dots, labels = [], []
    for name, frac, colour, side in PHASES:
        x, y = pt(frac * math.pi)
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{g["dot"]}" style="fill: var(--st-card); '
            f'stroke: var(--st-{colour})" stroke-width="{g["dot_line"]}"></circle>'
        )
        ly = top if side == "top" else bottom
        labels.append(f'<text x="{x:.1f}" y="{ly:.1f}" style="fill: var(--st-{colour})">{name}</text>')

    pi = math.pi
    return [
        f'<g fill="none" stroke-width="{g["line"]}" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="{path(2 * pi, pi)}" style="stroke: var(--st-c2)"></path>'
        f'<path d="{path(pi, 0)}" style="stroke: var(--st-c1)"></path></g>',
        f'<g fill="none" stroke-width="{g["dot_line"]}" stroke-linecap="round" stroke-linejoin="round">'
        f'{chevron(1.5 * pi, "c2")}{chevron(0.5 * pi, "c1")}</g>',
        "".join(dots),
        f'<g style="fill: var(--st-muted); {MONO}; font-size: {g["lobe"]}px; letter-spacing: 0.14em" '
        f'text-anchor="middle"><text x="{cx - g["lobe_dx"]}" y="{cy + 3}">DEV</text>'
        f'<text x="{cx + g["lobe_dx"]}" y="{cy + 3}">OPS</text></g>',
        f'<g style="{MONO}; font-size: {g["label"]}px" text-anchor="middle">{"".join(labels)}</g>',
    ]


def tile_svg():
    head = f'<svg viewBox="0 0 200 178" role="img" aria-label="{ARIA}" class="st-svg">'
    return "\n".join([head, *loop_elements(TILE), "</svg>"]) + "\n"


def post_svg():
    g = POST
    cx = g["cx"]
    ring = (
        f'<ellipse cx="{cx}" cy="{g["cy"]}" rx="256" ry="126" fill="none" '
        'style="stroke: var(--st-muted)" stroke-width="1.2" stroke-dasharray="5 5"></ellipse>'
    )
    # The label sits on the ring; a stroke in the page colour clears the dashes behind it.
    ring_label = (
        f'<text x="{cx}" y="{g["cy"] - 122}" text-anchor="middle" style="fill: var(--st-muted); '
        f'stroke: var(--st-bg); stroke-width: 6px; paint-order: stroke; {MONO}; font-size: 10px; '
        'letter-spacing: 0.14em">CONTINUOUS TESTING</text>'
    )
    y = 296
    shifts = (
        '<g fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M{cx - 14} {y} H 20 M 28 {y - 6} L 20 {y} L 28 {y + 6}" style="stroke: var(--st-c2)"></path>'
        f'<path d="M{cx + 14} {y} H 500 M 492 {y - 6} L 500 {y} L 492 {y + 6}" style="stroke: var(--st-c1)"></path></g>'
        f'<g style="{MONO}; font-size: 12px"><text x="22" y="{y - 10}" style="fill: var(--st-c2)">'
        "shift left: test earlier</text>"
        f'<text x="498" y="{y - 10}" text-anchor="end" style="fill: var(--st-c1)">'
        "shift right: learn in production</text></g>"
    )
    aria = ARIA + ", inside a ring of continuous testing, with shift left and shift right below"
    head = f'<svg viewBox="0 0 520 306" role="img" aria-label="{aria}" class="st-svg st-figure-svg">'
    return "\n".join([head, ring, ring_label, *loop_elements(g), shifts, "</svg>"]) + "\n"


OUTPUTS = {
    "tile": ("tile-engineering.svg", tile_svg),
    "post": ("devops-loop.svg", post_svg),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", choices=sorted(OUTPUTS), default=None)
    parser.add_argument("--out-dir", type=Path, default=INCLUDES)
    args = parser.parse_args()
    for key, (name, draw) in OUTPUTS.items():
        if args.only and key != args.only:
            continue
        out = args.out_dir / name
        out.write_text(draw(), encoding="utf-8", newline="\n")
        print(f"saved {out}")


if __name__ == "__main__":
    main()
