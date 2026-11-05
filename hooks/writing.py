"""
hooks/writing.py

Motivation
----------
The Blog list, overrides/partials/post.html, shows each post's title and
cover picture. Under Material for MkDocs, an excerpt only learns its title
once the post has been rendered, which can be after the list, and the blog
plugin moves images out of writing/posts/, so the cover path in the front
matter does not point at the published file. This hook resolves both from
the post's own Markdown file and stores them in the post's metadata, where
the template reads them. The template does not depend on this hook: Zensical
ignores MkDocs hooks, and there the template falls back to `post.title` and
to the cover path under writing/.

What it measures
----------------
Nothing. For every page with a `date` in its front matter, which is every
blog post, it sets:
* st_list_title: the `title` in the front matter if there is one, otherwise
  the first "# " heading outside code blocks.
* st_cover_url: the site URL of the file named by `cover:`, a path relative
  to the post, like a Markdown image. A missing file is logged as a warning,
  so `mkdocs build --strict` fails on it.

Usage
-----
Listed under `hooks:` in mkdocs.yml, so MkDocs loads it on every build.
In a theme template:

    {{ post.meta.st_list_title or post.title }}
    {{ post.meta.st_cover_url | url }}
"""

import logging
import posixpath
import re

log = logging.getLogger("mkdocs.hooks.writing")

_FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
_H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$", re.M)


def on_page_markdown(markdown, page, config, files):
    meta = page.meta
    if "date" not in meta:
        return markdown

    if meta.get("title"):
        meta["st_list_title"] = meta["title"]
    else:
        match = _H1.search(_FENCE.sub("", markdown))
        if match:
            meta["st_list_title"] = match.group(1)

    cover = meta.get("cover")
    if cover:
        folder = posixpath.dirname(page.file.src_uri)
        src = posixpath.normpath(posixpath.join(folder, str(cover)))
        file = files.get_file_from_path(src)
        if file is None:
            log.warning("cover '%s' of '%s' not found", cover, page.file.src_uri)
        else:
            meta["st_cover_url"] = file.url
    return markdown
