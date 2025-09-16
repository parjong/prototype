all: run-mypy run-app

run-app:
	uv run recipe-design

run-mypy:
	uv run mypy

run-pytest:
	uv run pytest
