"""Unit tests for the blog build engine."""

from pathlib import Path

import pytest

import build


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


def _setup_site(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    post_files: dict[str, str],
    template_text: str = "$lang $lang_switcher $title $description $content $root",
) -> Path:
    """Helper to set up a temporary site structure. Returns build_dir."""
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    for filename, content in post_files.items():
        (posts_dir / filename).write_text(content)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text(template_text)

    build_dir: Path = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    return build_dir


# --- split_stem tests ---


def test_split_stem_valid() -> None:
    post_id: str
    slug: str
    lang: str
    post_id, slug, lang = build.split_stem("001-hello-world.en")
    assert post_id == "001"
    assert slug == "hello-world"
    assert lang == "en"


def test_split_stem_slug_with_hyphens() -> None:
    post_id: str
    slug: str
    lang: str
    post_id, slug, lang = build.split_stem("001-bonjour-le-monde.fr")
    assert post_id == "001"
    assert slug == "bonjour-le-monde"
    assert lang == "fr"


def test_split_stem_invalid_no_lang() -> None:
    with pytest.raises(ValueError, match="No language suffix"):
        build.split_stem("001-no-lang")


def test_split_stem_invalid_unknown_lang() -> None:
    with pytest.raises(ValueError, match="Unknown language"):
        build.split_stem("001-hello.de")


def test_split_stem_no_prefix() -> None:
    with pytest.raises(ValueError, match="Non-numeric prefix"):
        build.split_stem("hello-world.en")


def test_split_stem_non_numeric_prefix() -> None:
    with pytest.raises(ValueError, match="Non-numeric prefix"):
        build.split_stem("abc-hello.en")


# --- parse_post tests ---


def test_parse_post(tmp_path: Path) -> None:
    md_file: Path = tmp_path / "001-test-post.en.md"
    md_file.write_text(SAMPLE_POST)
    result: build.Post = build.parse_post(md_file)
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
    result: build.Post = build.parse_post(md_file)
    assert result["excerpt"] == ""


# --- estimate_reading_time tests ---


def test_estimate_reading_time_short() -> None:
    short_text: str = "Hello world this is a short text."
    assert build.estimate_reading_time(short_text) == 1


def test_estimate_reading_time_long() -> None:
    long_text: str = "word " * 400
    assert build.estimate_reading_time(long_text) == 2


# --- format_reading_time tests ---


def test_format_reading_time() -> None:
    assert build.format_reading_time(2, "en") == "2 min read"
    assert build.format_reading_time(3, "fr") == "3 min de lecture"
    assert build.format_reading_time(1, "nl") == "1 min leestijd"


# --- parse_post reading_time test ---


def test_parse_post_includes_reading_time(tmp_path: Path) -> None:
    md_file: Path = tmp_path / "001-test-post.en.md"
    md_file.write_text(SAMPLE_POST)
    result: build.Post = build.parse_post(md_file)
    assert "reading_time" in result
    assert result["reading_time"] >= 1


# --- group_translations tests ---


def test_group_translations() -> None:
    posts: list[build.Post] = [
        {"title": "A", "date": "2026-01-01", "excerpt": "", "reading_time": 1, "post_id": "001", "slug": "a", "lang": "en", "html": ""},
        {"title": "A", "date": "2026-01-01", "excerpt": "", "reading_time": 1, "post_id": "001", "slug": "a-fr", "lang": "fr", "html": ""},
        {"title": "B", "date": "2026-01-02", "excerpt": "", "reading_time": 1, "post_id": "002", "slug": "b", "lang": "en", "html": ""},
    ]
    groups: dict[str, dict[str, build.Post]] = build.group_translations(posts)
    assert "001" in groups
    assert "en" in groups["001"]
    assert "fr" in groups["001"]
    assert "002" in groups
    assert "en" in groups["002"]
    assert "fr" not in groups["002"]


# --- render_lang_switcher tests ---


def test_render_lang_switcher() -> None:
    html: str = build.render_lang_switcher(
        "en", ["en", "fr", "nl"], lambda lang: f"../{lang}/"
    )
    assert "<span>en</span>" in html
    assert '<a href="../fr/">fr</a>' in html
    assert '<a href="../nl/">nl</a>' in html
    assert "lang-switcher" in html


# --- Integration tests ---


def test_build_creates_index_and_post_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
    )

    build.build_site()

    assert (build_dir / "en" / "index.html").exists()
    assert (build_dir / "en" / "first" / "index.html").exists()
    assert (build_dir / "en" / "second" / "index.html").exists()
    assert (build_dir / "style.css").exists()


def test_build_index_lists_posts_newest_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
        template_text="$lang $lang_switcher $description $content",
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    position_new: int = index_html.index("Test Post")
    position_old: int = index_html.index("Earlier Post")
    assert position_new < position_old


def test_build_post_page_contains_content(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $title $description $content",
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "Test Post" in post_html
    assert "<strong>test</strong>" in post_html


def test_build_cleans_previous_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $description $content",
    )
    build_dir.mkdir()
    stale_file: Path = build_dir / "stale.html"
    stale_file.write_text("old")

    build.build_site()

    assert not stale_file.exists()


def test_build_multilang_creates_per_lang_dirs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    assert (build_dir / "en" / "hello" / "index.html").exists()
    assert (build_dir / "fr" / "bonjour" / "index.html").exists()
    assert (build_dir / "nl" / "index.html").exists()


def test_build_root_redirect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
    )

    build.build_site()

    root_html: str = (build_dir / "index.html").read_text()
    assert 'url=en/' in root_html
    assert "refresh" in root_html


def test_build_lang_switcher_on_post_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    en_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "<span>en</span>" in en_html
    assert "../../fr/bonjour/" in en_html
    assert "../../nl/hello/" in en_html

    fr_html: str = (build_dir / "fr" / "bonjour" / "index.html").read_text()
    assert "<span>fr</span>" in fr_html
    assert "../../en/hello/" in fr_html
    assert "../../nl/bonjour/" in fr_html


def test_build_lang_switcher_on_index_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<span>en</span>" in index_html
    assert '../fr/' in index_html
    assert '../nl/' in index_html


def test_build_post_page_has_back_link(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $title $description $content",
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert 'class="back-link"' in post_html
    assert 'href="../"' in post_html


def test_build_index_article_structure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$description $content",
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<article>" in index_html
    assert "<time>" in index_html
    assert 'href="hello/">' in index_html


def test_build_html_lang_attribute(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.fr.md": SAMPLE_POST_FR},
        template_text='<html lang="$lang">$lang_switcher $title $description $content $root</html>',
    )

    build.build_site()

    fr_html: str = (build_dir / "fr" / "hello" / "index.html").read_text()
    assert 'lang="fr"' in fr_html


def test_build_index_shows_excerpt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$description $content",
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert '<p class="excerpt">A short test excerpt.</p>' in index_html


def test_build_post_page_has_meta_description(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text='<meta name="description" content="$description">$content',
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert '<meta name="description" content="A short test excerpt.">' in post_html

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert '<meta name="description" content="">' in index_html


def test_build_post_meta_description_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    post_no_excerpt: str = """\
---
title: No Excerpt
date: 2026-01-15
---

Some body text without an excerpt field.
"""
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": post_no_excerpt},
        template_text='<meta name="description" content="$description">$content',
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "Some body text without an excerpt field." in post_html
    assert 'content=""' not in post_html


# --- Reading time integration tests ---


def test_build_post_page_shows_reading_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$content",
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "min read" in post_html
    assert 'class="reading-time"' in post_html


def test_build_post_page_shows_localized_reading_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-bonjour.fr.md": SAMPLE_POST_FR},
        template_text="$content",
    )

    build.build_site()

    fr_html: str = (build_dir / "fr" / "bonjour" / "index.html").read_text()
    assert "min de lecture" in fr_html


def test_build_index_shows_reading_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text="$content",
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "min read" in index_html
    assert 'class="reading-time"' in index_html


# --- format_rfc822_date tests ---


def test_format_rfc822_date() -> None:
    result: str = build.format_rfc822_date("2026-02-16")
    assert result == "Mon, 16 Feb 2026 00:00:00 +0000"


# --- render_rss_item tests ---


def test_render_rss_item() -> None:
    post: build.Post = {
        "title": "Test Post",
        "date": "2026-01-15",
        "excerpt": "A test excerpt.",
        "reading_time": 1,
        "post_id": "001",
        "slug": "test-post",
        "lang": "en",
        "html": "<p>Hello <strong>world</strong></p>",
    }
    item: str = build.render_rss_item(post, "en")
    assert "<title>Test Post</title>" in item
    assert f"<link>{build.SITE_URL}/en/test-post/</link>" in item
    assert f"<guid>{build.SITE_URL}/en/test-post/</guid>" in item
    assert "<pubDate>Thu, 15 Jan 2026 00:00:00 +0000</pubDate>" in item
    assert "A test excerpt." in item


def test_render_rss_item_escapes_title() -> None:
    post: build.Post = {
        "title": "A <b>Bold</b> & \"Quoted\" Title",
        "date": "2026-01-15",
        "excerpt": "",
        "reading_time": 1,
        "post_id": "001",
        "slug": "bold-title",
        "lang": "en",
        "html": "<p>Content</p>",
    }
    item: str = build.render_rss_item(post, "en")
    assert "A &lt;b&gt;Bold&lt;/b&gt; &amp; &quot;Quoted&quot; Title" in item


# --- build_post_description tests ---


def test_build_post_description_uses_excerpt() -> None:
    post: build.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "My excerpt.",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": "<p>Full content here.</p>",
    }
    assert build.build_post_description(post) == "My excerpt."


def test_build_post_description_fallback_short() -> None:
    post: build.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": "<p>Short content.</p>",
    }
    assert build.build_post_description(post) == "Short content."


def test_build_post_description_fallback_truncates() -> None:
    long_text: str = "A" * 300
    post: build.Post = {
        "title": "T", "date": "2026-01-01", "excerpt": "",
        "reading_time": 1, "post_id": "001", "slug": "t", "lang": "en",
        "html": f"<p>{long_text}</p>",
    }
    result: str = build.build_post_description(post)
    assert result == "A" * 200 + "..."
    assert len(result) == 203


# --- RSS feed integration tests ---


def test_build_creates_rss_feeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    assert (build_dir / "en" / "feed.xml").exists()
    assert (build_dir / "fr" / "feed.xml").exists()
    assert (build_dir / "nl" / "feed.xml").exists()


def test_rss_feed_contains_posts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
    )

    build.build_site()

    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert 'version="2.0"' in feed
    assert "<language>en</language>" in feed
    assert "<title>Test Post</title>" in feed


def test_rss_feed_only_contains_lang_posts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST, "001-bonjour.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    en_feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "Test Post" in en_feed
    assert "Article de Test" not in en_feed

    fr_feed: str = (build_dir / "fr" / "feed.xml").read_text()
    assert "Article de Test" in fr_feed
    assert "Test Post" not in fr_feed


def test_rss_feed_posts_sorted_newest_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-first.en.md": SAMPLE_POST, "002-second.en.md": SAMPLE_POST_2},
    )

    build.build_site()

    feed: str = (build_dir / "en" / "feed.xml").read_text()
    pos_new: int = feed.index("Test Post")
    pos_old: int = feed.index("Earlier Post")
    assert pos_new < pos_old


def test_rss_feed_uses_excerpt_as_description(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
    )

    build.build_site()

    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "A short test excerpt." in feed
    assert "&lt;p&gt;" not in feed


def test_rss_feed_truncates_without_excerpt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    long_body: str = "word " * 100
    post_no_excerpt: str = f"""\
---
title: Long Post
date: 2026-01-15
---

{long_body}
"""
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-long.en.md": post_no_excerpt},
    )

    build.build_site()

    feed: str = (build_dir / "en" / "feed.xml").read_text()
    assert "..." in feed


def test_rss_discovery_link_in_html(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"001-hello.en.md": SAMPLE_POST},
        template_text=(
            '<link rel="stylesheet" href="$root/style.css">'
            '<link rel="alternate" type="application/rss+xml"'
            ' title="$title - RSS" href="$root/$lang/feed.xml">'
            "$lang_switcher $description $content"
        ),
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert 'type="application/rss+xml"' in index_html
    assert "../en/feed.xml" in index_html

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "../../en/feed.xml" in post_html
