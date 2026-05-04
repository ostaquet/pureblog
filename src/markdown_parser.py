"""Markdown to HTML rendering for blog posts.

Centralizes the conversion of Markdown bodies into HTML so the builder
stays focused on file orchestration. Supported syntax is documented in
`docs/markdown-cheatsheet.md`.
"""

from __future__ import annotations

import markdown
from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor


# A leading empty group is required: SimpleTagInlineProcessor uses
# match group 2 as the tag's inner text.
_STRIKETHROUGH_RE: str = r"()~~(.+?)~~"


class _StrikethroughExtension(Extension):
    """Render ``~~text~~`` as ``<del>text</del>``.

    Registered as an inline processor so it is automatically skipped
    inside inline code spans and fenced code blocks.
    """

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(_STRIKETHROUGH_RE, "del"),
            "pureblog-strikethrough",
            175,
        )


def render_markdown(text: str) -> str:
    """Convert a Markdown body into HTML.

    Supports headers (``#``..``####``), emphasis (``**bold**``,
    ``_italic_``, ``~~strike~~``), unordered and ordered lists,
    blockquotes (``>``), inline code (`` `code` ``) and fenced code
    blocks (``` ``` ```).
    """
    extensions: list[str | Extension] = [
        "fenced_code",
        _StrikethroughExtension(),
    ]
    return markdown.markdown(text, extensions=extensions)
