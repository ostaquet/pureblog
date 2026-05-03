.PHONY: venv build serve clean test

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

clean:
	rm -rf build $(VENV)
