---
title: Getting started
date: 2026-05-05
excerpt: Pureblog is a static, minimalist blog engine with the best multilingual content management. Discover the basics of Pureblog in this overview. You will learn how to install, configure and use your first Pureblog-based website, as well as deploy it to a web server.
---

## What is Pureblog?

Pureblog is a static, minimalist blog engine with enhanced support for content written in multiple languages. Pureblog converts content written in Markdown into a static website.

It has no trackers and not a single line of JavaScript. The design is intentionally minimalist. By design, Pureblog is extremely fast and requires very few system resources to host your blog, even with high traffic.

**The only thing that really matters is your content.**

## Preparing your own Pureblog repository

To start building your own Pureblog, all you need to do is _fork_ the main Pureblog repository.

To do so:

1. Sign in with your GitHub account at <https://github.com/ostaquet/pureblog>
2. Click the **Fork** button at the top right.
3. Choose a repository name (for example: `my-pureblog` with `ostaquet` as the owner).
4. Click **Create fork**.
5. Copy the GitHub URL of your repository (for example `https://github.com/ostaquet/my-pureblog`).

You now have a Pureblog repository in your GitHub space.

## Setting up the environment

Make sure you have what you need to use Pureblog on your machine. Specifically, you need Git, Python 3.13+ and Make.

Open a terminal to make sure Git, Python and Make are installed with the following commands:

```
git --version
python3 --version
make --version
```

If the programs are properly installed, you should see the version currently installed on your machine. If you get an error message, you need to install the missing programs.

Clone your repository locally with the command:

```
git clone https://github.com/<owner>/<repository-name>
```

In our example, that would be `git clone https://github.com/ostaquet/my-pureblog`.

You now have a local clone; all that's left is to start the test Pureblog.

Go to the folder containing the clone of your repository:

```
cd <repository-name>
```

In our example, that's `cd my-pureblog`.

Start the service locally:

```
make serve
```

The system will install the dependencies and trigger a build of the Pureblog you are currently reading.

You can now go to <http://localhost:8000> to browse the Pureblog running on your computer.

## Usage and configuration

There are a few things to know about your Pureblog.

The configuration is in the `config/config.yml` file. The file is well documented to help you tailor the configuration to your needs.

All fields are mandatory. The build aborts with an explanatory error if a field is missing or invalid (for example, a missing translation for a declared language, or an unknown timezone).

To use a different configuration file, pass it via `--config`:

```
python3 src/main.py --config path/to/your-config.yml
```

You can also use the following command to build your Pureblog with the default configuration file `config/config.yml`:

```
make build
```

Or run the build together with an HTTP server to preview the result at <http://localhost:8000>:

```
make serve
```

### Sections of the configuration file

The `config/config.yml` file is organised into five sections, all of which are mandatory:

- `general`: site title, site URL, author (shown in the footer as `© {author} {year}`), posts directory, output directory and static assets directory.
- `seo`: path to the source `robots.txt` file.
- `languages`: list of language codes and localised labels (reading time, back link).
- `publish`: timezone and default publish hour, used for RSS feed dates.
- `theme`: paths to the HTML template and the CSS stylesheet, plus `favicon_emoji` (a single emoji, e.g. `📝`, which is converted into SVG and exposed at `/favicon.svg`).

By default, blog posts live in `posts/`. Posts are Markdown files (`.md`). The filename has the form `<id>-<slug>.<lang>.md`. The `id` identifier links together the same page written in different languages. The `slug` is the URL that will be used. The language is the 2-character ISO code (`lang`).

Static assets (images, etc.) live in the directory configured by `general.assets_dir` (default: `assets/`). The whole directory is copied verbatim into `build/assets/` on every build, so internal images can be referenced from posts using their relative path.

Feel free to read the article on [writing a new post](posts/002-write-a-new-post.en.md) to get familiar with Pureblog.

⚠️ **Important** ⚠️: While you are writing your posts, they are not refreshed automatically in the browser. Posts are generated as static HTML, so you have to re-run `make build` or `make serve` to regenerate them after a change.

To start from a clean build, you can delete the output folder with `make clean`.

## Publishing your Pureblog online

Your Pureblog is ready to be published in the `build/` directory. When you copy this content to a web server, you can immediately browse your pages.

The output directory of the generated site is configurable in the configuration file (`general.build_dir`).

⚠️ **Before deployment**, change `general.site_url` in `config/config.yml` so that it points to your real domain name. This URL is used in RSS feeds and the sitemap: if it is incorrect, the absolute links on your site will point to the wrong domain.
