.PHONY: venv build serve clean test lint e2e

E2E_IMAGE = pureblog-e2e

ifneq (,$(wildcard /.dockerenv))
VENV = .venv_docker
else
VENV = .venv_local
endif

venv: requirements.txt
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; pip install --upgrade pip; pip install -r requirements.txt

build: venv
	. $(VENV)/bin/activate; python3 src/main.py

serve: build
	cd build && python3 -m http.server 8000

test: venv
	. $(VENV)/bin/activate; pytest src/ -v

lint: venv
	. $(VENV)/bin/activate; flake8 src/
	. $(VENV)/bin/activate; mypy src/
	. $(VENV)/bin/activate; bandit -q -c pyproject.toml -r src/

e2e:
	docker build -f e2e/Dockerfile -t $(E2E_IMAGE) .
	docker run --rm $(E2E_IMAGE)

clean:
	rm -rf build $(VENV)
