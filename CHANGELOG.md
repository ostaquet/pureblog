# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added

- RSS feed dates use Europe/Brussels timezone with 13:00 default publish time (*0015-publishing-date-and-hour*)
- Index page shows fallback description (first 200 chars) when no excerpt is set (*0014-fallback-if-excerpt-not-set-on-index*)
- SEO meta description falls back to first 200 characters of post body when no excerpt is set (*0013-fallback-if-excerpt-not-set*)
- RSS feed description uses post excerpt, with fallback to first 200 characters of plain text (*0012-rss-feed-with-excerpt*)
- Per-language RSS 2.0 feeds at `/{lang}/feed.xml` with RSS autodiscovery `<link>` in all HTML pages (*0011-add-rss-feeds*)
- Estimated reading time displayed on post pages and index pages, localized for en/fr/nl (*0010-add-estimated-reading-time*)
- Post excerpts displayed on index page and as `<meta name="description">` for SEO (*0009-add-excerpt*)
- Clean editorial blog design with Lora serif web font (*0008-improve-blog-design*)
- "Back" navigation link on post pages (*0008-improve-blog-design*)
- Multi-language support for English (`en`), French (`fr`), and Dutch (`nl`) (*0006-multi-language-support*)
- Language switcher navigation on all pages (*0006-multi-language-support*)
- Root redirect from `/` to `/en/` (*0006-multi-language-support*)
- Per-language URL structure: `/{lang}/{slug}/` (*0006-multi-language-support*)
- Per-language SEO-friendly slugs via numeric filename prefix (*0007-improve-multi-language-seo*)

### Changed

- Post page layout: h1 title first, then date + reading time in meta div, then content (*0017-improve-design-of-post*)
- Index page layout: title on first line, date and reading time on second, excerpt on third (*0016-improve-design-of-index*)
- Redesigned CSS with editorial typography, refined color palette (`#1a1a1a` text, `#2c5282` accent), improved spacing and layout (*0008-improve-blog-design*)
- Language switcher styled with uppercase labels and active language emphasis (*0008-improve-blog-design*)
- Index page articles now display date above title for cleaner visual hierarchy (*0008-improve-blog-design*)
- Code blocks and blockquotes refined with subtle backgrounds and borders (*0008-improve-blog-design*)
- Post filenames now use `{prefix}-{slug}.{lang}.md` convention with numeric prefix linking translations (e.g. `001-hello-world.en.md` and `001-bonjour-le-monde.fr.md`) (*0007-improve-multi-language-seo*)
- Language switcher on post pages links to the correct per-language slug for each translation (*0007-improve-multi-language-seo*)
- `build.py` decomposed into smaller functions: `prepare_build_dir`, `load_posts`, `build_lang`, `build_post_pages`, `build_index_page`, `build_root_redirect` (*0006-multi-language-support*)
- Template uses `$lang` and `$lang_switcher` placeholders (*0006-multi-language-support*)

## [0.0.1]

### Added

- Minimal blog engine: Python build script converting Markdown posts to static HTML (*0000-base-of-the-blog*)
- Single HTML template with clean URL structure (`/post-slug/`) (*0000-base-of-the-blog*)
- Minimal CSS stylesheet with responsive design (*0000-base-of-the-blog*)
- Makefile with `install`, `build`, `serve`, and `clean` targets (*0000-base-of-the-blog*)
- Sample "Hello World" post demonstrating frontmatter format (*0000-base-of-the-blog*)
- Separate Python virtual environments for Docker (`.venv_docker`) and local (`.venv_local`) to avoid cross-architecture conflicts (*0004-improve-makefile*)

### Changed

- Added explicit type annotations to all functions and variables in `build.py` and `test_build.py` (*0005-clean-code-and-lint*)
- Introduced `Post` TypedDict for type-safe post data (*0005-clean-code-and-lint*)
- Renamed `build()` to `build_site()` for verb-based function naming (*0005-clean-code-and-lint*)
- Added `types-Markdown` and `types-PyYAML` stubs for Pylance compatibility (*0005-clean-code-and-lint*)
- Added Pyright `extraPaths` config in `pyproject.toml` for Pylance import resolution (*0005-clean-code-and-lint*)
