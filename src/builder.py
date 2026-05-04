from datetime import datetime
import html
import math
from pathlib import Path
import re
import shutil
from string import Template
import sys
from typing import Any, Callable, TypedDict

import markdown
import yaml

from config import BlogConfig


class Post(TypedDict):
    title: str
    date: str
    excerpt: str
    reading_time: int
    post_id: str
    slug: str
    lang: str
    html: str


class BlogBuilder:
    def __init__(self, cfg: BlogConfig):
        self.cfg = cfg

    def build_site(self) -> None:
        self.prepare_build_dir()
        template: Template = Template(self.cfg.template_file.read_text(encoding="utf-8"))
        posts: list[Post] = self.load_posts()
        translations: dict[str, dict[str, Post]] = group_translations(posts)
        warn_missing_translations(translations, self.cfg.languages)

        for lang in self.cfg.languages:
            self.build_lang(lang, posts, translations, template)

        self.build_root_redirect()
        self.build_sitemap(posts)
        self.build_robots()

        print(f"Built {len(posts)} posts -> {self.cfg.build_dir}/")

    def format_reading_time(self, minutes: int, lang: str) -> str:
        """Return localized reading time string, e.g. '2 min read'."""
        label: str = self.cfg.reading_time_labels[lang]
        return f"{minutes} {label}"

    def prepare_build_dir(self) -> None:
        """Clean and recreate the build directory, copy static assets."""
        if self.cfg.build_dir.exists():
            shutil.rmtree(self.cfg.build_dir)
        self.cfg.build_dir.mkdir()
        shutil.copy2(self.cfg.style_file, self.cfg.build_dir / "style.css")

    def load_posts(self) -> list[Post]:
        """Glob, parse, and sort all posts by date descending."""
        posts: list[Post] = []
        for p in sorted(self.cfg.posts_dir.glob("*.md")):
            post: Post = parse_post(p)
            if post.get("lang") not in self.cfg.languages:
                raise ValueError(f"Language not defined in configuration for file {p}")
            posts.append(post)
        posts.sort(key=lambda p: p["date"], reverse=True)
        return posts

    def format_rfc822_date(self, iso_date: str) -> str:
        """Convert an ISO date string (YYYY-MM-DD) to RFC 822 format for RSS.

        Uses Europe/Brussels timezone and 13:00 as the default publish time.
        """
        dt: datetime = datetime.strptime(iso_date, "%Y-%m-%d").replace(
            hour=self.cfg.default_publish_hour, tzinfo=self.cfg.default_timezone
        )
        return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

    def render_rss_item(self, post: Post, lang: str) -> str:
        """Render a single RSS <item> element for a post."""
        url: str = f"{self.cfg.site_url}/{lang}/{post['slug']}/"
        title_escaped: str = html.escape(post["title"])
        description: str = html.escape(build_post_description(post))
        pub_date: str = self.format_rfc822_date(post["date"])
        return (
            "<item>"
            f"<title>{title_escaped}</title>"
            f"<link>{url}</link>"
            f"<description>{description}</description>"
            f"<pubDate>{pub_date}</pubDate>"
            f"<guid>{url}</guid>"
            "</item>"
        )

    def build_feed(self, lang: str, lang_dir: Path, lang_posts: list[Post]) -> None:
        """Build an RSS 2.0 feed.xml for a given language."""
        feed_url: str = f"{self.cfg.site_url}/{lang}/feed.xml"
        lang_url: str = f"{self.cfg.site_url}/{lang}/"
        items: str = "\n".join(self.render_rss_item(post, lang) for post in lang_posts)
        feed: str = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "<channel>\n"
            f"<title>{html.escape(self.cfg.site_title)}</title>\n"
            f"<link>{lang_url}</link>\n"
            f"<description>{html.escape(self.cfg.site_title)}</description>\n"
            f"<language>{lang}</language>\n"
            f'<atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>\n'
            f"{items}\n"
            "</channel>\n"
            "</rss>"
        )
        (lang_dir / "feed.xml").write_text(feed, encoding="utf-8")

    def build_post_pages(
        self,
        lang: str,
        lang_dir: Path,
        lang_posts: list[Post],
        translations: dict[str, dict[str, Post]],
        template: Template,
    ) -> None:
        """Write individual post pages for a given language."""
        available_langs: list[str] = self.cfg.languages
        for post in lang_posts:
            slug: str = post["slug"]
            post_id: str = post["post_id"]
            post_dir: Path = lang_dir / slug
            post_dir.mkdir(parents=True)
            sibling_posts: dict[str, Post] = translations.get(post_id, {})

            def resolve(other_lang: str, sp: dict[str, Post] = sibling_posts) -> tuple[str, bool]:
                if other_lang in sp:
                    return (f"../../{other_lang}/{sp[other_lang]['slug']}/", True)
                return ("./", False)

            switcher: str = render_lang_switcher(lang, available_langs, resolve)
            back_label: str = self.cfg.back_labels[lang]
            reading_time_str: str = self.format_reading_time(
                post["reading_time"], lang
            )
            page: str = template.substitute(
                title=post["title"],
                lang=lang,
                lang_switcher=switcher,
                description=build_post_description(post),
                content=(
                    f'<a href="../" class="back-link">{back_label}</a>'
                    f"<article>"
                    f'<h1>{post["title"]}</h1>'
                    f'<div class="meta">'
                    f'<time>{post["date"]}</time>'
                    f'<span class="reading-time">{reading_time_str}</span>'
                    f"</div>"
                    f'{post["html"]}</article>'
                ),
                root="../..",
            )
            (post_dir / "index.html").write_text(page, encoding="utf-8")

    def build_index_page(
        self,
        lang: str,
        lang_dir: Path,
        lang_posts: list[Post],
        template: Template,
    ) -> None:
        """Write the index page for a given language."""
        available_langs: list[str] = self.cfg.languages
        switcher: str = render_lang_switcher(
            lang,
            available_langs,
            lambda other_lang: (f"../{other_lang}/", True),
        )
        items: list[str] = []
        for post in lang_posts:
            description: str = build_post_description(post)
            excerpt_html: str = f'<p class="excerpt">{description}</p>'
            reading_time_str: str = self.format_reading_time(
                post["reading_time"], lang
            )
            items.append(
                f"<article>"
                f'<a href="{post["slug"]}/">{post["title"]}</a>'
                f'<div class="meta">'
                f'<time>{post["date"]}</time>'
                f'<span class="reading-time">{reading_time_str}</span>'
                f"</div>"
                f"{excerpt_html}"
                f"</article>"
            )
        index_content: str = "\n".join(items)
        page: str = template.substitute(
            title=self.cfg.site_title,
            lang=lang,
            lang_switcher=switcher,
            description="",
            content=index_content,
            root="..",
        )
        (lang_dir / "index.html").write_text(page, encoding="utf-8")

    def build_lang(
        self,
        lang: str,
        posts: list[Post],
        translations: dict[str, dict[str, Post]],
        template: Template,
    ) -> None:
        """Build all pages for a given language."""
        lang_dir: Path = self.cfg.build_dir / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        lang_posts: list[Post] = [p for p in posts if p["lang"] == lang]
        self.build_post_pages(lang, lang_dir, lang_posts, translations, template)
        self.build_index_page(lang, lang_dir, lang_posts, template)
        self.build_feed(lang, lang_dir, lang_posts)

    def build_sitemap(self, posts: list[Post]) -> None:
        """Write sitemap.xml listing all language indexes and post pages."""
        latest_per_lang: dict[str, str] = {}
        for post in posts:
            current: str = latest_per_lang.get(post["lang"], "")
            if post["date"] > current:
                latest_per_lang[post["lang"]] = post["date"]

        entries: list[str] = []
        for lang in self.cfg.languages:
            loc: str = f"{self.cfg.site_url}/{lang}/"
            if lang in latest_per_lang:
                entries.append(
                    f"<url><loc>{loc}</loc>"
                    f"<lastmod>{latest_per_lang[lang]}</lastmod></url>"
                )
            else:
                entries.append(f"<url><loc>{loc}</loc></url>")
        for post in posts:
            post_loc: str = f"{self.cfg.site_url}/{post['lang']}/{post['slug']}/"
            entries.append(
                f"<url><loc>{post_loc}</loc>"
                f"<lastmod>{post['date']}</lastmod></url>"
            )

        sitemap: str = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(entries)
            + "\n</urlset>"
        )
        (self.cfg.build_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    def build_robots(self) -> None:
        """Copy seo/robots.txt to build/, ensuring the Sitemap directive is set."""
        directive: str = f"Sitemap: {self.cfg.site_url}/sitemap.xml"
        if not self.cfg.robots_file.is_file():
            print(
                f"Warning: {self.cfg.robots_file} not found; skipping robots.txt generation.",
                file=sys.stderr,
            )
            return
        source_text: str = self.cfg.robots_file.read_text(encoding="utf-8")
        if directive not in source_text:
            if source_text and not source_text.endswith("\n"):
                source_text += "\n"
            source_text += directive + "\n"
        (self.cfg.build_dir / "robots.txt").write_text(source_text, encoding="utf-8")

    def build_root_redirect(self) -> None:
        """Write a root index.html that redirects to /en/."""
        html: str = (
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta http-equiv="refresh" content="0;url=en/">\n'
            "</head>\n<body></body>\n</html>"
        )
        (self.cfg.build_dir / "index.html").write_text(html, encoding="utf-8")


def warn_missing_translations(
    translations: dict[str, dict[str, "Post"]],
    languages: list[str],
) -> None:
    """Print a warning to stderr for each post missing one or more translations."""
    for post_id in sorted(translations.keys()):
        by_lang: dict[str, Post] = translations[post_id]
        missing: list[str] = [lang for lang in languages if lang not in by_lang]
        if not missing:
            continue
        sample_post: Post = next(iter(by_lang.values()))
        print(
            f"Warning: post {post_id} ('{sample_post['title']}') is missing "
            f"translation(s): {', '.join(missing)}",
            file=sys.stderr,
        )


def build_post_description(post: Post) -> str:
    """Return the post description: excerpt or truncated plain text."""
    if post["excerpt"]:
        return post["excerpt"]
    plain: str = re.sub(r"<[^>]+>", "", post["html"])
    if len(plain) <= 200:
        return plain
    return plain[:200] + "..."


def render_lang_switcher(
    current_lang: str,
    available_langs: list[str],
    link_builder: Callable[[str], tuple[str, bool]],
) -> str:
    """Generate a language switcher nav element.

    `link_builder` returns `(href, is_translated)` for each other language.
    When `is_translated` is False the link is rendered strikethrough so the
    reader can see the translation is missing without hitting a 404.
    """
    items: list[str] = []
    for lang in available_langs:
        if lang == current_lang:
            items.append(f"<span>{lang}</span>")
            continue
        href: str
        is_translated: bool
        href, is_translated = link_builder(lang)
        if is_translated:
            items.append(f'<a href="{href}">{lang}</a>')
        else:
            items.append(
                f'<a href="{href}" class="missing-translation">{lang}</a>'
            )
    return '<nav class="lang-switcher">' + " | ".join(items) + "</nav>"


def group_translations(posts: list[Post]) -> dict[str, dict[str, Post]]:
    """Group posts by post_id, then by lang. Returns {post_id: {lang: Post}}."""
    groups: dict[str, dict[str, Post]] = {}
    for post in posts:
        post_id: str = post["post_id"]
        if post_id not in groups:
            groups[post_id] = {}
        groups[post_id][post["lang"]] = post
    return groups


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


def estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes from raw markdown text."""
    word_count: int = len(text.split())
    return max(1, math.ceil(word_count / 200))


def split_stem(stem: str) -> tuple[str, str, str]:
    """Extract post_id, slug, and lang from a stem like '001-hello-world.en'.

    Returns (post_id, slug, lang).
    """
    dot_index: int = stem.rfind(".")
    if dot_index == -1:
        raise ValueError(f"No language suffix in stem: {stem!r}")
    prefix_slug: str = stem[:dot_index]
    lang: str = stem[dot_index + 1 :]
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
