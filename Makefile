.PHONY: venv build serve clean test

venv: requirements.txt
	python3 -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip; pip install -r requirements.txt

build: venv
	. .venv/bin/activate; python3 src/build.py

serve: build
	cd build && python3 -m http.server 8000

test: venv
	. .venv/bin/activate; pytest src/test_build.py -v

clean:
	rm -rf build .venv
