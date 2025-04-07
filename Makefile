.PHONY: build serve clean watch lint

build:
	python3 generator.py

serve:
	python3 server.py

clean:
	rm -rf output/*

watch:
	watchmedo shell-command --patterns="*.md" --recursive --command='make build' content/

lint:
	flake8 generator.py server.py --count --show-source --statistics
	pylint generator.py server.py