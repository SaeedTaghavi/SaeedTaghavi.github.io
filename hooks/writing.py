"""
hooks/writing.py

Motivation
----------
The Writing list, overrides/partials/post.html, shows each post's title and
cover picture. Material's excerpts only learn the title once the post has
been rendered, which can be after the list, and the blog plugin moves images
out of writing/posts/, so a fixed path to a cover breaks. This hook gives the
theme two Jinja filters that resolve both from the post's own Markdown file.

What it measures
----------------
Nothing. It registers two filters:
* post_title: the `title` in the front matter if there is one, otherwise the
  first "# " heading outside code blocks, otherwise MkDocs' own page title.
* post_cover: the site URL of the file named by `cover:` in the front matter,
  a path relative to the post, like a Markdown image. A missing file is
  logged as a warning, so `mkdocs build --strict` fails on it.

Usage
-----
Listed under `hooks:` in mkdocs.yml, so MkDocs loads it on every build.
In a theme template:

    {{ post | post_title }}
    {{ post | post_cover | url }}
"""

import logging
import posixpath
import re

log = logging.getLogger("mkdocs.hooks.writing")

_FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
_H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)
_files = None


def on_env(env, config, files):
    global _files
    _files = files
    env.filters["post_title"] = post_title
    env.filters["post_cover"] = post_cover
    return env


def post_title(post):
    """Title of a post or of its excerpt."""
    source = getattr(post, "post", post)
    if source.meta.get("title"):
        return source.meta["title"]
    match = _H1.search(_FENCE.sub("", source.markdown or ""))
    return match.group(1) if match else source.title


def post_cover(post):
    """Site URL of the post's cover picture, or an empty string."""
    cover = post.meta.get("cover")
    if not cover or _files is None:
        return ""
    folder = posixpath.dirname(post.file.src_uri)
    src = posixpath.normpath(posixpath.join(folder, cover))
    file = _files.get_file_from_path(src)
    if file is None:
        log.warning("cover '%s' of '%s' not found", cover, post.file.src_uri)
        return ""
    return file.url
