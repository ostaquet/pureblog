"""Unit tests for the Markdown parser."""

from markdown_parser import render_markdown


# --- Headers ---


def test_header_h1() -> None:
    assert "<h1>Title</h1>" in render_markdown("# Title")


def test_header_h2() -> None:
    assert "<h2>Title</h2>" in render_markdown("## Title")


def test_header_h3() -> None:
    assert "<h3>Title</h3>" in render_markdown("### Title")


def test_header_h4() -> None:
    assert "<h4>Title</h4>" in render_markdown("#### Title")


# --- Emphasis ---


def test_bold_with_asterisks() -> None:
    assert "<strong>bold</strong>" in render_markdown("This is **bold**.")


def test_italic_with_underscores() -> None:
    assert "<em>italic</em>" in render_markdown("This is _italic_.")


def test_italic_with_asterisks() -> None:
    assert "<em>italic</em>" in render_markdown("This is *italic*.")


def test_strikethrough() -> None:
    assert "<del>old</del>" in render_markdown("This is ~~old~~ text.")


def test_strikethrough_in_inline_code_is_preserved() -> None:
    html: str = render_markdown("Use `~~text~~` literally.")
    assert "<code>~~text~~</code>" in html
    assert "<del>" not in html


def test_strikethrough_in_fenced_code_is_preserved() -> None:
    md: str = "```\n~~not strikethrough~~\n```"
    html: str = render_markdown(md)
    assert "~~not strikethrough~~" in html
    assert "<del>" not in html


# --- Lists ---


def test_unordered_list() -> None:
    html: str = render_markdown("- one\n- two\n- three\n")
    assert "<ul>" in html
    assert "<li>one</li>" in html
    assert "<li>two</li>" in html
    assert "<li>three</li>" in html


def test_ordered_list() -> None:
    html: str = render_markdown("1. one\n2. two\n3. three\n")
    assert "<ol>" in html
    assert "<li>one</li>" in html
    assert "<li>two</li>" in html
    assert "<li>three</li>" in html


# --- Blockquote ---


def test_blockquote() -> None:
    html: str = render_markdown("> A wise quote.")
    assert "<blockquote>" in html
    assert "A wise quote." in html


# --- Code ---


def test_inline_code() -> None:
    assert "<code>x = 1</code>" in render_markdown("Set `x = 1` here.")


def test_fenced_code_block() -> None:
    md: str = "```\nline1\nline2\n```"
    html: str = render_markdown(md)
    assert "<pre>" in html
    assert "<code>" in html
    assert "line1" in html
    assert "line2" in html


# --- Paragraphs ---


def test_plain_paragraph() -> None:
    assert "<p>Just a paragraph.</p>" in render_markdown("Just a paragraph.")
