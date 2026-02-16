"""Unit tests for the blog build engine."""

from pathlib import Path
from string import Template

import build


SAMPLE_POST = """\
---
title: Test Post
date: 2026-01-15
---

This is a **test** post.
"""

SAMPLE_POST_2 = """\
---
title: Earlier Post
date: 2025-12-01
---

An older post.
"""


def test_parse_post(tmp_path):
    md_file = tmp_path / "test-post.md"
    md_file.write_text(SAMPLE_POST)
    result = build.parse_post(md_file)
    assert result["title"] == "Test Post"
    assert result["date"] == "2026-01-15"
    assert result["slug"] == "test-post"
    assert "<strong>test</strong>" in result["html"]


def test_build_creates_index_and_post_pages(tmp_path, monkeypatch):
    # Set up source files
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "first.md").write_text(SAMPLE_POST)
    (posts_dir / "second.md").write_text(SAMPLE_POST_2)

    style = tmp_path / "style.css"
    style.write_text("body {}")

    template = tmp_path / "template.html"
    template.write_text("<html>$title $content $root</html>")

    build_dir = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build()

    # Index page exists
    assert (build_dir / "index.html").exists()

    # Post directories exist
    assert (build_dir / "first" / "index.html").exists()
    assert (build_dir / "second" / "index.html").exists()

    # Style copied
    assert (build_dir / "style.css").exists()


def test_build_index_lists_posts_newest_first(tmp_path, monkeypatch):
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "first.md").write_text(SAMPLE_POST)
    (posts_dir / "second.md").write_text(SAMPLE_POST_2)

    style = tmp_path / "style.css"
    style.write_text("body {}")

    template = tmp_path / "template.html"
    template.write_text("$content")

    build_dir = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build()

    index_html = (build_dir / "index.html").read_text()
    # Newest post (Test Post, 2026-01-15) should appear before older one
    pos_new = index_html.index("Test Post")
    pos_old = index_html.index("Earlier Post")
    assert pos_new < pos_old


def test_build_post_page_contains_content(tmp_path, monkeypatch):
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "hello.md").write_text(SAMPLE_POST)

    style = tmp_path / "style.css"
    style.write_text("body {}")

    template = tmp_path / "template.html"
    template.write_text("$title $content")

    build_dir = tmp_path / "build"

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build()

    post_html = (build_dir / "hello" / "index.html").read_text()
    assert "Test Post" in post_html
    assert "<strong>test</strong>" in post_html


def test_build_cleans_previous_build(tmp_path, monkeypatch):
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    (posts_dir / "hello.md").write_text(SAMPLE_POST)

    style = tmp_path / "style.css"
    style.write_text("body {}")

    template = tmp_path / "template.html"
    template.write_text("$content")

    build_dir = tmp_path / "build"
    build_dir.mkdir()
    stale = build_dir / "stale.html"
    stale.write_text("old")

    monkeypatch.setattr(build, "POSTS_DIR", posts_dir)
    monkeypatch.setattr(build, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build, "TEMPLATE_FILE", template)
    monkeypatch.setattr(build, "STYLE_FILE", style)

    build.build()

    assert not stale.exists()
