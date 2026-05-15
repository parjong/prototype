# Agent Guidelines

## Python Usage
- **Direct execution of `python` is prohibited.**
- **Always use `uv` to run Python scripts.**
    - Use `uv run python <script>` to ensure the correct virtual environment and dependencies are used.
- This ensures consistency across different environments and prevents "ModuleNotFoundError" due to missing dependencies in the global Python environment.

## Phase Management
- **Never proceed to the next Phase until all checklists and validation steps of the current Phase in `docs/01.WORK_PLAN.md` are 100% completed and verified.**
- Each phase must end with a validation report (e.g., `docs/reports/*.md`) and user approval.

## Test Report Standards
- **Reproducibility is mandatory.** Every test report must include the exact sequence of commands used to verify the features.
- Commands should be documented in a way that allows them to be copy-pasted (e.g., including `direnv exec . uv run` prefixes if necessary).
- Include both success and failure cases if relevant, along with the environment state (e.g., DB status, model versions).
