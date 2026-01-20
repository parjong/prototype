all: eval sync

eval:
	./eval_and_log examples/SEARCH_DISCUSSION.graphql
	./eval_and_log examples/GET_NODE_TYPE_BY_NUMBER_OF_DISCUSSION.graphql
	./eval_and_log examples/GET_NODE_TYPE_BY_NUMBER_OF_ISSUE.graphql

sync:
	git add -u
	git commit --amend --no-edit
	git push --force
