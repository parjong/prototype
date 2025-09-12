# prototype
For fast prototyping!

```
$ uv run --python 3.9 hello.tflite-runtime.py
...
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.0.2 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.
...
```

```
$ uv run --python 3.8 --script ./hello.ai-edge-litert.py
  × No solution found when resolving script dependencies:
  ╰─▶ Because all versions of ai-edge-litert have no wheels with a matching Python implementation tag (e.g., `cp38`) and you require ai-edge-litert, we can conclude that your requirements are unsatisfiable.

      hint: Pre-releases are available for `ai-edge-litert` in the requested range (e.g., 2.0.2a1), but pre-releases weren't enabled (try: `--prerelease=allow`)

      hint: You require CPython 3.8 (`cp38`), but we only found wheels for `ai-edge-litert` (v1.4.0) with the following Python implementation tags: `cp39`, `cp310`, `cp311`, `cp312`
```
