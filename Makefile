all:

sync:
	git add -u
	git commit --amend --no-edit --quiet
	git push --force
