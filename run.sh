#!/bin/bash

CASE_NAME="$1"
MODEL_NAME="$2"
MODEL_TAG="$3"

RESPONSE_PATH="$CASE_NAME/$MODEL_NAME-$MODEL_TAG.response"

mkdir -p "$CASE_NAME"
(
  for IDX in 0 1 2 3 4; do
    echo "$IDX"
    cat "$CASE_NAME/0.prompt" | ollama.exe run "$MODEL_NAME:$MODEL_TAG" --hidethinking
    echo "$IDX - END"
  done
) | tee "$RESPONSE_PATH"
