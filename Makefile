.PHONY: venv build serve clean test lint e2e deploy

E2E_IMAGE = pureblog-e2e

# Detect if we are running inside a Docker or native. The virtual environment
# is different to support the safe-setup mode of Claude Code & OpenCode.
# As the safe-mode runs into Alpine, the libs are potentially differents than the
# native environment (MacOS or Windows).
ifneq (,$(wildcard /.dockerenv))
VENV = .venv_docker
else
VENV = .venv_local
endif


# Prepare the virtual environment and install the required Python libraries with pip
venv: requirements.txt
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; pip install --upgrade pip; pip install -r requirements.txt | grep -v "Requirement already satisfied:" || true

# Build the static HTML
build: venv
	. $(VENV)/bin/activate; python3 src/main.py

# Start a local HTTP server to test the web site
serve: build
	cd build && python3 -m http.server 8000

# Run the unit tests
test: venv
	. $(VENV)/bin/activate; pytest src/ -v

# Run the linter and the SAST
lint: venv
	. $(VENV)/bin/activate; flake8 src/
	. $(VENV)/bin/activate; mypy src/
	. $(VENV)/bin/activate; bandit -q -c pyproject.toml -r src/

# Run the end-to-end tests (inside a Docker container with Playwright)
e2e:
	docker build -f e2e/Dockerfile -t $(E2E_IMAGE) .
	docker run --rm $(E2E_IMAGE)

# Clean the build directory (classic output)
clean:
	rm -rf build $(VENV)

# Deploy on Firebase Hosting
deploy: build
	firebase deploy