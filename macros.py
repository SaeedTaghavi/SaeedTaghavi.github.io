"""
macros.py

Motivation
----------
Keep the repeating content of the site in plain YAML files under ``data/``
instead of hand-written HTML. Adding a paper, a repository, a talk or a news
item then means adding one entry to one file, and every page that lists it
picks it up on the next build.

What it computes
----------------
At build time, mkdocs-macros calls ``define_env``. It reads every
``data/*.yml`` file and exposes each one as a Jinja variable named after the
file, so ``data/publications.yml`` becomes ``publications`` inside any page.
It also adds two small helpers, ``unique`` and ``slug``, used by the
publication filters.

Usage
-----
    mkdocs serve                  # live preview at http://127.0.0.1:8000
    mkdocs build --strict         # full build into site/, fails on warnings

Inside a Markdown page:

    {% for p in publications %} ... {{ p.title }} ... {% endfor %}
"""

from pathlib import Path
import re

import yaml

DATA_DIR = Path(__file__).parent / "data"


def _slug(text: str) -> str:
    """Lower-case, hyphen-separated version of ``text`` for data attributes."""
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def define_env(env):
    """Register the YAML data files and helper filters with mkdocs-macros."""
    for path in sorted(DATA_DIR.glob("*.yml")):
        with path.open(encoding="utf-8") as handle:
            env.variables[path.stem] = yaml.safe_load(handle) or []

    @env.filter
    def slug(text):
        return _slug(text)

    @env.macro
    def unique(items, key):
        """Distinct values of ``key`` across ``items``, in first-seen order."""
        seen = []
        for item in items:
            value = item.get(key)
            if value and value not in seen:
                seen.append(value)
        return seen
