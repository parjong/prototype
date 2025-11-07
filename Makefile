.PHONY: all run sync

all:

run:
	./run.sh 0.ray_core.function
	./run.sh 1.ray_core.actor

sync:
	git add -u
	git commit --amend --no-edit
	git push --force
