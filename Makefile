all:

sync:
	git add -u
	git commit --amend --no-edit
	git push --force

generate-model-info:
	./show-model-info.sh qwen3 0.6b
	./show-model-info.sh qwen3 1.7b
	./show-model-info.sh qwen3 4b

run:
	./run.sh case1 qwen3 0.6b
	./run.sh case1 qwen3 1.7b
	./run.sh case1 qwen3 4b
