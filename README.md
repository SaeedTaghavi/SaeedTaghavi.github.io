# saeedtaghavi.github.io

Personal site built with [Zensical](https://zensical.org/), the successor of
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/): site
search, a **Blog**, and data files for everything that repeats. Zensical reads
`mkdocs.yml`, and the project still builds with Material for MkDocs as a fallback.

## Preview locally

```bash
python3 -m venv .venv            # once: a private Python for this project
source .venv/bin/activate        # every new terminal; `deactivate` leaves it
pip install -r requirements.txt
zensical serve                   # http://localhost:8000, reloads on save
zensical build --strict          # the same check the deploy runs
```

## Where things live

| To change | Edit |
| --- | --- |
| A paper, thesis or abstract | `data/publications.yml` |
| A repository, course or product | `data/software.yml` (`home: true` also shows it on the home page) |
| A talk or video | `data/talks.yml` (only the YouTube id is needed; `cover` is optional) |
| The "Latest" list on the home page | `data/news.yml` |
| Home page text, research themes, CV | `docs/index.md`, `docs/research.md`, `docs/cv.md` |
| Colours, fonts, spacing | `docs/assets/stylesheets/site.css` (tokens at the top) |
| Drawings used in pages | `includes/*.svg` (they follow the light and dark colours) |
| Menu, social links, plugins | `mkdocs.yml` |

Square brackets in the content, such as `[Thesis title]`, mark facts still to fill in.

## Tags

A page or post can carry `tags:` in its front matter. The search box lists
every tag under **Filters**, and picking one narrows the results to the pages
with that tag. A tag applies to the whole page, so each of its sections shows
up under the filter too. Keep to these names so the list stays short:

Spiking networks, Phase oscillators, Synchrony, Plasticity, Brain stimulation, Stochastic dynamics, EEG, Machine learning, Information theory, Numerical methods, Astrophysics, Python, NEST, PyTorch, Docker, Kubernetes, Teaching.

Home, the CV and the Blog index carry no tags, because they cover everything.

## Write a blog post

Create `docs/writing/posts/<name>.md`:

```markdown
---
date:
  created: 2026-11-05
categories:
  - Numerical methods
tags:
  - Python
slug: short-url-name
description: One sentence, shown under the title on the Blog page.
cover: img/<name>-cover.png
---

# Title

First paragraph, the opening of the post.

<!-- more -->

The rest of the post. Inline maths $x^2$, display maths $$...$$.
```

The Blog page lists each post with its date, reading time, title, topics,
`description` and `cover`, a 4:3 picture in `docs/writing/posts/img/` shown on
the right. A post without
`cover` takes the full width.

Keep the scripts that draw a post's figures and covers in `scripts/`. They
need a few extra packages that the site build does not:

```bash
pip install -r scripts/requirements.txt
python scripts/euler_maruyama_sho.py
python scripts/infomeasure_checks.py
python scripts/post_covers.py           # thumbnails for the Blog page
```

## Deploy to GitHub Pages

1. The site lives in `SaeedTaghavi/saeedtaghavi.github.io`, on the branch `master`. The earlier Jekyll site is kept on the branch `jekyll-site`.
2. In the repository, **Settings → Pages → Source** is set to **GitHub Actions**.
3. Every push to `master` runs `zensical build --strict` and publishes to <https://saeedtaghavi.github.io/>. The workflow also accepts `main`, in case the branch is renamed.

Zensical has no `gh-deploy` command, so the site is published only through this workflow.

## A note on versions

The site is built with Zensical, pinned to `0.1.0` in `requirements.txt`
because it is still young. Raise the pin deliberately and check the result with
`zensical serve`. `theme.variant: modern` in `mkdocs.yml` selects Zensical's
modern look.

The project also still builds with Material for MkDocs, which is in
maintenance mode:

```bash
pip install -r requirements-mkdocs.txt
mkdocs build --strict
```

Only that fallback uses `hooks/writing.py`, which works out the title and cover
of each post for the Blog list under MkDocs. Zensical ignores MkDocs hooks, and
`overrides/partials/post.html` falls back to what Zensical provides itself.
