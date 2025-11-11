BUILD_DIR="build"

all:
	rm -rf $(BUILD_DIR)
	cmake -B $(BUILD_DIR) -S .
	cmake --build $(BUILD_DIR)

run-serena-project-index:
	# https://oraios.github.io/serena/02-usage/040_workflow.html#indexing
	uvx --from git+https://github.com/oraios/serena@v0.1.4 serena project index
