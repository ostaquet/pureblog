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

## Agentic development

This project supports Claude Code and Opencode for agentic development. Details can be found in the respective directories `.claude` and `.opencode`.

In order to avoid giving all access to the local machine, the project offers safe-setup to run the agents in a sandboxed container. The documentation about the safe-setup is in [.claude/safe-setup/HACKING.md](../.claude/safe-setup/HACKING.md) and in [.opencode/safe-setup/HACKING.md](../.opencode/safe-setup/HACKING.md).

We believe that agentic development must be more structured than solely prompting and hoping for the best. This is why this project uses the concept of **Structured Micro-prompting**. The tasks are described in `.tasks/` folder with a clear status:

- `.tasks/todo`: Tasks to do for the agent under the form `9999-thing-todo.md`.
- `.tasks/done`: Tasks done.
- `.tasks/analysed`: If the task to do is too complex and required analysis.
- `.tasks/ideas`: Ideas of tasks for the future.

When starting the agent in its safe-setup, you can prompt:

- `Read the AGENTS.md`
- `Implement next task`

The agent will follow the workflow of the tasks and iterate to provide code with the expected quality and documentation.

## Tests and quality

### Linter and SAST

The project uses:

- flake8 for code style
- mypy for type checking (strict mode)
- bandit for security checking

`make lint` runs the linters.

### Unit tests

Unit tests are wrtten with `pytest` framework. The unit tests lives next to the source code in `src/`.

`make test` runs the unit tests.

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
