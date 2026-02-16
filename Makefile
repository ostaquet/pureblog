.PHONY: build serve clean

VENV = venv
BIN = $(VENV)/bin

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt
	touch $(VENV)

build: $(VENV)
	$(BIN)/python build.py

serve: build
	cd build && python3 -m http.server 8000

clean:
	rm -rf build
