# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Estimated reading time displayed on post pages and index pages, localized for en/fr/nl ([.claude/tasks/todo/0010-add-estimated-reading-time.md])
- Post excerpts displayed on index page and as `<meta name="description">` for SEO ([.claude/tasks/todo/0009-add-excerpt.md])
- Clean editorial blog design with Lora serif web font ([.claude/tasks/done/0008-improve-blog-design.md])
- "Back" navigation link on post pages ([.claude/tasks/done/0008-improve-blog-design.md])

### Changed

- Redesigned CSS with editorial typography, refined color palette (`#1a1a1a` text, `#2c5282` accent), improved spacing and layout ([.claude/tasks/done/0008-improve-blog-design.md])
- Language switcher styled with uppercase labels and active language emphasis ([.claude/tasks/done/0008-improve-blog-design.md])
- Index page articles now display date above title for cleaner visual hierarchy ([.claude/tasks/done/0008-improve-blog-design.md])
- Code blocks and blockquotes refined with subtle backgrounds and borders ([.claude/tasks/done/0008-improve-blog-design.md])

### Added

- Multi-language support for English (`en`), French (`fr`), and Dutch (`nl`) ([.claude/tasks/done/0006-multi-language-support.md])
- Language switcher navigation on all pages ([.claude/tasks/done/0006-multi-language-support.md])
- Root redirect from `/` to `/en/` ([.claude/tasks/done/0006-multi-language-support.md])
- Per-language URL structure: `/{lang}/{slug}/` ([.claude/tasks/done/0006-multi-language-support.md])
- Per-language SEO-friendly slugs via numeric filename prefix ([.claude/tasks/todo/0007-improve-multi-language-seo.md])

### Changed

- Post filenames now use `{prefix}-{slug}.{lang}.md` convention with numeric prefix linking translations (e.g. `001-hello-world.en.md` and `001-bonjour-le-monde.fr.md`) ([.claude/tasks/todo/0007-improve-multi-language-seo.md])
- Language switcher on post pages links to the correct per-language slug for each translation ([.claude/tasks/todo/0007-improve-multi-language-seo.md])
- `build.py` decomposed into smaller functions: `prepare_build_dir`, `load_posts`, `build_lang`, `build_post_pages`, `build_index_page`, `build_root_redirect` ([.claude/tasks/done/0006-multi-language-support.md])
- Template uses `$lang` and `$lang_switcher` placeholders ([.claude/tasks/done/0006-multi-language-support.md])

## [Previous]

### Added

- Minimal blog engine: Python build script converting Markdown posts to static HTML ([.claude/tasks/done/0000-base-of-the-blog.md]))
- Single HTML template with clean URL structure (`/post-slug/`) ([.claude/tasks/done/0000-base-of-the-blog.md])
- Minimal CSS stylesheet with responsive design ([.claude/tasks/done/0000-base-of-the-blog.md])
- Makefile with `install`, `build`, `serve`, and `clean` targets ([.claude/tasks/done/0000-base-of-the-blog.md])
- Sample "Hello World" post demonstrating frontmatter format ([.claude/tasks/done/0000-base-of-the-blog.md])
- Separate Python virtual environments for Docker (`.venv_docker`) and local (`.venv_local`) to avoid cross-architecture conflicts ([.claude/tasks/done/0004-improve-makefile.md])

### Changed

- Added explicit type annotations to all functions and variables in `build.py` and `test_build.py` ([.claude/tasks/done/0005-clean-code-and-lint.md])
- Introduced `Post` TypedDict for type-safe post data ([.claude/tasks/done/0005-clean-code-and-lint.md])
- Renamed `build()` to `build_site()` for verb-based function naming ([.claude/tasks/done/0005-clean-code-and-lint.md])
- Added `types-Markdown` and `types-PyYAML` stubs for Pylance compatibility ([.claude/tasks/done/0005-clean-code-and-lint.md])
- Added Pyright `extraPaths` config in `pyproject.toml` for Pylance import resolution ([.claude/tasks/done/0005-clean-code-and-lint.md])
