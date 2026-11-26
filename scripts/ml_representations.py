"""
scripts/ml_representations.py

Motivation
----------
Figure for the blog post "Machine learning notes, part 1: what learning
means". The goal is to show that the representation of a model, the language
it is written in, decides which boundaries it can draw at all. It is pursued
by fitting four models from four families of representation to the same
two-class data set and drawing the regions each one assigns to each class.

What it measures
----------------
On scikit-learn's two-moons data (two interleaving half circles with Gaussian
noise), split into training and test points:
* a linear function (logistic regression),
* a symbolic one (a decision tree of limited depth),
* an instance-based one (k nearest neighbours),
* a probabilistic graphical model (Gaussian naive Bayes).
Each panel shows the predicted class regions, the boundary where both classes
are equally likely, the training points, and the accuracy on the test points.

Usage
-----
    pip install -r scripts/requirements.txt
    python scripts/ml_representations.py
    python scripts/ml_representations.py --noise 0.35 --seed 3
    python scripts/ml_representations.py --out /tmp/rep.png --dpi 600
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

INK = "#13212b"
MUTED = "#a3b1ba"
ACCENT = "#cf3e24"
# Same roles as the site figures: blue and vermilion for the two classes,
# with pale tints of the same colours for the regions a model assigns.
BLUE = "#1a5188"
BLUE_TINT = "#dde5ed"
ACCENT_TINT = "#f8e2de"
DEFAULT_OUT = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "blog"
    / "posts"
    / "img"
    / "ml-representations.png"
)

MODELS = [
    ("Linear function", "logistic regression", LogisticRegression()),
    ("Decision tree", "depth 4", DecisionTreeClassifier(max_depth=4, random_state=0)),
    ("Instance-based", "15 nearest neighbours", KNeighborsClassifier(n_neighbors=15)),
    ("Probabilistic model", "Gaussian naive Bayes", GaussianNB()),
]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--n", type=int, default=400)
    parser.add_argument("--noise", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--dpi", type=int, default=300)
    return parser.parse_args()


def main():
    args = parse_args()
    X, y = make_moons(n_samples=args.n, noise=args.noise, random_state=args.seed)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=args.seed
    )

    pad = 0.5
    gx, gy = np.meshgrid(
        np.linspace(X[:, 0].min() - pad, X[:, 0].max() + pad, 400),
        np.linspace(X[:, 1].min() - pad, X[:, 1].max() + pad, 300),
    )
    grid = np.column_stack([gx.ravel(), gy.ravel()])

    fig, axes = plt.subplots(2, 2, figsize=(9, 7.2), layout="constrained")
    for ax, (family, model_name, model) in zip(axes.ravel(), MODELS):
        model.fit(X_train, y_train)
        p = model.predict_proba(grid)[:, 1].reshape(gx.shape)
        accuracy = model.score(X_test, y_test)

        ax.contourf(gx, gy, p, levels=[0, 0.5, 1], colors=[BLUE_TINT, ACCENT_TINT])
        ax.contour(gx, gy, p, levels=[0.5], colors=INK, linewidths=1.2)
        for label, color in ((0, BLUE), (1, ACCENT)):
            pts = X_train[y_train == label]
            ax.scatter(pts[:, 0], pts[:, 1], s=9, color=color, linewidths=0)

        ax.set_title(
            f"{family}\n{model_name}, test accuracy {accuracy:.2f}",
            loc="left",
            fontsize=10,
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for side in ax.spines.values():
            side.set_color(MUTED)
        print(f"{family:20s} {model_name:24s} test accuracy {accuracy:.3f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=args.dpi)
    print(f"saved {args.out}")


if __name__ == "__main__":
    main()
