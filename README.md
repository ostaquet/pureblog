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

Create a Markdown file in `posts/` with YAML frontmatter:

```markdown
---
title: My Post Title
date: 2026-02-16
---

Your content here.
```

The URL of a post is the filename of the Markdown file (without the `.md` extension).

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
