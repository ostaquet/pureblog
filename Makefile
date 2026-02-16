.PHONY: build serve clean test

VENV = venv
BIN = $(VENV)/bin

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(BIN)/pip3 install -r requirements.txt
	touch $(VENV)

build: $(VENV)
	$(BIN)/python3 src/build.py

serve: build
	cd build && python3 -m http.server 8000

test: $(VENV)
	$(BIN)/pytest src/test_build.py -v

clean:
	rm -rf build
