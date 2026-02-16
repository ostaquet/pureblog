#!/usr/bin/env python3
"""Minimal blog engine. Converts Markdown posts to static HTML."""

import shutil
from pathlib import Path
from string import Template

import markdown
import yaml

SRC_DIR = Path(__file__).resolve().parent
POSTS_DIR = Path("posts")
BUILD_DIR = Path("build")
TEMPLATE_FILE = SRC_DIR / "template.html"
STYLE_FILE = SRC_DIR / "style.css"
SITE_TITLE = "Olivier's Blog"


def parse_post(filepath):
    """Read a markdown file with YAML frontmatter, return post dict."""
    raw = filepath.read_text(encoding="utf-8")
    _, fm_text, body = raw.split("---", 2)
    meta = yaml.safe_load(fm_text)
    html = markdown.markdown(body, extensions=["fenced_code"])
    return {
        "title": meta["title"],
        "date": str(meta["date"]),
        "slug": filepath.stem,
        "html": html,
    }


def build():
    """Build the static site."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()

    shutil.copy2(STYLE_FILE, BUILD_DIR / "style.css")

    template = Template(TEMPLATE_FILE.read_text(encoding="utf-8"))

    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda p: p["date"], reverse=True)

    for post in posts:
        post_dir = BUILD_DIR / post["slug"]
        post_dir.mkdir()
        html = template.substitute(
            title=post["title"],
            content=(
                f'<article><time>{post["date"]}</time>'
                f'<h2>{post["title"]}</h2>'
                f'{post["html"]}</article>'
            ),
            root="..",
        )
        (post_dir / "index.html").write_text(html, encoding="utf-8")

    items = []
    for post in posts:
        items.append(
            f'<article><time>{post["date"]}</time> '
            f'<a href="{post["slug"]}/">{post["title"]}</a></article>'
        )
    index_content = "\n".join(items)
    html = template.substitute(
        title=SITE_TITLE,
        content=index_content,
        root=".",
    )
    (BUILD_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"Built {len(posts)} posts -> {BUILD_DIR}/")


if __name__ == "__main__":
    build()
