#!/bin/bash

(
  uv run python $1.py
) 2>&1 | tee $1.log
