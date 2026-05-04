# Pureblog : User's README

## Writing posts

Create a Markdown file in `posts/` named `{prefix}-{slug}.{lang}.md` where `{prefix}` is a numeric ID linking translations together, `{slug}` is the URL-friendly name, and `{lang}` is one of `en`, `fr`, or `nl`:

```
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

The post body supports the standard Markdown syntax used by Pureblog. The full list with examples is in [`docs/markdown_format.md`](markdown_format.md).

## Images and assets

Static assets (images, etc.) live in the directory configured by `general.assets_dir` (default: `assets/`). The whole directory is copied verbatim into `build/assets/` on every build, so internal images can be referenced from posts using their project-root relative path:

```
![External image](https://i.ibb.co/Vvh17pr/3jxqrKP.jpg)
![Internal image](assets/img/documentation.png)
```

If a referenced internal image cannot be found in `assets_dir`, the build prints a warning but still completes.

Images larger than the article's text column are automatically scaled down to fit. Smaller images keep their natural size. Resizing the browser window reflows them accordingly.

## Languages

The languages are configured in the section `languages` of `config/config.yml`. The `languages.code` must be configured with the `languages.reading_time_labels` and `languages.back_labels`. It allows some localization for the common labels.

The site builds a per-language index at `/{lang}/` and a root page that redirects to `/en/`. A language switcher appears on every page, linking to the correct per-language slug for each translation.

If a translation is missing for a post, the build prints a warning (the build still succeeds), and the language switcher renders the missing language as a strikethrough link pointing to the current page so the reader does not get a 404.

## RSS feeds

Each language has an RSS 2.0 feed at `/{lang}/feed.xml` (e.g. `/en/feed.xml`). All HTML pages include an RSS autodiscovery `<link>` tag so feed readers can find the feed automatically.

The feed URLs use the `site_url` value in `config/config.yml` (currently `https://example.com`). Update it to your actual domain before deploying.

Run `make build` to generate the static site in `build/`.

## SEO: sitemap and robots.txt

The build generates `/sitemap.xml` listing every per-language index and post page (with `<lastmod>` taken from the post date or, for index pages, the most recent post in that language).

The static file `seo/robots.txt` is copied to `/robots.txt` at the root of the build output. The build appends `Sitemap: {site_url}/sitemap.xml` if that directive is not already present, so the source file only needs the rules you care about.

## Configuration

All blog settings live in `config/config.yml`. The file is split into four documented sections:

- `general`: site title, site URL, author, posts directory, build directory, assets directory. The `author` value is shown in the page footer (`© {author} {current-year}`).
- `seo`: path to the source `robots.txt` file.
- `languages`: list of language codes plus localized labels for reading time and the back link.
- `publish`: timezone and default publish hour used for RSS dates.
- `theme`: paths to the template and stylesheet files.

All fields are mandatory. The build aborts with an explanatory error if any field is missing or invalid (for example, a missing label for a declared language, or an unknown timezone).

To use a different configuration file, pass it via `--config`:

```sh
python3 src/main.py --config path/to/your-config.yml
```
