#!/usr/bin/env python3
"""Minimal blog engine. Converts Markdown posts to static HTML."""

import shutil
from collections.abc import Callable
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
LANGUAGES: list[str] = ["en", "fr", "nl"]


class Post(TypedDict):
    title: str
    date: str
    slug: str
    lang: str
    html: str


def split_stem(stem: str) -> tuple[str, str]:
    """Extract slug and lang from a filename stem like 'hello-world.en'."""
    dot_index: int = stem.rfind(".")
    if dot_index == -1:
        raise ValueError(f"No language suffix in stem: {stem!r}")
    slug: str = stem[:dot_index]
    lang: str = stem[dot_index + 1 :]
    if lang not in LANGUAGES:
        raise ValueError(f"Unknown language {lang!r} in stem: {stem!r}")
    return slug, lang


def parse_post(filepath: Path) -> Post:
    """Read a markdown file with YAML frontmatter, return post dict."""
    raw: str = filepath.read_text(encoding="utf-8")
    parts: list[str] = raw.split("---", 2)
    frontmatter: str = parts[1]
    body: str = parts[2]
    metadata: dict[str, Any] = yaml.safe_load(frontmatter)
    content: str = markdown.markdown(body, extensions=["fenced_code"])
    slug: str
    lang: str
    slug, lang = split_stem(filepath.stem)
    return {
        "title": metadata["title"],
        "date": str(metadata["date"]),
        "slug": slug,
        "lang": lang,
        "html": content,
    }


def group_translations(posts: list[Post]) -> dict[str, dict[str, Post]]:
    """Group posts by slug, then by lang. Returns {slug: {lang: Post}}."""
    groups: dict[str, dict[str, Post]] = {}
    for post in posts:
        slug: str = post["slug"]
        if slug not in groups:
            groups[slug] = {}
        groups[slug][post["lang"]] = post
    return groups


def render_lang_switcher(
    current_lang: str,
    available_langs: list[str],
    path_builder: Callable[[str], str],
) -> str:
    """Generate a language switcher nav element."""
    items: list[str] = []
    for lang in available_langs:
        if lang == current_lang:
            items.append(f"<span>{lang}</span>")
        else:
            items.append(f'<a href="{path_builder(lang)}">{lang}</a>')
    return '<nav class="lang-switcher">' + " | ".join(items) + "</nav>"


def prepare_build_dir() -> None:
    """Clean and recreate the build directory, copy static assets."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()
    shutil.copy2(STYLE_FILE, BUILD_DIR / "style.css")


def load_posts() -> list[Post]:
    """Glob, parse, and sort all posts by date descending."""
    posts: list[Post] = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def build_post_pages(
    lang: str,
    lang_dir: Path,
    lang_posts: list[Post],
    translations: dict[str, dict[str, Post]],
    template: Template,
) -> None:
    """Write individual post pages for a given language."""
    available_langs: list[str] = LANGUAGES
    for post in lang_posts:
        slug: str = post["slug"]
        post_dir: Path = lang_dir / slug
        post_dir.mkdir(parents=True)
        switcher: str = render_lang_switcher(
            lang,
            available_langs,
            lambda other_lang, s=slug: f"../../{other_lang}/{s}/",
        )
        page: str = template.substitute(
            title=post["title"],
            lang=lang,
            lang_switcher=switcher,
            content=(
                f'<article><time>{post["date"]}</time>'
                f'<h2>{post["title"]}</h2>'
                f'{post["html"]}</article>'
            ),
            root="../..",
        )
        (post_dir / "index.html").write_text(page, encoding="utf-8")


def build_index_page(
    lang: str,
    lang_dir: Path,
    lang_posts: list[Post],
    template: Template,
) -> None:
    """Write the index page for a given language."""
    available_langs: list[str] = LANGUAGES
    switcher: str = render_lang_switcher(
        lang,
        available_langs,
        lambda other_lang: f"../{other_lang}/",
    )
    items: list[str] = []
    for post in lang_posts:
        items.append(
            f'<article><time>{post["date"]}</time> '
            f'<a href="{post["slug"]}/">{post["title"]}</a></article>'
        )
    index_content: str = "\n".join(items)
    page: str = template.substitute(
        title=SITE_TITLE,
        lang=lang,
        lang_switcher=switcher,
        content=index_content,
        root="..",
    )
    (lang_dir / "index.html").write_text(page, encoding="utf-8")


def build_lang(
    lang: str,
    posts: list[Post],
    translations: dict[str, dict[str, Post]],
    template: Template,
) -> None:
    """Build all pages for a given language."""
    lang_dir: Path = BUILD_DIR / lang
    lang_dir.mkdir(parents=True, exist_ok=True)
    lang_posts: list[Post] = [p for p in posts if p["lang"] == lang]
    build_post_pages(lang, lang_dir, lang_posts, translations, template)
    build_index_page(lang, lang_dir, lang_posts, template)


def build_root_redirect() -> None:
    """Write a root index.html that redirects to /en/."""
    html: str = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta http-equiv="refresh" content="0;url=en/">\n'
        "</head>\n<body></body>\n</html>"
    )
    (BUILD_DIR / "index.html").write_text(html, encoding="utf-8")


def build_site() -> None:
    """Build the static site."""
    prepare_build_dir()
    template: Template = Template(TEMPLATE_FILE.read_text(encoding="utf-8"))
    posts: list[Post] = load_posts()
    translations: dict[str, dict[str, Post]] = group_translations(posts)

    for lang in LANGUAGES:
        build_lang(lang, posts, translations, template)

    build_root_redirect()

    print(f"Built {len(posts)} posts -> {BUILD_DIR}/")


if __name__ == "__main__":
    build_site()
