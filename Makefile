.PHONY: build serve clean install

install:
	pip install --break-system-packages markdown pyyaml

build:
	python3 build.py

serve: build
	cd build && python3 -m http.server 8000

clean:
	rm -rf build
