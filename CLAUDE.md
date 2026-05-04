# Agentic Development Guide for Pureblog

This document providers instructions for AI assistants (like Claude) working on the Pureblog project.

## Project Overview

Pureblog is a minimal static blog engine that converts Markdown posts to HTML with enhanced multilanguage support.

## Design principles

- Explicit typing everywhere: variables, function parameters, return values.
- Pylance must pass without warnings. No `type: ignore` statements allowed.
- Function names are verbs, variable names are nouns.
- Write understandable code, not clever code.
- Functions must be short (max 60 lines).
- `make lint` must be clean: `flake8` (max line 100), `mypy --strict`, and `bandit`. No `# noqa`, no `# type: ignore`, no `# nosec` escape hatches.

## Architecture

Source code lives in the `src/` folder: `main.py` (CLI entrypoint), `builder.py` (`BlogBuilder` class plus parsing helpers), `config.py` (YAML config loader), and the `test_builder.py` / `test_config.py` test files. The HTML template and stylesheet live under `theme/`, the source `robots.txt` lives under `seo/`, and the YAML configuration lives under `config/`. Tests import from `src/` via the `pythonpath` setting in `pyproject.toml`.

### Multi-language support

The blog supports three languages: English (`en`), French (`fr`), and Dutch (`nl`), defined in `languages.codes` of `config/config.yml`. Posts use the naming convention `{prefix}-{slug}.{lang}.md` (e.g. `001-hello-world.en.md`). The numeric prefix links translations together, allowing each language to have its own SEO-friendly slug (e.g. `001-hello-world.en.md` and `001-bonjour-le-monde.fr.md`). The build produces `build/{lang}/{slug}/index.html` per post, `build/{lang}/index.html` per language index, and a root `build/index.html` that redirects to `/en/`. A language switcher nav appears on every page, linking to the correct per-language slug.

Posts support an optional `excerpt` field in YAML frontmatter. When present, it is displayed on the index page below the post title and injected as a `<meta name="description">` tag on the post page for SEO.

Reading time is automatically calculated from the post body word count (200 wpm, minimum 1 minute) and displayed on both post and index pages with localized labels (`READING_TIME_LABELS`).

Per-language RSS 2.0 feeds are generated at `build/{lang}/feed.xml`. The `SITE_URL` constant defines the base URL used in feed links (default: `https://example.com`). All HTML pages include an RSS autodiscovery `<link>` tag. RSS dates use Europe/Brussels timezone (`DEFAULT_TIMEZONE`) with a default publish time of 13:00 (`DEFAULT_PUBLISH_HOUR`), with proper DST handling via `zoneinfo`.

## End-to-end tests

E2E tests live in `e2e/` (outside `src/`) and run inside the Microsoft Playwright Python Docker image. `make e2e` builds the image (which builds the site at image build time), starts `python -m http.server` against `build/` and runs `pytest e2e/test_e2e.py`. They are intentionally separate from `make test` so unit tests stay fast and Docker-free.

## Test-Driven Development

## Tasks & agents

This list of tasks can be found in `.tasks/todo` and `.tasks/done`. Done tasks provide history of my prompts. Todo tasks are the next envisonned steps.

**CRITITCAL** You can always look the vision ahead in written todo tasks, but we NEVER implement anything else that the very next step (first todo tasks, by alphabetic order). Other tasks are informative and may help making future-proof design decisions. If it leads to unecessary complexity, we just forget about them and act as if they were not written at all.

When a tasks involves enhancing the project (typically adding a new feature), a typical list of things to do is :

- Add the feature in the code.
- Add the relevant unit tests for the code.
- Run the unit tests to ensure that everything passes.
- Run the linter to ensure that everything passes.
- Run the end to end tests to ensure that everything passes.
- Document in `README.md` for the humans.
- Potentially update the `CLAUDE.md` for yourself.
- Update the `CHANGELOG.md` with your changes and the task related to the change.
- Commit and mark the task done.

**IMPORTANT** If you block on something and are in autonomous mode, adapt the task with your analysis and questions, move it to `.tasks/analyzed` and move to the next task.

**CRITICAL** Commit everytime you have something stable. You should end up having ONE commit per task. `Use commit --amend` if needed. NEVER have two different tasks commited together.
