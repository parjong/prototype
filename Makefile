all:
	make run-pre-commit | tee ../make.log
	cp ../make.log make.log

run-pre-commit:
	uv --version
	uvx pre-commit run --all-files --config pre-commit-config.yaml

sync:
	git add -u
	git commit --amend --no-edit
	git push --force
