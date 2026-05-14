all:

sync:
	git add -u
	git commit --amend --quiet --no-edit
	git push --force
