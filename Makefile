all:
	uv run python example.py
	# uv run --reinstall-package sample python example.py

sync:
	git add -u
	git commit --amend --no-edit
	git push --force

build-wheel:
	rm -rf dist
	uv build --wheel -p 3.8
	uv build --wheel -p 3.9
