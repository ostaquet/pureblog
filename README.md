# Pureblog : Pure content. Any language.

Pureblog is a minimal static blog engine that converts Markdown posts to static HTML with enhanced multilanguage support.

**No trackers, no javascript and a minimal design. The only thing that matters is your content.**

It is fast and requires very low resources to host a Pureblog.

## Quick start

Installing the dependencies to build your Pureblog:

- Ensure that Python is installed (`python3 --version`). If not, go on https://www.python.org/downloads/.
- Ensure that `pip` is installed (`pip3 --version`). If not, go on https://pip.pypa.io/en/stable/installation/.
- Ensure that `make` is installed (`make --version`). If not installed:
  - Windows: https://gnuwin32.sourceforge.net/packages/make.htm
  - MacOS: `brew install make`
  - Linux: `sudo apt-get install build-essential`

Build the example blog:

- Run `make build` in a Terminal.

Your Pureblog is available in `build/` and can be deployed with a simple copy-paste.

- Run `make serve` in a Terminal to test it right away.

Visit the website on http://localhost:8000

## Important things to know

The configuration is the most important files and it lives in `config/config.yml`. [The example file](config/config.yml) is quite complete and verbose.

For additional information about the configuration, check <https://www.pureblog.dev>.

## Additional documentation

- For the developers, you can find specific informattion on the [developer's README](docs/developers.md).

## Project structure

For users:

```
config/           Blog configuration (general, seo, languages, publish, theme)
seo/              Static files for SEO (like robots rules; build appends Sitemap directive)
theme/            HTML page template and CSS stylesheet
posts/            Markdown source files for the posts (and the documentation of Pureblog in the main repository)
assets/           Static assets (images, etc.) copied verbatim into output folder
build/            Default output folder for the static website (configurable). Ready to host.
```

For developers:

```
src/              Source code and unit tests
docs/             Documentation for developers
e2e/              Playwrigth end-to-end-tests
.claude/          Agentic safe-setup for Claude Code
.opencode/        Agentic safe-setup for Opencode
.tasks/           Structured micro-prompting tasks for agentic development
```
