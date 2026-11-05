# saeedtaghavi.github.io

Personal site built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/): site
search, a **Blog**, and data files for everything that repeats.

## Preview locally

```bash
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000, reloads on save
mkdocs build --strict   # the same check the deploy runs
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

## Write a blog post

Create `docs/writing/posts/<name>.md`:

```markdown
---
date:
  created: 2026-11-05
categories:
  - Numerical methods
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
3. Every push to `master` builds with `--strict` and publishes to <https://saeedtaghavi.github.io/>. The workflow also accepts `main`, in case the branch is renamed.

`mkdocs gh-deploy --force` also works, as for computational-neuroscience.ir. In that case set the Pages source to the `gh-pages` branch instead.

## A note on versions

Material for MkDocs is in maintenance mode, and MkDocs 2.0 will not run its
plugins or theme overrides, so `requirements.txt` pins `mkdocs<2`. The same
team now develops [Zensical](https://zensical.org/), which reads this
`mkdocs.yml` and already supports the blog, search and macros plugins used
here. Check its compatibility notes for theme overrides before switching.
