# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Extended Markdown support for blog posts: headers (`#` to `####`), bold, italic, strikethrough (`~~text~~`), unordered and ordered lists, blockquotes, inline code and fenced code blocks. Markdown-to-HTML conversion now lives in `src/markdown_parser.py` (with dedicated tests in `src/test_markdown_parser.py`) and is documented in `docs/markdown-cheatsheet.md` (_0026-support-extensive-markdown_)
- End-to-end test suite under `e2e/` (Dockerfile based on `mcr.microsoft.com/playwright/python`, entrypoint `e2e/run.sh`, tests in `e2e/test_e2e.py`) covering root redirect, per-language indexes, post rendering, language switching, missing-translation self-link, RSS feeds, sitemap and `robots.txt`. Invoked via `make e2e` and kept separate from `make test` (_0025-add-e2e-tests_)
- Auto-generated `sitemap.xml` listing language indexes and post pages with `lastmod` dates, plus `robots.txt` copied from `seo/robots.txt` with the `Sitemap:` directive injected (_0022-improve-seo_)
- Localized back link on post pages: "Back" (en), "Retour" (fr), "Terug" (nl) (_0018-back-link-localization_)
- Strikethrough for missing-translation links is now applied via the `.missing-translation` CSS class in `theme/style.css` instead of the `<s>` HTML element, making it easier to customize in the theme (_0021-missing-translation-with-css_)
- Add support of agentic tool Opencode (details in `.opencode` with a safe setup as already done for Claude Code)
- Linter and SAST tooling: `flake8`, `mypy --strict`, and `bandit` are now run via `make lint`. Configuration lives in `.flake8` and `pyproject.toml`. `requirements.txt` updated; existing source code adjusted to pass all three checks (_0024-add-python-linter_)

### Changed

- Move theme files (raw template and css) out of source code
- Configuration manager: blog settings now live in `config/config.yml` (general, languages, publish, theme), loaded and validated by `src/config.py`. `build.py` accepts `--config <path>` to point at an alternative file (_0019-config-mgnt_)
- Warning on stderr when a post is missing one or more translations; language switcher renders missing-translation links as strikethrough pointing to the current page (avoids 404s) (_0020-handle-not-translated-post_)
- Split module between `main.py` and `builder.py` to ease the architecture + Refactored unit tests to follow the new module split (CLI in `src/main.py`, generator in `src/builder.py` as `BlogBuilder`); tests live in `src/test_builder.py` and `src/test_config.py` (_0023-refactor-builder-unit-test_)
- Refactor agentic framework: adjust some parts of Claude Code and move `.claude/tasks` to `.tasks` in order to use different tools.

## [1.0.0]

### Added

- RSS feed dates use Europe/Brussels timezone with 13:00 default publish time (_0015-publishing-date-and-hour_)
- Index page shows fallback description (first 200 chars) when no excerpt is set (_0014-fallback-if-excerpt-not-set-on-index_)
- SEO meta description falls back to first 200 characters of post body when no excerpt is set (_0013-fallback-if-excerpt-not-set_)
- RSS feed description uses post excerpt, with fallback to first 200 characters of plain text (_0012-rss-feed-with-excerpt_)
- Per-language RSS 2.0 feeds at `/{lang}/feed.xml` with RSS autodiscovery `<link>` in all HTML pages (_0011-add-rss-feeds_)
- Estimated reading time displayed on post pages and index pages, localized for en/fr/nl (_0010-add-estimated-reading-time_)
- Post excerpts displayed on index page and as `<meta name="description">` for SEO (_0009-add-excerpt_)
- Clean editorial blog design with Lora serif web font (_0008-improve-blog-design_)
- "Back" navigation link on post pages (_0008-improve-blog-design_)
- Multi-language support for English (`en`), French (`fr`), and Dutch (`nl`) (_0006-multi-language-support_)
- Language switcher navigation on all pages (_0006-multi-language-support_)
- Root redirect from `/` to `/en/` (_0006-multi-language-support_)
- Per-language URL structure: `/{lang}/{slug}/` (_0006-multi-language-support_)
- Per-language SEO-friendly slugs via numeric filename prefix (_0007-improve-multi-language-seo_)

### Changed

- Post page layout: h1 title first, then date + reading time in meta div, then content (_0017-improve-design-of-post_)
- Index page layout: title on first line, date and reading time on second, excerpt on third (_0016-improve-design-of-index_)
- Redesigned CSS with editorial typography, refined color palette (`#1a1a1a` text, `#2c5282` accent), improved spacing and layout (_0008-improve-blog-design_)
- Language switcher styled with uppercase labels and active language emphasis (_0008-improve-blog-design_)
- Index page articles now display date above title for cleaner visual hierarchy (_0008-improve-blog-design_)
- Code blocks and blockquotes refined with subtle backgrounds and borders (_0008-improve-blog-design_)
- Post filenames now use `{prefix}-{slug}.{lang}.md` convention with numeric prefix linking translations (e.g. `001-hello-world.en.md` and `001-bonjour-le-monde.fr.md`) (_0007-improve-multi-language-seo_)
- Language switcher on post pages links to the correct per-language slug for each translation (_0007-improve-multi-language-seo_)
- `build.py` decomposed into smaller functions: `prepare_build_dir`, `load_posts`, `build_lang`, `build_post_pages`, `build_index_page`, `build_root_redirect` (_0006-multi-language-support_)
- Template uses `$lang` and `$lang_switcher` placeholders (_0006-multi-language-support_)

## [0.0.1]

### Added

- Minimal blog engine: Python build script converting Markdown posts to static HTML (_0000-base-of-the-blog_)
- Single HTML template with clean URL structure (`/post-slug/`) (_0000-base-of-the-blog_)
- Minimal CSS stylesheet with responsive design (_0000-base-of-the-blog_)
- Makefile with `install`, `build`, `serve`, and `clean` targets (_0000-base-of-the-blog_)
- Sample "Hello World" post demonstrating frontmatter format (_0000-base-of-the-blog_)
- Separate Python virtual environments for Docker (`.venv_docker`) and local (`.venv_local`) to avoid cross-architecture conflicts (_0004-improve-makefile_)

### Changed

- Added explicit type annotations to all functions and variables in `build.py` and `test_build.py` (_0005-clean-code-and-lint_)
- Introduced `Post` TypedDict for type-safe post data (_0005-clean-code-and-lint_)
- Renamed `build()` to `build_site()` for verb-based function naming (_0005-clean-code-and-lint_)
- Added `types-Markdown` and `types-PyYAML` stubs for Pylance compatibility (_0005-clean-code-and-lint_)
- Added Pyright `extraPaths` config in `pyproject.toml` for Pylance import resolution (_0005-clean-code-and-lint_)
