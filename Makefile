all:

model.tflite:
	./make.model.tflite.py

run-hello-tflite-runtime: model.tflite
	uv run --python 3.8 --script hello.tflite-runtime.py

run-hello-ai-edge-litert: model.tflite
	# no pacakage: 3.8
	uv run --python 3.9 hello.ai-edge-litert.py
	uv run --python 3.10 hello.ai-edge-litert.py
	uv run --python 3.11 hello.ai-edge-litert.py
	uv run --python 3.12 hello.ai-edge-litert.py
	# no pacakage: 3.13
