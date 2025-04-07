.PHONY: build serve clean watch

build:
	python3 generator.py

serve:
	python3 server.py

clean:
	rm -rf output/*

watch:
	watchmedo shell-command --patterns="*.md" --recursive --command='make build' content/