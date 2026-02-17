#!/usr/bin/env python3
"""Minimal blog engine. Converts Markdown posts to static HTML."""

import html
import math
import re
import shutil
from collections.abc import Callable
from datetime import datetime
from zoneinfo import ZoneInfo
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
SITE_URL: str = "https://example.com"
LANGUAGES: list[str] = ["en", "fr", "nl"]
DEFAULT_TIMEZONE: ZoneInfo = ZoneInfo("Europe/Brussels")
DEFAULT_PUBLISH_HOUR: int = 13
READING_TIME_LABELS: dict[str, str] = {
    "en": "min read",
    "fr": "min de lecture",
    "nl": "min leestijd",
}


class Post(TypedDict):
    title: str
    date: str
    excerpt: str
    reading_time: int
    post_id: str
    slug: str
    lang: str
    html: str


def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes from raw markdown text."""
    word_count: int = len(text.split())
    return max(1, math.ceil(word_count / 200))


def format_reading_time(minutes: int, lang: str) -> str:
    """Return localized reading time string, e.g. '2 min read'."""
    label: str = READING_TIME_LABELS[lang]
    return f"{minutes} {label}"


def split_stem(stem: str) -> tuple[str, str, str]:
    """Extract post_id, slug, and lang from a stem like '001-hello-world.en'.

    Returns (post_id, slug, lang).
    """
    dot_index: int = stem.rfind(".")
    if dot_index == -1:
        raise ValueError(f"No language suffix in stem: {stem!r}")
    prefix_slug: str = stem[:dot_index]
    lang: str = stem[dot_index + 1 :]
    if lang not in LANGUAGES:
        raise ValueError(f"Unknown language {lang!r} in stem: {stem!r}")
    dash_index: int = prefix_slug.find("-")
    if dash_index == -1:
        raise ValueError(f"No prefix-slug separator in stem: {stem!r}")
    post_id: str = prefix_slug[:dash_index]
    slug: str = prefix_slug[dash_index + 1 :]
    if not post_id.isdigit():
        raise ValueError(f"Non-numeric prefix {post_id!r} in stem: {stem!r}")
    if not slug:
        raise ValueError(f"Empty slug in stem: {stem!r}")
    return post_id, slug, lang


def parse_post(filepath: Path) -> Post:
    """Read a markdown file with YAML frontmatter, return post dict."""
    raw: str = filepath.read_text(encoding="utf-8")
    parts: list[str] = raw.split("---", 2)
    frontmatter: str = parts[1]
    body: str = parts[2]
    metadata: dict[str, Any] = yaml.safe_load(frontmatter)
    content: str = markdown.markdown(body, extensions=["fenced_code"])
    post_id: str
    slug: str
    lang: str
    post_id, slug, lang = split_stem(filepath.stem)
    return {
        "title": metadata["title"],
        "date": str(metadata["date"]),
        "excerpt": metadata.get("excerpt", ""),
        "reading_time": estimate_reading_time(body),
        "post_id": post_id,
        "slug": slug,
        "lang": lang,
        "html": content,
    }


def group_translations(posts: list[Post]) -> dict[str, dict[str, Post]]:
    """Group posts by post_id, then by lang. Returns {post_id: {lang: Post}}."""
    groups: dict[str, dict[str, Post]] = {}
    for post in posts:
        post_id: str = post["post_id"]
        if post_id not in groups:
            groups[post_id] = {}
        groups[post_id][post["lang"]] = post
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


def format_rfc822_date(iso_date: str) -> str:
    """Convert an ISO date string (YYYY-MM-DD) to RFC 822 format for RSS.

    Uses Europe/Brussels timezone and 13:00 as the default publish time.
    """
    dt: datetime = datetime.strptime(iso_date, "%Y-%m-%d").replace(
        hour=DEFAULT_PUBLISH_HOUR, tzinfo=DEFAULT_TIMEZONE
    )
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def build_post_description(post: Post) -> str:
    """Return the post description: excerpt or truncated plain text."""
    if post["excerpt"]:
        return post["excerpt"]
    plain: str = re.sub(r"<[^>]+>", "", post["html"])
    if len(plain) <= 200:
        return plain
    return plain[:200] + "..."


def render_rss_item(post: Post, lang: str) -> str:
    """Render a single RSS <item> element for a post."""
    url: str = f"{SITE_URL}/{lang}/{post['slug']}/"
    title_escaped: str = html.escape(post["title"])
    description: str = html.escape(build_post_description(post))
    pub_date: str = format_rfc822_date(post["date"])
    return (
        "<item>"
        f"<title>{title_escaped}</title>"
        f"<link>{url}</link>"
        f"<description>{description}</description>"
        f"<pubDate>{pub_date}</pubDate>"
        f"<guid>{url}</guid>"
        "</item>"
    )


def build_feed(lang: str, lang_dir: Path, lang_posts: list[Post]) -> None:
    """Build an RSS 2.0 feed.xml for a given language."""
    feed_url: str = f"{SITE_URL}/{lang}/feed.xml"
    lang_url: str = f"{SITE_URL}/{lang}/"
    items: str = "\n".join(render_rss_item(post, lang) for post in lang_posts)
    feed: str = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "<channel>\n"
        f"<title>{html.escape(SITE_TITLE)}</title>\n"
        f"<link>{lang_url}</link>\n"
        f"<description>{html.escape(SITE_TITLE)}</description>\n"
        f"<language>{lang}</language>\n"
        f'<atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>\n'
        f"{items}\n"
        "</channel>\n"
        "</rss>"
    )
    (lang_dir / "feed.xml").write_text(feed, encoding="utf-8")


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
        post_id: str = post["post_id"]
        post_dir: Path = lang_dir / slug
        post_dir.mkdir(parents=True)
        sibling_posts: dict[str, Post] = translations.get(post_id, {})
        switcher: str = render_lang_switcher(
            lang,
            available_langs,
            lambda other_lang, sp=sibling_posts, s=slug: (
                f"../../{other_lang}/{sp[other_lang]['slug']}/"
                if other_lang in sp
                else f"../../{other_lang}/{s}/"
            ),
        )
        back_label: str = "\u2190 Back"
        reading_time_str: str = format_reading_time(
            post["reading_time"], lang
        )
        page: str = template.substitute(
            title=post["title"],
            lang=lang,
            lang_switcher=switcher,
            description=build_post_description(post),
            content=(
                f'<a href="../" class="back-link">{back_label}</a>'
                f'<article><time>{post["date"]}</time>'
                f'<span class="reading-time">{reading_time_str}</span>'
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
        description: str = build_post_description(post)
        excerpt_html: str = f'<p class="excerpt">{description}</p>'
        reading_time_str: str = format_reading_time(
            post["reading_time"], lang
        )
        items.append(
            f"<article>"
            f'<time>{post["date"]}</time>'
            f'<span class="reading-time">{reading_time_str}</span>'
            f'<a href="{post["slug"]}/">{post["title"]}</a>'
            f"{excerpt_html}"
            f"</article>"
        )
    index_content: str = "\n".join(items)
    page: str = template.substitute(
        title=SITE_TITLE,
        lang=lang,
        lang_switcher=switcher,
        description="",
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
    build_feed(lang, lang_dir, lang_posts)


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
