# AI Code Workshop: Broken Orders API

This is a deliberately broken FastAPI project for a short workshop on using AI
to understand, test, debug, and refactor code.

The goal is to finish the core exercises in a half-day session. Work in small
steps: run one test file, ask AI for help, review the answer, change code, and
run the test again.

## What You Need

- Python 3.10 or newer
- Git
- A code editor
- An AI assistant

This repo was tested with Python 3.13.

## Step 1: Get the Code

```bash
git clone https://github.com/kalinbas/ai-code-workshop-buggy-api.git
cd ai-code-workshop-buggy-api
```

## Step 2: Create a Virtual Environment

On macOS or Linux:

```bash
PYTHON=python3.13  # change this to python3.12, python3.11, or python3.10 if needed
$PYTHON -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Keep the virtual environment activated while you work.

## Step 3: Install Dependencies

```bash
python -m pip install -e ".[dev]"
```

## Step 4: Check the Starting Point

```bash
pytest --collect-only
pytest
```

The tests should collect successfully, then several tests should fail. That is
expected. The failures are the workshop.

## Step 5: Do the Three Exercises

Run one exercise at a time:

```bash
pytest tests/test_01_validation.py
pytest tests/test_02_pricing.py
pytest tests/test_03_security.py
```

Use `docs/01_task_cards.md` for the instructions for each exercise.

## Step 6: Use AI in Small Steps

Start with this prompt:

```text
You are helping me work on an unfamiliar FastAPI codebase.
First, inspect the files I provide and summarize:
1. the main responsibilities,
2. likely risks or design smells,
3. the minimum tests I should run before changing anything.
Do not rewrite code yet.
```

For each exercise:

1. Run the test file.
2. Give AI the failing test and relevant code.
3. Ask for possible causes before asking for code.
4. Make one small change.
5. Run the test again.
6. Review the AI suggestion before trusting it.

More prompt examples are in `docs/02_prompt_patterns.md`.

## Optional: Run the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Use these local test tokens:

```text
Authorization: Bearer user-token-1
Authorization: Bearer premium-token-1
Authorization: Bearer admin-token
```

## Useful Make Commands

```bash
make check-setup
make test
make test-baseline
make test-extension
make test-expert
make run
```

If `make check-setup` uses the wrong Python, run:

```bash
make PYTHON=python3.13 check-setup
```

## Extra Workshop Files

- `docs/01_task_cards.md`: exercise instructions
- `docs/02_prompt_patterns.md`: prompts to try
- `docs/prompt_journal_template.md`: worksheet for tracking prompts
- `docs/ai_patch_review_lab.md`: checklist for reviewing AI output
- `docs/workshop_rubric.md`: debrief rubric
- `examples/refactor_prompt_demo.py`: small presentation demo
