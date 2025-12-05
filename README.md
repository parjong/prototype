# prototype
For fast prototyping!

## What?

- Type some ideas into some "Github Issue"
- Trigger Github Actions Workflow via ``issue_comment``
  - e.g. ``hey, alex {PROMPT}``
  - e.g. ``alex, {PROMPT}``
- The workflow convert the main description and all comments into a Chat history

## Probeles to Solve

1. How to test workflows?
   - Espeically workflows with ``issue_comment`` trigger

## References

- LLM Provider
  - Ollama (in use)
    - https://github.com/ollama/ollama-python
  - Gemini (candidate)
    - https://ai.google.dev/gemini-api/docs
- Github Actions
  - https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
  - https://docs.github.com/en/actions/concepts/runners/self-hosted-runners
  - https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners
  - https://docs.github.com/en/actions/reference/runners/self-hosted-runners

### How to Run Linters?

```
uv run pre-commit run -a -c pre-commit-config.yaml
```
