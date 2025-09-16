all: run-pytest

sync:
	git add -u
	git commit --amend --no-edit
	git push --force

run-pytest:
	uv run pytest
