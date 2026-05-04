"""End-to-end tests for the Pureblog static site.

These tests are run inside the Playwright Docker image (see e2e/Dockerfile).
They drive a real browser against a local HTTP server serving the freshly
built site and assert that the user-visible behaviour is correct: navigation,
language switching, missing-translation handling, RSS feeds and SEO files.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET

import pytest
import requests
from playwright.sync_api import Page, expect

BASE_URL: str = os.environ.get("E2E_BASE_URL", "http://localhost:8000")


def test_root_redirects_to_english_index(page: Page) -> None:
    page.goto(f"{BASE_URL}/")
    page.wait_for_url(f"{BASE_URL}/en/")
    expect(page).to_have_url(f"{BASE_URL}/en/")


def test_english_index_lists_posts_in_descending_date_order(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/")
    expect(page).to_have_title("Example's Blog")
    titles: list[str] = page.locator("main article a").all_inner_texts()
    assert titles == [
        "Markdown format",
        "Yolo",
        "Hello World",
        "Other post",
    ], titles


def test_post_page_renders_title_and_content(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/hello-world/")
    expect(page).to_have_title("Hello World")
    expect(page.locator("main article h1")).to_have_text("Hello World")
    expect(page.locator("main article")).to_contain_text(
        "Welcome to my blog."
    )
    expect(page.locator(".reading-time")).to_contain_text("min read")


def test_language_switcher_links_to_translated_slug(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/hello-world/")
    fr_link = page.locator("nav.lang-switcher a", has_text="fr")
    expect(fr_link).to_have_attribute("href", "../../fr/bonjour-monde/")
    fr_link.click()
    page.wait_for_url(f"{BASE_URL}/fr/bonjour-monde/")
    expect(page.locator("main article h1")).to_have_text("Bonjour Monde")


def test_missing_translation_is_marked_and_self_links(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/yolo/")
    fr_link = page.locator("nav.lang-switcher a", has_text="fr")
    expect(fr_link).to_have_attribute("class", "missing-translation")
    fr_link.click()
    # Clicking a missing-translation link must not 404; it returns to the
    # current page so the reader stays on a valid URL.
    page.wait_for_url(f"{BASE_URL}/en/yolo/")


def test_back_link_returns_to_language_index(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/hello-world/")
    page.locator("a.back-link").click()
    page.wait_for_url(f"{BASE_URL}/en/")


@pytest.mark.parametrize("lang", ["en", "fr", "nl"])
def test_rss_feed_is_well_formed(lang: str) -> None:
    response = requests.get(f"{BASE_URL}/{lang}/feed.xml", timeout=5)
    assert response.status_code == 200
    root = ET.fromstring(response.text)
    assert root.tag == "rss"
    channel = root.find("channel")
    assert channel is not None
    assert channel.find("title") is not None


def test_sitemap_lists_all_language_indexes() -> None:
    response = requests.get(f"{BASE_URL}/sitemap.xml", timeout=5)
    assert response.status_code == 200
    body: str = response.text
    for lang in ("en", "fr", "nl"):
        assert f"/{lang}/" in body, f"sitemap missing /{lang}/"


def test_markdown_post_renders_headers(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    article = page.locator("main article")
    expect(article.locator("h1", has_text="This is a header 1")).to_have_count(1)
    expect(article.locator("h2", has_text="This is a header 2")).to_have_count(1)
    expect(article.locator("h3", has_text="This is a header 3")).to_have_count(1)
    expect(article.locator("h4", has_text="This is a header 4")).to_have_count(1)


def test_markdown_post_renders_emphasis(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    article = page.locator("main article")
    expect(article.locator("strong")).to_contain_text(
        "This is important text in bold"
    )
    expect(article.locator("em").first).to_contain_text(
        "This is important test in italic"
    )
    expect(article.locator("del")).to_contain_text("This is not a good test")


def test_markdown_post_renders_lists(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    article = page.locator("main article")
    ul_items: list[str] = article.locator("ul > li").all_inner_texts()
    assert any("List 1" in item for item in ul_items)
    assert any("List 2" in item for item in ul_items)
    assert any("List 3" in item for item in ul_items)
    ol_items: list[str] = article.locator("ol > li").all_inner_texts()
    assert ol_items[:3] == ["Item number 1", "Item number 2", "Item number 3"]


def test_markdown_post_renders_inline_and_fenced_code(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    article = page.locator("main article")
    expect(article.locator("ul > li code", has_text="a bit of code")).to_have_count(1)
    pre_code = article.locator("pre code")
    expect(pre_code).to_contain_text("This is clearly some code.")
    expect(pre_code).to_contain_text("Is it important code?")


def test_markdown_post_renders_blockquote(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    expect(page.locator("main article blockquote")).to_contain_text(
        "This is a quote, a very important quote."
    )


def test_post_image_is_served_and_fits_article(page: Page) -> None:
    """Image renders, is reachable, and never overflows the article width."""
    response = requests.get(
        f"{BASE_URL}/assets/img/documentation.png", timeout=5
    )
    assert response.status_code == 200

    page.goto(f"{BASE_URL}/en/markdown-format/")
    img = page.locator("main article img").first
    expect(img).to_have_count(1)

    for viewport_width in (320, 480, 1280):
        page.set_viewport_size({"width": viewport_width, "height": 800})
        article_width: float = page.locator("main article").evaluate(
            "el => el.getBoundingClientRect().width"
        )
        img_width: float = img.evaluate("el => el.getBoundingClientRect().width")
        assert img_width <= article_width + 0.5, (
            f"image width {img_width} exceeds article width {article_width} "
            f"at viewport {viewport_width}"
        )


def test_post_renders_link_variants(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/markdown-format/")
    article = page.locator("main article")

    autolink = article.locator(
        'a[href="http://www.example.com"]',
        has_text="http://www.example.com",
    )
    expect(autolink).to_have_count(1)

    same_tab = article.locator("a", has_text="the docs")
    expect(same_tab).to_have_attribute("href", "http://www.example.com")
    expect(same_tab).not_to_have_attribute("target", "_blank")

    new_tab = article.locator("a", has_text="reference in a new tab")
    expect(new_tab).to_have_attribute("href", "http://www.example.com")
    expect(new_tab).to_have_attribute("target", "_blank")
    expect(new_tab).to_have_attribute("rel", "noopener noreferrer")

    internal = article.locator("a", has_text="Hello World")
    expect(internal).to_have_attribute("href", "../../en/hello-world/")
    internal.click()
    page.wait_for_url(f"{BASE_URL}/en/hello-world/")


def test_header_h1_uses_site_title(page: Page) -> None:
    page.goto(f"{BASE_URL}/en/")
    expect(page.locator("header h1")).to_have_text("Example's Blog")


def test_footer_shows_author_and_year(page: Page) -> None:
    import datetime as _dt

    page.goto(f"{BASE_URL}/en/")
    footer_text: str = page.locator("footer").inner_text()
    assert "John Doe" in footer_text
    assert str(_dt.datetime.now().year) in footer_text


def test_favicon_is_served_and_referenced(page: Page) -> None:
    response = requests.get(f"{BASE_URL}/favicon.svg", timeout=5)
    assert response.status_code == 200
    assert "<svg" in response.text
    assert "📝" in response.text

    page.goto(f"{BASE_URL}/en/")
    favicon_link = page.locator('head link[rel="icon"]')
    expect(favicon_link).to_have_attribute("type", "image/svg+xml")
    expect(favicon_link).to_have_attribute("href", "../favicon.svg")


def test_robots_txt_advertises_sitemap() -> None:
    response = requests.get(f"{BASE_URL}/robots.txt", timeout=5)
    assert response.status_code == 200
    assert "Sitemap:" in response.text
