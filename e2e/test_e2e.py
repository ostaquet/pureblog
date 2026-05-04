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
    expect(page).to_have_title("Olivier's Blog")
    titles: list[str] = page.locator("main article a").all_inner_texts()
    assert titles == ["Yolo", "Hello World", "Other post"], titles


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


def test_robots_txt_advertises_sitemap() -> None:
    response = requests.get(f"{BASE_URL}/robots.txt", timeout=5)
    assert response.status_code == 200
    assert "Sitemap:" in response.text
