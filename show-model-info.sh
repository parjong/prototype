#!/bin/bash

MODEL_NAME="$1"
MODEL_TAG="$2"

ollama show --modelfile "$MODEL_NAME:$MODEL_TAG" | tee "models/${MODEL_NAME}-${MODEL_TAG}"
