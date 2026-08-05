all:

compile:
	g++ -static -o sample.out sample.cpp

sync:
	git add -u
	git commit --amend --quiet --no-edit
	git push --force
