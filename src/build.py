#!/usr/bin/env python3
"""Minimal blog engine. Converts Markdown posts to static HTML."""

import shutil
from pathlib import Path
from string import Template
from typing import Any, TypedDict

import markdown
import yaml

SRC_DIR: Path = Path(__file__).resolve().parent
POSTS_DIR: Path = Path("posts")
BUILD_DIR: Path = Path("build")
TEMPLATE_FILE: Path = SRC_DIR / "template.html"
STYLE_FILE: Path = SRC_DIR / "style.css"
SITE_TITLE: str = "Olivier's Blog"


class Post(TypedDict):
    title: str
    date: str
    slug: str
    html: str


def parse_post(filepath: Path) -> Post:
    """Read a markdown file with YAML frontmatter, return post dict."""
    raw: str = filepath.read_text(encoding="utf-8")
    parts: list[str] = raw.split("---", 2)
    frontmatter: str = parts[1]
    body: str = parts[2]
    metadata: dict[str, Any] = yaml.safe_load(frontmatter)
    content: str = markdown.markdown(body, extensions=["fenced_code"])
    return {
        "title": metadata["title"],
        "date": str(metadata["date"]),
        "slug": filepath.stem,
        "html": content,
    }


def build_site() -> None:
    """Build the static site."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()

    shutil.copy2(STYLE_FILE, BUILD_DIR / "style.css")

    template: Template = Template(TEMPLATE_FILE.read_text(encoding="utf-8"))

    posts: list[Post] = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda p: p["date"], reverse=True)

    for post in posts:
        post_dir: Path = BUILD_DIR / post["slug"]
        post_dir.mkdir()
        page: str = template.substitute(
            title=post["title"],
            content=(
                f'<article><time>{post["date"]}</time>'
                f'<h2>{post["title"]}</h2>'
                f'{post["html"]}</article>'
            ),
            root="..",
        )
        (post_dir / "index.html").write_text(page, encoding="utf-8")

    items: list[str] = []
    for post in posts:
        items.append(
            f'<article><time>{post["date"]}</time> '
            f'<a href="{post["slug"]}/">{post["title"]}</a></article>'
        )
    index_content: str = "\n".join(items)
    index_page: str = template.substitute(
        title=SITE_TITLE,
        content=index_content,
        root=".",
    )
    (BUILD_DIR / "index.html").write_text(index_page, encoding="utf-8")

    print(f"Built {len(posts)} posts -> {BUILD_DIR}/")


if __name__ == "__main__":
    build_site()
