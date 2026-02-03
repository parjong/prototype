all:

run:
	uv run sample.py

sync:
	git add -u
	git commit --amend --no-edit --quiet
	git push --force
