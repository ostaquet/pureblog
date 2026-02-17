"""Unit tests for the blog build engine."""

from pathlib import Path

import pytest

import build


SAMPLE_POST: str = """\
---
title: Test Post
date: 2026-01-15
---

This is a **test** post.
"""

SAMPLE_POST_2: str = """\
---
title: Earlier Post
date: 2025-12-01
---

An older post.
"""

SAMPLE_POST_FR: str = """\
---
title: Article de Test
date: 2026-01-15
---

Ceci est un article de **test**.
"""


def _setup_site(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    post_files: dict[str, str],
    template_text: str = "$lang $lang_switcher $title $content $root",
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


# --- Existing tests (updated for multi-language) ---


def test_parse_post(tmp_path: Path) -> None:
    md_file: Path = tmp_path / "test-post.en.md"
    md_file.write_text(SAMPLE_POST)
    result: build.Post = build.parse_post(md_file)
    assert result["title"] == "Test Post"
    assert result["date"] == "2026-01-15"
    assert result["slug"] == "test-post"
    assert result["lang"] == "en"
    assert "<strong>test</strong>" in result["html"]


def test_build_creates_index_and_post_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"first.en.md": SAMPLE_POST, "second.en.md": SAMPLE_POST_2},
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
        {"first.en.md": SAMPLE_POST, "second.en.md": SAMPLE_POST_2},
        template_text="$lang $lang_switcher $content",
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
        {"hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $title $content",
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
        {"hello.en.md": SAMPLE_POST},
        template_text="$lang $lang_switcher $content",
    )
    build_dir.mkdir()
    stale_file: Path = build_dir / "stale.html"
    stale_file.write_text("old")

    build.build_site()

    assert not stale_file.exists()


# --- New tests for multi-language support ---


def test_split_stem_valid() -> None:
    slug: str
    lang: str
    slug, lang = build.split_stem("hello-world.en")
    assert slug == "hello-world"
    assert lang == "en"


def test_split_stem_invalid_no_lang() -> None:
    with pytest.raises(ValueError, match="No language suffix"):
        build.split_stem("no-lang")


def test_split_stem_invalid_unknown_lang() -> None:
    with pytest.raises(ValueError, match="Unknown language"):
        build.split_stem("hello.de")


def test_group_translations() -> None:
    posts: list[build.Post] = [
        {"title": "A", "date": "2026-01-01", "slug": "a", "lang": "en", "html": ""},
        {"title": "A", "date": "2026-01-01", "slug": "a", "lang": "fr", "html": ""},
        {"title": "B", "date": "2026-01-02", "slug": "b", "lang": "en", "html": ""},
    ]
    groups: dict[str, dict[str, build.Post]] = build.group_translations(posts)
    assert "a" in groups
    assert "en" in groups["a"]
    assert "fr" in groups["a"]
    assert "b" in groups
    assert "en" in groups["b"]
    assert "fr" not in groups["b"]


def test_render_lang_switcher() -> None:
    html: str = build.render_lang_switcher(
        "en", ["en", "fr", "nl"], lambda lang: f"../{lang}/"
    )
    assert "<span>en</span>" in html
    assert '<a href="../fr/">fr</a>' in html
    assert '<a href="../nl/">nl</a>' in html
    assert "lang-switcher" in html


def test_build_multilang_creates_per_lang_dirs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"hello.en.md": SAMPLE_POST, "hello.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    assert (build_dir / "en" / "hello" / "index.html").exists()
    assert (build_dir / "fr" / "hello" / "index.html").exists()
    assert (build_dir / "nl" / "index.html").exists()


def test_build_root_redirect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"hello.en.md": SAMPLE_POST},
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
        {"hello.en.md": SAMPLE_POST, "hello.fr.md": SAMPLE_POST_FR},
    )

    build.build_site()

    post_html: str = (build_dir / "en" / "hello" / "index.html").read_text()
    assert "<span>en</span>" in post_html
    assert '../../fr/hello/' in post_html
    assert '../../nl/hello/' in post_html


def test_build_lang_switcher_on_index_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"hello.en.md": SAMPLE_POST},
    )

    build.build_site()

    index_html: str = (build_dir / "en" / "index.html").read_text()
    assert "<span>en</span>" in index_html
    assert '../fr/' in index_html
    assert '../nl/' in index_html


def test_build_html_lang_attribute(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    build_dir: Path = _setup_site(
        tmp_path,
        monkeypatch,
        {"hello.fr.md": SAMPLE_POST_FR},
        template_text='<html lang="$lang">$lang_switcher $title $content $root</html>',
    )

    build.build_site()

    fr_html: str = (build_dir / "fr" / "hello" / "index.html").read_text()
    assert 'lang="fr"' in fr_html
