# AGENTS.md

Compact orientation for AI agents. This file lists what an agent is likely to get wrong without help; for developer-facing prose see the docs under `docs/`; for users-facing prose see the docs under `posts/`.

## Commands

- `make build` / `make test` / `make lint` / `make serve` / `make clean` — all auto-create the venv from `requirements.txt`.
- `make e2e` builds `e2e/Dockerfile` (Playwright Python image) and runs `e2e/test_e2e.py` against the served site. Requires a working Docker daemon; not part of `make test`.
- `make lint` runs `flake8` (config in `.flake8`, max line 100), `mypy --strict` (config in `pyproject.toml`), and `bandit` (excludes test files via `pyproject.toml`). All three must pass clean — no `# noqa`, no `# type: ignore`, no `# nosec`.
- The Makefile picks `.venv_docker` when `/.dockerenv` exists, else `.venv_local`. Do not assume a single `.venv/` path.
- `pytest`, `python`, etc. are **not** on the global PATH. Either use `make test` or activate the appropriate venv first (`. .venv_docker/bin/activate`).
- Run a single test: `. .venv_docker/bin/activate && pytest src/test_builder.py::test_name -v`.
- CLI entrypoint: `python3 src/main.py [--config path/to/config.yml]`.

## Layout quirks

- Tests live **next to** the code in `src/` (`src/test_builder.py`, `src/test_config.py`), not under `tests/`. `pyproject.toml` sets `pythonpath = ["src"]` so imports are flat (`from builder import ...`).
- `pyproject.toml` is config-only (pytest + pyright). There is no package metadata; dependencies are in `requirements.txt`.
- Runtime config lives in `config/config.yml`. Every field is mandatory; the loader aborts on missing/invalid fields. When adding features, extend `src/config.py` validation and `test_config.py` together.
- Static assets: `theme/template.html` (uses `$title`, `$lang`, `$lang_switcher`, `$description`, `$content`, `$root`, `$site_title`, `$author`, `$year` placeholders), `theme/style.css`, `seo/robots.txt`. The build also emits `build/favicon.svg` derived from `theme.favicon_emoji`.
- `build/` is wiped on every build — never store source there.

## Documentation layout

`README.md` is a high-level pitch + Quick start only. Detailed prose lives under `docs/`:

- `docs/developers.md` — tooling, tests, quality gates, internal FAQ.
- `CHANGELOG.md` — one entry per task, referencing the task slug.

The documentation for the end users lives directly in the Pureblog under `posts/`. The documentation exists only in French with files `posts/*.fr.md`.

When a task adds or changes a feature, update the doc that **owns** the content rather than bloating `README.md`. Always add a `CHANGELOG.md` entry. If it is related to developement, udpate the `docs/developers.md` documentation. If it is related to a feature for the users, update the documentation under `posts/`.

## Post conventions

- Filename: `{numeric-prefix}-{slug}.{lang}.md`. The numeric prefix links translations across languages; the slug is per-language (SEO). Languages must be listed in `config.yml` `languages.codes` (currently `en`, `fr`, `nl`).
- Frontmatter: `title`, `date` required; `excerpt` optional (falls back to first 200 chars for `<meta description>` and RSS).
- Reading time is computed at build time (200 wpm, min 1).
- Missing translation does not fail the build: a stderr warning is printed and the language switcher renders a strikethrough self-link.

## Code style (enforced expectations)

- Explicit type annotations on every variable/parameter/return. Pylance must be clean — **no `type: ignore`**.
- Functions ≤ 60 lines. Verb names for functions, noun names for variables.
- Prefer clarity over cleverness.

## Task workflow (critical)

- Backlog lives in `.tasks/{todo,done,analysed,ideas}` as Markdown files.
- **Implement only the first `.tasks/todo/*.md` in alphabetical order.** Later todos describe a vision; do not pre-implement them or let them shape the current change.
- Per-task definition of done: code → tests in `src/test_*.py` → `make test` green → `make lint` green → `make e2e` green → update the owning doc under `docs/` and `posts/` → append entry in `CHANGELOG.md` referencing the task → commit → move task file from `.tasks/todo` to `.tasks/done`.
- **One commit per task.** Use `git commit --amend` to keep it that way; never bundle two tasks.
- If blocked in autonomous mode: write your analysis/questions into the task file, move it to `.tasks/analysed/`, proceed to the next todo.

## Other gotchas

- RSS dates use `publish.default_timezone` (default `Europe/Brussels`) with DST handled via `zoneinfo`; `tzdata` is in `requirements.txt` for non-glibc systems.
- Root `build/index.html` is a redirect to `/en/`; per-language indexes live at `build/{lang}/index.html`.
- `seo/robots.txt` is copied verbatim; the build appends a `Sitemap:` directive only if absent.
