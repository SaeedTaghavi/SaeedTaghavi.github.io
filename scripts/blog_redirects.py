"""
scripts/blog_redirects.py

Motivation
----------
The blog moved from /writing/ to /blog/ in November 2026. GitHub Pages has no
server-side redirects, so every address that existed under /writing/ gets a
small static page in docs/writing/ that sends the visitor to the same page
under /blog/. Links already shared (LinkedIn, the ai-projects READMEs, search
results) keep working.

What it does
------------
Writes docs/writing/<path>/index.html for each path in OLD_PATHS. Each page has
a canonical link to the new address, a meta refresh, and a script that keeps
any #fragment. They are marked noindex, so search engines index /blog/ only.

Usage
-----
    python scripts/blog_redirects.py

Run it again only if OLD_PATHS changes. Posts published after the move live
under /blog/ from the start and need no entry here.
"""

from pathlib import Path

# Every page that was published under /writing/ before the move
# (taken from the live sitemap on 26 Nov 2026).
OLD_PATHS = [
    "",
    "devops-notes-01-loop-and-testing/",
    "euler-maruyama-noisy-harmonic-oscillator/",
    "infomeasure-information-theory-in-python/",
    "lenet-web-app/",
    "llm-fine-tuning-ticket-routing/",
    "local-llm-stack/",
    "local-llms-metabase-mcp/",
    "machine-learning-notes-01-introduction/",
    "category/ai/",
    "category/deep-learning/",
    "category/engineering/",
    "category/fine-tuning/",
    "category/information-theory/",
    "category/llm/",
    "category/machine-learning/",
    "category/numerical-methods/",
    "category/stochastic-dynamics/",
    "category/tools/",
]

SITE = "https://saeedtaghavi.xyz"
OUT = Path(__file__).resolve().parents[1] / "docs" / "writing"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {new}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{absolute}">
<meta http-equiv="refresh" content="0; url={new}">
<script>location.replace("{new}" + location.hash)</script>
</head>
<body>
<p>This page has moved to <a href="{new}">{new}</a>.</p>
</body>
</html>
"""


def main():
    for path in OLD_PATHS:
        new = f"/blog/{path}"
        target = OUT / path / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(PAGE.format(new=new, absolute=SITE + new), encoding="utf-8")
        print(f"/writing/{path} -> {new}")


if __name__ == "__main__":
    main()
