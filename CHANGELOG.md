# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Minimal blog engine: Python build script converting Markdown posts to static HTML ([.claude/tasks/done/0000-base-of-the-blog.md]))
- Single HTML template with clean URL structure (`/post-slug/`) ([.claude/tasks/done/0000-base-of-the-blog.md])
- Minimal CSS stylesheet with responsive design ([.claude/tasks/done/0000-base-of-the-blog.md])
- Makefile with `install`, `build`, `serve`, and `clean` targets ([.claude/tasks/done/0000-base-of-the-blog.md])
- Sample "Hello World" post demonstrating frontmatter format ([.claude/tasks/done/0000-base-of-the-blog.md])
- Separate Python virtual environments for Docker (`.venv_docker`) and local (`.venv_local`) to avoid cross-architecture conflicts ([.claude/tasks/done/0004-improve-makefile.md])
