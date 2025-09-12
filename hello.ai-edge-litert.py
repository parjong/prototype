#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["ai-edge-litert"]
# ///
#
# Reference
# - https://ai.google.dev/edge/litert/inference
import platform

import ai_edge_litert
from ai_edge_litert.interpreter import Interpreter
import numpy as np

print(platform.python_version())
print(np.__version__)
print(ai_edge_litert.__version__)

interpreter = Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)
