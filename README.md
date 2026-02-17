# Olivier's Blog

A minimal static blog engine that converts Markdown posts to HTML.

## Quick start

```sh
make build    # Build the site (creates venv automatically)
make serve    # Build and start a local server on port 8000
make test     # Run the unit tests
make clean    # Remove the build directory and virtual environments
```

## Writing posts

Create a Markdown file in `posts/` named `{slug}.{lang}.md` where `{lang}` is one of `en`, `fr`, or `nl`:

```markdown
---
title: My Post Title
date: 2026-02-16
---

Your content here.
```

For example, `hello-world.en.md` produces the URL `/en/hello-world/`. To add a French translation, create `hello-world.fr.md`.

The site builds a per-language index at `/{lang}/` and a root page that redirects to `/en/`. A language switcher appears on every page, linking to available translations.

Run `make build` to generate the static site in `build/`.

## Project structure

```
src/
  build.py        Static site generator
  template.html   HTML page template
  style.css       Stylesheet
  test_build.py   Unit tests
posts/            Markdown source files
```
