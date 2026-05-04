# Pureblog : Developer's README

## Developer's Toolset

Pureblog is written in Python 3.13+. There are plenty of scripts to ease your life based on Make.

At the root of the project, you will find some useful Make targets:

```sh
make build    # Build the site (creates venv automatically)
make serve    # Build and start a local server on port 8000
make test     # Run the unit tests
make lint     # Run flake8, mypy (strict), and bandit on src/
make e2e      # Build a Docker image and run Playwright end-to-end tests
make clean    # Remove the build directory and virtual environments
```

## Tests and quality

### Linter and SAST

### Unit tests

### End-to-end tests

`make e2e` runs the end-to-end tests with Playwright (see `e2e/`)

1. It builds a Docker image based on the official Playwright Python image.
2. It produces the static test site inside the container.
3. It serves it on port 8000.
4. It runs the Playwright test suite defined in `e2e/test_e2e.py` against it.

The objective of the E2E tests is to ensure that the overal functionning of the application is working correctly. All specific cases are handled in the unit tests.

This target requires a working Docker daemon. It runs in a container to have a fully clean environment and ensure that the end users have no issues to build their website.

Unit tests (`make test`) do not depend on Docker and remain the fast feedback loop for development.

## FAQ

### Why unit tests lives next to the code in `src/`?

It's an application, not a library. Nothing is published to PyPI, so _don't ship tests in the wheel_ doesn't apply.

`pyproject.toml` already sets `pythonpath = ["src"]` and the modules are flat (`from builder import ...`). Tests next to code make those imports trivial.

There is no single Python standard. Both layouts are idiomatic and defended by serious projects. The packaging community has a mild preference for a separate `tests/` folder, but only when paired with a `src/` layout that contains a real installable package — which is not the case here.
