# AGENTS.md

Compact orientation for AI agents. See `CLAUDE.md` for the longer narrative; this file lists only what an agent is likely to get wrong without help.

## Commands

- `make build` / `make test` / `make lint` / `make serve` / `make clean` — all auto-create the venv from `requirements.txt`.
- `make lint` runs `flake8` (config in `.flake8`, max line 100), `mypy --strict` (config in `pyproject.toml`), and `bandit` (excludes test files via `pyproject.toml`). All three must pass clean — no `# noqa`, no `# type: ignore`, no `# nosec`.
- The Makefile picks `.venv_docker` when `/.dockerenv` exists, else `.venv_local`. Do not assume a single `.venv/` path.
- `pytest`, `python`, etc. are **not** on the global PATH. Either use `make test` or activate the appropriate venv first (`. .venv_docker/bin/activate`).
- Run a single test: `. .venv_docker/bin/activate && pytest src/test_builder.py::test_name -v`.
- CLI entrypoint: `python3 src/main.py [--config path/to/config.yml]`.

## Layout quirks

- Tests live **next to** the code in `src/` (`src/test_builder.py`, `src/test_config.py`), not under `tests/`. `pyproject.toml` sets `pythonpath = ["src"]` so imports are flat (`from builder import ...`).
- `pyproject.toml` is config-only (pytest + pyright). There is no package metadata; dependencies are in `requirements.txt`.
- Runtime config lives in `config/config.yml`. Every field is mandatory; the loader aborts on missing/invalid fields. When adding features, extend `src/config.py` validation and `test_config.py` together.
- Static assets: `theme/template.html` (uses `$title`, `$lang`, `$lang_switcher`, `$description`, `$content`, `$root` placeholders), `theme/style.css`, `seo/robots.txt`.
- `build/` is wiped on every build — never store source there.

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
- Per-task definition of done: code → tests in `src/test_*.py` → `make test` green → `make lint` green → update `README.md` (humans) → update `CLAUDE.md` if agent-relevant → append entry in `CHANGELOG.md` referencing the task → commit → move task file from `.tasks/todo` to `.tasks/done`.
- **One commit per task.** Use `git commit --amend` to keep it that way; never bundle two tasks.
- If blocked in autonomous mode: write your analysis/questions into the task file, move it to `.tasks/analysed/`, proceed to the next todo.

## Other gotchas

- RSS dates use `publish.default_timezone` (default `Europe/Brussels`) with DST handled via `zoneinfo`; `tzdata` is in `requirements.txt` for non-glibc systems.
- Root `build/index.html` is a redirect to `/en/`; per-language indexes live at `build/{lang}/index.html`.
- `seo/robots.txt` is copied verbatim; the build appends a `Sitemap:` directive only if absent.
