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


def test_parse_post(tmp_path: Path) -> None:
    md_file: Path = tmp_path / "test-post.md"
    md_file.write_text(SAMPLE_POST)
    result: build.Post = build.parse_post(md_file)
    assert result["title"] == "Test Post"
    assert result["date"] == "2026-01-15"
    assert result["slug"] == "test-post"
    assert "<strong>test</strong>" in result["html"]


def test_build_creates_index_and_post_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "first.md").write_text(SAMPLE_POST)
    (posts_dir / "second.md").write_text(SAMPLE_POST_2)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text("<html>$title $content $root</html>")

    build_dir: Path = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build_site()

    assert (build_dir / "index.html").exists()
    assert (build_dir / "first" / "index.html").exists()
    assert (build_dir / "second" / "index.html").exists()
    assert (build_dir / "style.css").exists()


def test_build_index_lists_posts_newest_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "first.md").write_text(SAMPLE_POST)
    (posts_dir / "second.md").write_text(SAMPLE_POST_2)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text("$content")

    build_dir: Path = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build_site()

    index_html: str = (build_dir / "index.html").read_text()
    position_new: int = index_html.index("Test Post")
    position_old: int = index_html.index("Earlier Post")
    assert position_new < position_old


def test_build_post_page_contains_content(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "hello.md").write_text(SAMPLE_POST)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text("$title $content")

    build_dir: Path = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build_site()

    post_html: str = (build_dir / "hello" / "index.html").read_text()
    assert "Test Post" in post_html
    assert "<strong>test</strong>" in post_html


def test_build_cleans_previous_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts_dir: Path = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "hello.md").write_text(SAMPLE_POST)

    style: Path = tmp_path / "style.css"
    style.write_text("body {}")

    template: Path = tmp_path / "template.html"
    template.write_text("$content")

    build_dir: Path = tmp_path / "build"
    build_dir.mkdir()
    stale_file: Path = build_dir / "stale.html"
    stale_file.write_text("old")

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build_site()

    assert not stale_file.exists()
