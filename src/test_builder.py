"""Unit tests for the static blog builder."""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from _pytest.capture import CaptureResult

import builder
from config import BlogConfig


SAMPLE_POST: str = """\
---
title: Test Post
date: 2026-01-15
excerpt: A short test excerpt.
---

This is a **test** post.
"""

SAMPLE_POST_2: str = """\
---
title: Earlier Post
date: 2025-12-01
excerpt: An older post excerpt.
---

An older post.
"""

SAMPLE_POST_FR: str = """\
---
title: Article de Test
date: 2026-01-15
excerpt: Un court extrait de test.
---

Ceci est un article de **test**.
"""

SITE_URL: str = "https://example.com"


def _make_config(
    tmp_path: Path,
    post_files: dict[str, str],
    template_text: str = "$lang $lang_switcher $title $description $content $root",
    robots_content: str | None = "User-agent: *\nAllow: /\n",
    languages: list[str] | None = None,
) -> BlogConfig:
    """Build a BlogConfig pointing into tmp_path with the given post files."""
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    for filename, content in post_files.items():
        (posts_dir / filename).write_text(content)

    assets_dir: Path = tmp_path / "assets"
    assets_dir.mkdir(exist_ok=True)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text(template_text)

    robots: Path = tmp_path / "robots.txt"
    if robots_content is not None:
        robots.write_text(robots_content)

    return BlogConfig(
        site_title="Olivier's Blog",
        site_url=SITE_URL,
        author="Olivier",
        favicon_emoji="📝",
        posts_dir=posts_dir,
        build_dir=tmp_path / "build",
        assets_dir=assets_dir,
        robots_file=robots,
        languages=languages if languages is not None else ["en", "fr", "nl"],
        reading_time_labels={
            "en": "min read",
            "fr": "min de lecture",
            "nl": "min leestijd",
        },
        back_labels={"en": "← Back", "fr": "← Retour", "nl": "← Terug"},
        not_found_labels={
            "en": "Page not found",
            "fr": "Page introuvable",
            "nl": "Pagina niet gevonden",
        },
        not_found_home_labels={
            "en": "← Go to homepage",
            "fr": "← Aller à l'accueil",
            "nl": "← Naar de startpagina",
        },
        default_timezone=ZoneInfo("Europe/Brussels"),
        default_publish_hour=13,
        template_file=template,
        style_file=style,
    )


def _build(
    tmp_path: Path,
    post_files: dict[str, str],
    template_text: str = "$lang $lang_switcher $title $description $content $root",
    robots_content: str | None = "User-agent: *\nAllow: /\n",
    languages: list[str] | None = None,
) -> tuple[builder.BlogBuilder, Path]:
    cfg: BlogConfig = _make_config(
        tmp_path, post_files, template_text, robots_content, languages
    )
    return builder.BlogBuilder(cfg), cfg.build_dir


# --- split_stem tests ---


def test_split_stem_valid() -> None:
    assert builder.split_stem("001-hello-world.en") == ("001", "hello-world", "en")


def test_split_stem_slug_with_hyphens() -> None:
    assert builder.split_stem("001-bonjour-le-monde.fr") == (
        "001",
        "bonjour-le-monde",
        "fr",
    )


def test_split_stem_invalid_no_lang() -> None:
    with pytest.raises(ValueError, match="No language suffix"):
        builder.split_stem("001-no-lang")


def test_split_stem_no_prefix() -> None:
    with pytest.raises(ValueError, match="Non-numeric prefix"):
        builder.split_stem("hello-world.en")


def test_split_stem_non_numeric_prefix() -> None:
    with pytest.raises(ValueError, match="Non-numeric prefix"):
        builder.split_stem("abc-hello.en")


# --- parse_post tests ---


def test_parse_post(tmp_path: Path) -> None:
    md_file: Path = tmp_path / "001-test-post.en.md"
    md_file.write_text(SAMPLE_POST)
    result: builder.Post = builder.parse_post(md_file)
    assert result["title"] == "Test Post"
    assert result["date"] == "2026-01-15"
    assert result["excerpt"] == "A short test excerpt."
    assert result["post_id"] == "001"
    assert result["slug"] == "test-post"
    assert result["lang"] == "en"
    assert "<strong>test</strong>" in result["html"]


def test_parse_post_without_excerpt(tmp_path: Path) -> None:
    post_no_excerpt: str = """\
---
title: No Excerpt
date: 2026-01-15
---

Body text.
"""
    md_file: Path = tmp_path / "001-no-excerpt.en.md"
    md_file.write_text(post_no_excerpt)
    result: builder.Post = builder.parse_post(md_file)
    assert result["excerpt"] == ""


# --- estimate_reading_time tests ---


def test_estimate_reading_time_short() -> None:
    assert builder.estimate_reading_time("Hello world this is a short text.") == 1


def test_estimate_reading_time_long() -> None:
    assert builder.estimate_reading_time("word " * 400) == 2


# --- format_reading_time (BlogBuilder method) ---


def test_format_reading_time(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    assert blog.format_reading_time(2, "en") == "2 min read"
    assert blog.format_reading_time(3, "fr") == "3 min de lecture"
    assert blog.format_reading_time(1, "nl") == "1 min leestijd"


# --- group_translations tests ---


def test_group_translations() -> None:
    posts: list[builder.Post] = [
        {"title": "A", "date": "2026-01-01", "excerpt": "", "reading_time": 1,
         "post_id": "001", "slug": "a", "lang": "en", "html": ""},
        {"title": "A", "date": "2026-01-01", "excerpt": "", "reading_time": 1,
         "post_id": "001", "slug": "a-fr", "lang": "fr", "html": ""},
        {"title": "B", "date": "2026-01-02", "excerpt": "", "reading_time": 1,
         "post_id": "002", "slug": "b", "lang": "en", "html": ""},
    ]
    groups: dict[str, dict[str, builder.Post]] = builder.group_translations(posts)
    assert "001" in groups
    assert "en" in groups["001"]
    assert "fr" in groups["001"]
    assert "002" in groups
    assert "fr" not in groups["002"]


# --- render_lang_switcher tests ---


def test_render_lang_switcher() -> None:
    html: str = builder.render_lang_switcher(
        "en", ["en", "fr", "nl"], lambda lang: (f"../{lang}/", True)
    )
    assert "<span>en</span>" in html
    assert '<a href="../fr/">fr</a>' in html
    assert '<a href="../nl/">nl</a>' in html
    assert "lang-switcher" in html


def test_render_lang_switcher_missing_translation() -> None:
    html: str = builder.render_lang_switcher(
        "en",
        ["en", "fr", "nl"],
        lambda lang: (f"../{lang}/", False) if lang == "nl" else (f"../{lang}/", True),
    )
    assert '<a href="../fr/">fr</a>' in html
    assert '<a href="../nl/" class="missing-translation">nl</a>' in html


# --- warn_missing_translations test ---


def test_warn_missing_translations(capsys: pytest.CaptureFixture[str]) -> None:
    translations: dict[str, dict[str, builder.Post]] = {
        "001": {
            "en": {"title": "Hello", "date": "2026-01-01", "excerpt": "",
                   "reading_time": 1, "post_id": "001", "slug": "hello",
                   "lang": "en", "html": ""},
        },
        "002": {
            "en": {"title": "World", "date": "2026-01-02", "excerpt": "",
                   "reading_time": 1, "post_id": "002", "slug": "world",
                   "lang": "en", "html": ""},
            "fr": {"title": "Monde", "date": "2026-01-02", "excerpt": "",
                   "reading_time": 1, "post_id": "002", "slug": "monde",
                   "lang": "fr", "html": ""},
            "nl": {"title": "Wereld", "date": "2026-01-02", "excerpt": "",
                   "reading_time": 1, "post_id": "002", "slug": "wereld",
                   "lang": "nl", "html": ""},
        },
    }
    builder.warn_missing_translations(translations, ["en", "fr", "nl"])
    captured: CaptureResult[str] = capsys.readouterr()
    assert "001" in captured.err
    assert "Hello" in captured.err
    assert "fr" in captured.err and "nl" in captured.err
    assert "002" not in captured.err


# --- load_posts tests ---


def test_load_posts_rejects_unknown_language(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {"001-hallo.de.md": SAMPLE_POST})
    with pytest.raises(ValueError, match="Language not defined in configuration"):
        blog.load_posts()


# --- Integration tests ---


def test_build_creates_index_and_post_pages(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
    )
    blog.build_site()
    assert (build_dir / "en" / "index.html").exists()
    assert (build_dir / "en" / "first" / "index.html").exists()
    assert (build_dir / "en" / "second" / "index.html").exists()
    assert (build_dir / "style.css").exists()


def test_build_index_lists_posts_newest_first(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
        template_text="$lang $lang_switcher $description $content",
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert index_html.index("Test Post") < index_html.index("Earlier Post")


def test_build_post_page_contains_content(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $title $description $content",
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "Test Post" in post_html
    assert "<strong>test</strong>" in post_html


def test_build_cleans_previous_build(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $description $content",
    )
    build_dir.mkdir()
    stale_file: Path = build_dir / "stale.html"
    stale_file.write_text("old")
    blog.build_site()
    assert not stale_file.exists()


def test_build_multilang_creates_per_lang_dirs(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )
    blog.build_site()
    assert (build_dir / "en" / "hello" / "index.html").exists()
    assert (build_dir / "fr" / "bonjour" / "index.html").exists()
    assert (build_dir / "nl" / "index.html").exists()


def test_build_root_redirect(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    root_html: str = (build_dir / "index.html").read_text()
    assert "url=en/" in root_html
    assert "refresh" in root_html


def test_build_root_redirect_has_rss_discovery_link(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    root_html: str = (build_dir / "index.html").read_text()
    assert 'type="application/rss+xml"' in root_html
    assert 'href="en/feed.xml"' in root_html


def test_build_root_redirect_rss_uses_default_language(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-bonjour.fr.md": SAMPLE_POST_FR},
        languages=["fr", "en", "nl"],
    )
    blog.build_site()
    root_html: str = (build_dir / "index.html").read_text()
    assert 'href="fr/feed.xml"' in root_html
    assert 'type="application/rss+xml"' in root_html
    assert "url=fr/" in root_html


def test_build_lang_switcher_on_post_page(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )
    blog.build_site()
    en_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "<span>en</span>" in en_html
    assert "../../fr/bonjour/" in en_html
    assert '<a href="./" class="missing-translation">nl</a>' in en_html

    fr_html: str = (build_dir / "fr" / "bonjour" / "index.html").read_text()
    assert "<span>fr</span>" in fr_html
    assert "../../en/hello/" in fr_html
    assert '<a href="./" class="missing-translation">nl</a>' in fr_html


def test_build_lang_switcher_on_index_page(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<span>en</span>" in index_html
    assert "../fr/" in index_html
    assert "../nl/" in index_html


def test_build_post_page_has_back_link(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $title $description $content",
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert 'class="back-link"' in post_html
    assert 'href="../"' in post_html


def test_build_warns_about_missing_translations(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"002-only-english.en.md": SAMPLE_POST})
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "002" in captured.err
    assert "fr" in captured.err and "nl" in captured.err
    assert (build_dir / "en" / "only-english" / "index.html").exists()


def test_build_post_strikethrough_for_missing_translation(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"002-only-english.en.md": SAMPLE_POST})
    blog.build_site()
    post_html: str = (build_dir / "en" / "only-english" / "index.html").read_text()
    assert '<a href="./" class="missing-translation">fr</a>' in post_html
    assert '<a href="./" class="missing-translation">nl</a>' in post_html


def test_build_writes_sitemap_with_posts_and_indexes(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )
    blog.build_site()
    sitemap: str = (build_dir / "sitemap.xml").read_text()
    assert '<?xml version="1.0" encoding="UTF-8"?>' in sitemap
    assert 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in sitemap
    assert f"<loc>{SITE_URL}/en/</loc>" in sitemap
    assert f"<loc>{SITE_URL}/fr/</loc>" in sitemap
    assert f"<loc>{SITE_URL}/nl/</loc>" in sitemap
    assert f"<loc>{SITE_URL}/en/hello/</loc>" in sitemap
    assert f"<loc>{SITE_URL}/fr/bonjour/</loc>" in sitemap
    assert "<lastmod>2026-01-15</lastmod>" in sitemap


def test_build_writes_robots_with_sitemap_directive(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    robots: str = (build_dir / "robots.txt").read_text()
    assert "User-agent: *" in robots
    assert f"Sitemap: {SITE_URL}/sitemap.xml" in robots


def test_build_robots_does_not_duplicate_sitemap_directive(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        robots_content=(
            f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
        ),
    )
    blog.build_site()
    robots: str = (build_dir / "robots.txt").read_text()
    assert robots.count(f"Sitemap: {SITE_URL}/sitemap.xml") == 1


def test_build_robots_warns_when_source_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path, {"001-hello.en.md": SAMPLE_POST}, robots_content=None
    )
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "robots.txt" in captured.err
    assert not (build_dir / "robots.txt").exists()


def test_build_post_page_back_link_localized(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
        template_text="$lang_switcher $title $description $content",
    )
    blog.build_site()
    en_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "Back" in en_html
    fr_html: str = (build_dir / "fr" / "bonjour" / "index.html").read_text()
    assert "Retour" in fr_html


def test_build_post_page_article_structure(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path, {"001-hello.en.md": SAMPLE_POST}, template_text="$content"
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "<h1>Test Post</h1>" in post_html
    assert '<div class="meta">' in post_html
    pos_title: int = post_html.index("<h1>")
    pos_meta: int = post_html.index('<div class="meta">')
    pos_content: int = post_html.index("<strong>test</strong>")
    assert pos_title < pos_meta < pos_content


def test_build_index_article_structure(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$description $content",
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<article>" in index_html
    assert "<time>" in index_html
    assert 'href="hello/">' in index_html
    assert '<div class="meta">' in index_html
    pos_title: int = index_html.index('href="hello/">')
    pos_date: int = index_html.index("<time>")
    pos_excerpt: int = index_html.index("excerpt")
    assert pos_title < pos_date < pos_excerpt


def test_build_html_lang_attribute(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.fr.md": SAMPLE_POST_FR},
        template_text='<html lang="$lang">$lang_switcher $title $description $content $root</html>',
    )
    blog.build_site()
    fr_html: str = (build_dir / "fr" / "hello" / "index.html").read_text()
    assert 'lang="fr"' in fr_html


def test_build_index_shows_excerpt(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$description $content",
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert '<p class="excerpt">A short test excerpt.</p>' in index_html


def test_build_index_shows_fallback_when_no_excerpt(tmp_path: Path) -> None:
    post_no_excerpt: str = """\
---
title: No Excerpt
date: 2026-01-15
---

Some body text without an excerpt field.
"""
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": post_no_excerpt},
        template_text="$content",
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert '<p class="excerpt">' in index_html
    assert "Some body text without an excerpt field." in index_html


def test_build_post_page_has_meta_description(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text='<meta name="description" content="$description">$content',
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert '<meta name="description" content="A short test excerpt.">' in post_html
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert '<meta name="description" content="">' in index_html


def test_build_post_meta_description_fallback(tmp_path: Path) -> None:
    post_no_excerpt: str = """\
---
title: No Excerpt
date: 2026-01-15
---

Some body text without an excerpt field.
"""
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": post_no_excerpt},
        template_text='<meta name="description" content="$description">$content',
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "Some body text without an excerpt field." in post_html
    assert 'content=""' not in post_html


# --- Reading time integration tests ---


def test_build_post_page_shows_reading_time(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path, {"001-hello.en.md": SAMPLE_POST}, template_text="$content"
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "min read" in post_html
    assert 'class="reading-time"' in post_html


def test_build_post_page_shows_localized_reading_time(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path, {"001-bonjour.fr.md": SAMPLE_POST_FR}, template_text="$content"
    )
    blog.build_site()
    fr_html: str = (build_dir / "fr" / "bonjour" / "index.html").read_text()
    assert "min de lecture" in fr_html


def test_build_index_shows_reading_time(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path, {"001-hello.en.md": SAMPLE_POST}, template_text="$content"
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "min read" in index_html
    assert 'class="reading-time"' in index_html


# --- Header / footer template tests ---


def test_template_globals_contains_site_title_author_year(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    globals_: dict[str, str] = blog.template_globals()
    assert globals_["site_title"] == "Olivier's Blog"
    assert globals_["author"] == "Olivier"
    current_year: int = datetime.now(tz=blog.cfg.default_timezone).year
    assert globals_["year"] == str(current_year)


def test_build_header_uses_site_title(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text=(
            "<header><h1>$site_title</h1></header>"
            "$lang_switcher $title $description $content $root"
        ),
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<header><h1>Olivier's Blog</h1></header>" in index_html
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "<header><h1>Olivier's Blog</h1></header>" in post_html


def test_build_footer_uses_author_and_year(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text=(
            "<footer>&copy; $author $year</footer>"
            "$lang_switcher $title $description $content $root"
        ),
    )
    blog.build_site()
    current_year: int = datetime.now(tz=blog.cfg.default_timezone).year
    expected: str = f"<footer>&copy; Olivier {current_year}</footer>"
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert expected in index_html
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert expected in post_html


# --- Favicon tests ---


def test_build_writes_favicon_svg(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    favicon: Path = build_dir / "favicon.svg"
    assert favicon.is_file()
    content: str = favicon.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "📝" in content
    assert "<text" in content


def test_build_template_references_favicon(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text=(
            '<link rel="icon" type="image/svg+xml" href="$root/favicon.svg">'
            "$lang_switcher $title $description $content"
        ),
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert 'href="../favicon.svg"' in index_html
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert 'href="../../favicon.svg"' in post_html


# --- Image / asset handling tests ---


SAMPLE_POST_WITH_IMAGES: str = """\
---
title: Image Post
date: 2026-02-01
excerpt: Has images.
---

External: ![ext](https://example.com/img.png)

Internal: ![int](assets/img/foo.png)
"""


def test_extract_relative_image_sources() -> None:
    html: str = (
        '<p><img alt="ext" src="https://example.com/x.png" /> '
        '<img alt="abs" src="/absolute.png" /> '
        '<img alt="rel" src="assets/img/foo.png" /></p>'
    )
    assert builder.extract_relative_image_sources(html) == ["assets/img/foo.png"]


def test_rewrite_relative_image_sources() -> None:
    html: str = (
        '<img src="assets/img/foo.png" />'
        '<img src="https://x.example/y.png" />'
        '<img src="/abs.png" />'
    )
    rewritten: str = builder.rewrite_relative_image_sources(html, "../..")
    assert '<img src="../../assets/img/foo.png" />' in rewritten
    assert '<img src="https://x.example/y.png" />' in rewritten
    assert '<img src="/abs.png" />' in rewritten


def test_build_copies_assets(tmp_path: Path) -> None:
    cfg: BlogConfig = _make_config(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    (cfg.assets_dir / "img").mkdir()
    (cfg.assets_dir / "img" / "logo.png").write_bytes(b"\x89PNGfake")
    blog: builder.BlogBuilder = builder.BlogBuilder(cfg)
    blog.build_site()
    assert (cfg.build_dir / "assets" / "img" / "logo.png").read_bytes() == b"\x89PNGfake"


def test_build_warns_when_assets_dir_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg: BlogConfig = _make_config(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    cfg.assets_dir.rmdir()
    blog: builder.BlogBuilder = builder.BlogBuilder(cfg)
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "assets directory" in captured.err
    assert not (cfg.build_dir / "assets").exists()


def test_build_warns_about_missing_image(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-images.en.md": SAMPLE_POST_WITH_IMAGES},
        template_text="$content",
    )
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "missing image" in captured.err
    assert "assets/img/foo.png" in captured.err


def test_build_does_not_warn_when_image_present(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg: BlogConfig = _make_config(
        tmp_path,
        {"001-images.en.md": SAMPLE_POST_WITH_IMAGES},
        template_text="$content",
    )
    (cfg.assets_dir / "img").mkdir()
    (cfg.assets_dir / "img" / "foo.png").write_bytes(b"data")
    blog: builder.BlogBuilder = builder.BlogBuilder(cfg)
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "missing image" not in captured.err


def test_build_post_rewrites_internal_image_src(tmp_path: Path) -> None:
    cfg: BlogConfig = _make_config(
        tmp_path,
        {"001-images.en.md": SAMPLE_POST_WITH_IMAGES},
        template_text="$content",
    )
    (cfg.assets_dir / "img").mkdir()
    (cfg.assets_dir / "img" / "foo.png").write_bytes(b"data")
    blog: builder.BlogBuilder = builder.BlogBuilder(cfg)
    blog.build_site()
    post_html: str = (cfg.build_dir / "en" / "images" / "index.html").read_text()
    assert 'src="../../assets/img/foo.png"' in post_html
    assert 'src="https://example.com/img.png"' in post_html


# --- Link handling tests ---


SAMPLE_POST_WITH_LINKS: str = """\
---
title: Link Post
date: 2026-03-01
excerpt: Has links.
---

External: [example](http://www.example.com)

New tab: [other](tab:http://www.example.com)

Internal: [hello](posts/001-hello-world.en.md)

Autolink: <http://www.example.com>

Missing: [gone](posts/999-missing.en.md)
"""


def test_rewrite_new_tab_links() -> None:
    html: str = '<a href="tab:http://example.com">x</a>'
    rewritten: str = builder.rewrite_new_tab_links(html)
    assert 'href="http://example.com"' in rewritten
    assert 'target="_blank"' in rewritten
    assert 'rel="noopener noreferrer"' in rewritten
    assert "tab:" not in rewritten


def test_rewrite_new_tab_links_leaves_others_alone() -> None:
    html: str = '<a href="http://example.com">x</a>'
    assert builder.rewrite_new_tab_links(html) == html


def test_rewrite_internal_post_links() -> None:
    html: str = '<a href="posts/001-hello-world.en.md">hello</a>'
    rewritten: str = builder.rewrite_internal_post_links(html, "../..", "posts")
    assert '<a href="../../en/hello-world/">hello</a>' == rewritten


def test_rewrite_internal_post_links_unparseable_left_alone() -> None:
    html: str = '<a href="posts/no-prefix.md">x</a>'
    assert (
        builder.rewrite_internal_post_links(html, "../..", "posts") == html
    )


def test_transform_post_links_combines_tab_and_internal() -> None:
    html: str = (
        '<a href="tab:posts/001-hello-world.en.md">hello</a>'
    )
    rewritten: str = builder.transform_post_links(html, "../..", "posts")
    assert 'href="../../en/hello-world/"' in rewritten
    assert 'target="_blank"' in rewritten


def test_extract_internal_post_link_stems() -> None:
    html: str = (
        '<a href="posts/001-hello-world.en.md">a</a>'
        '<a href="posts/002-other.fr.md">b</a>'
        '<a href="http://example.com">c</a>'
    )
    stems: list[str] = builder.extract_internal_post_link_stems(html, "posts")
    assert stems == ["001-hello-world.en", "002-other.fr"]


def test_build_post_renders_external_and_autolink(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {
            "001-hello.en.md": SAMPLE_POST,
            "002-links.en.md": SAMPLE_POST_WITH_LINKS,
        },
        template_text="$content",
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "links" / "index.html").read_text()
    assert '<a href="http://www.example.com">example</a>' in post_html
    # Autolink rendered via python-markdown
    assert post_html.count('href="http://www.example.com"') >= 2


def test_build_post_renders_new_tab_link(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {
            "001-hello.en.md": SAMPLE_POST,
            "002-links.en.md": SAMPLE_POST_WITH_LINKS,
        },
        template_text="$content",
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "links" / "index.html").read_text()
    assert 'target="_blank"' in post_html
    assert 'rel="noopener noreferrer"' in post_html
    assert 'href="tab:' not in post_html


def test_build_post_renders_internal_link(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {
            "001-hello.en.md": SAMPLE_POST,
            "002-links.en.md": SAMPLE_POST_WITH_LINKS,
        },
        template_text="$content",
    )
    blog.build_site()
    post_html: str = (build_dir / "en" / "links" / "index.html").read_text()
    assert '<a href="../../en/hello-world/">hello</a>' in post_html


def test_build_warns_about_missing_internal_link(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(
        tmp_path,
        {
            "001-hello.en.md": SAMPLE_POST,
            "002-links.en.md": SAMPLE_POST_WITH_LINKS,
        },
        template_text="$content",
    )
    blog.build_site()
    captured: CaptureResult[str] = capsys.readouterr()
    assert "missing post" in captured.err
    assert "999-missing.en.md" in captured.err


# --- format_rfc822_date / render_rss_item (BlogBuilder methods) ---


def test_format_rfc822_date(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    assert blog.format_rfc822_date("2026-02-16") == "Mon, 16 Feb 2026 13:00:00 +0100"


def test_format_rfc822_date_summer_dst(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    assert blog.format_rfc822_date("2026-07-15") == "Wed, 15 Jul 2026 13:00:00 +0200"


def test_render_rss_item(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    post: builder.Post = {
        "title": "Test Post",
        "date": "2026-01-15",
        "excerpt": "A test excerpt.",
        "reading_time": 1,
        "post_id": "001",
        "slug": "test-post",
        "lang": "en",
        "html": "<p>Hello <strong>world</strong></p>",
    }
    item: str = blog.render_rss_item(post, "en")
    assert "<title>Test Post</title>" in item
    assert f"<link>{SITE_URL}/en/test-post/</link>" in item
    assert f"<guid>{SITE_URL}/en/test-post/</guid>" in item
    assert "<pubDate>Thu, 15 Jan 2026 13:00:00 +0100</pubDate>" in item
    assert "A test excerpt." in item


def test_render_rss_item_escapes_title(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    blog, _ = _build(tmp_path, {})
    post: builder.Post = {
        "title": "A <b>Bold</b> & \"Quoted\" Title",
        "date": "2026-01-15",
        "excerpt": "",
        "reading_time": 1,
        "post_id": "001",
        "slug": "bold-title",
        "lang": "en",
        "html": "<p>Content</p>",
    }
    item: str = blog.render_rss_item(post, "en")
    assert "A &lt;b&gt;Bold&lt;/b&gt; &amp; &quot;Quoted&quot; Title" in item


# --- build_post_description tests ---


def test_build_post_description_uses_excerpt() -> None:
    post: builder.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "My excerpt.",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": "<p>Full content here.</p>",
    }
    assert builder.build_post_description(post) == "My excerpt."


def test_build_post_description_fallback_short() -> None:
    post: builder.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": "<p>Short content.</p>",
    }
    assert builder.build_post_description(post) == "Short content."


def test_build_post_description_fallback_truncates() -> None:
    long_text: str = "A" * 300
    post: builder.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": f"<p>{long_text}</p>",
    }
    result: str = builder.build_post_description(post)
    assert result == "A" * 200 + "..."


# --- RSS feed integration tests ---


def test_build_creates_rss_feeds(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )
    blog.build_site()
    assert (build_dir / "en" / "feed.xml").exists()
    assert (build_dir / "fr" / "feed.xml").exists()
    assert (build_dir / "nl" / "feed.xml").exists()


def test_rss_feed_contains_posts(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert 'version="2.0"' in feed
    assert "<language>en</language>" in feed
    assert "<title>Test Post</title>" in feed


def test_rss_feed_only_contains_lang_posts(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )
    blog.build_site()
    en_feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "Test Post" in en_feed
    assert "Article de Test" not in en_feed
    fr_feed: str = (build_dir / "fr" / "feed.xml").read_text()
    assert "Article de Test" in fr_feed
    assert "Test Post" not in fr_feed


def test_rss_feed_posts_sorted_newest_first(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
    )
    blog.build_site()
    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert feed.index("Test Post") < feed.index("Earlier Post")


def test_rss_feed_uses_excerpt_as_description(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "A short test excerpt." in feed
    assert "&lt;p&gt;" not in feed


def test_rss_feed_truncates_without_excerpt(tmp_path: Path) -> None:
    long_body: str = "word " * 100
    post_no_excerpt: str = f"""\
---
title: Long Post
date: 2026-01-15
---

{long_body}
"""
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-long.en.md": post_no_excerpt})
    blog.build_site()
    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "..." in feed


# --- 404 page tests ---


def test_build_creates_404_page(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(tmp_path, {"001-hello.en.md": SAMPLE_POST})
    blog.build_site()
    assert (build_dir / "404.html").exists()


def test_build_404_page_contains_not_found_label(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$content",
    )
    blog.build_site()
    page: str = (build_dir / "404.html").read_text()
    assert "Page not found" in page


def test_build_404_page_contains_home_link(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$content",
    )
    blog.build_site()
    page: str = (build_dir / "404.html").read_text()
    assert 'href="en/"' in page
    assert "Go to homepage" in page


def test_build_404_page_uses_default_language(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-bonjour.fr.md": SAMPLE_POST_FR},
        template_text="$lang $content",
        languages=["fr", "en", "nl"],
    )
    blog.build_site()
    page: str = (build_dir / "404.html").read_text()
    assert "fr " in page
    assert 'href="fr/"' in page
    assert "Page introuvable" in page


def test_build_404_page_has_lang_switcher(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang_switcher $content",
    )
    blog.build_site()
    page: str = (build_dir / "404.html").read_text()
    assert "lang-switcher" in page
    assert 'href="fr/"' in page
    assert 'href="nl/"' in page


def test_build_404_page_uses_template(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="<footer>&copy; $author $year</footer>$content",
    )
    blog.build_site()
    page: str = (build_dir / "404.html").read_text()
    assert "<footer>" in page
    assert "Olivier" in page


def test_rss_discovery_link_in_html(tmp_path: Path) -> None:
    blog: builder.BlogBuilder
    build_dir: Path
    blog, build_dir = _build(
        tmp_path,
        {"001-hello.en.md": SAMPLE_POST},
        template_text=(
            '<link rel="stylesheet" href="$root/style.css">'
            '<link rel="alternate" type="application/rss+xml"'
            ' title="$title - RSS" href="$root/$lang/feed.xml">'
            "$lang_switcher $description $content"
        ),
    )
    blog.build_site()
    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert 'type="application/rss+xml"' in index_html
    assert "../en/feed.xml" in index_html
    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "../../en/feed.xml" in post_html
