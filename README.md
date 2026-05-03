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

If a translation is missing for a post, the build prints a warning to stderr (the build still succeeds), and the language switcher renders the missing language as a strikethrough link pointing to the current page so the reader does not get a 404.

## RSS feeds

Each language has an RSS 2.0 feed at `/{lang}/feed.xml` (e.g. `/en/feed.xml`). All HTML pages include an RSS autodiscovery `<link>` tag so feed readers can find the feed automatically.

The feed URLs use the `site_url` value in `config/config.yml` (currently `https://example.com`). Update it to your actual domain before deploying.

Run `make build` to generate the static site in `build/`.

## Configuration

All blog settings live in `config/config.yml`. The file is split into four documented sections:

- `general`: site title, site URL, posts directory, build directory.
- `languages`: list of language codes plus localized labels for reading time and the back link.
- `publish`: timezone and default publish hour used for RSS dates.
- `theme`: theme directory and the names of the template and stylesheet inside it.

All fields are mandatory. The build aborts with an explanatory error if any field is missing or invalid (for example, a missing label for a declared language, or an unknown timezone).

To use a different configuration file, pass it via `--config`:

```sh
python3 src/build.py --config path/to/your-config.yml
```

## Project structure

```
src/
  build.py        Static site generator
  config.py       Configuration loader and validator
  test_build.py   Unit tests for the generator
  test_config.py  Unit tests for the configuration loader
config/
  config.yml      Blog configuration (site, languages, publish, theme)
theme/
  template.html   HTML page template
  style.css       Stylesheet
posts/            Markdown source files
```
