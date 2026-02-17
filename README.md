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

Create a Markdown file in `posts/` named `{prefix}-{slug}.{lang}.md` where `{prefix}` is a numeric ID linking translations together, `{slug}` is the URL-friendly name, and `{lang}` is one of `en`, `fr`, or `nl`:

```markdown
---
title: My Post Title
date: 2026-02-16
excerpt: A short summary shown on the index page and used for SEO.
---

Your content here.
```

The `excerpt` field is optional. When provided, it appears below the post title on the index page and is used as the `<meta name="description">` tag on the post page. When no excerpt is set, the meta description falls back to the first 200 characters of the post body.

An estimated reading time is automatically calculated from the post word count (200 words per minute) and displayed alongside the date on both post and index pages, localized per language.

For example, `001-hello-world.en.md` produces the URL `/en/hello-world/`. To add a French translation with its own SEO-friendly slug, create `001-bonjour-le-monde.fr.md` (same prefix `001` links the translations). The French version will be served at `/fr/bonjour-le-monde/`.

The site builds a per-language index at `/{lang}/` and a root page that redirects to `/en/`. A language switcher appears on every page, linking to the correct per-language slug for each translation.

## RSS feeds

Each language has an RSS 2.0 feed at `/{lang}/feed.xml` (e.g. `/en/feed.xml`). All HTML pages include an RSS autodiscovery `<link>` tag so feed readers can find the feed automatically.

The feed URLs use the `SITE_URL` constant in `build.py` (currently `https://example.com`). Update it to your actual domain before deploying.

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
