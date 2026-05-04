# Half-Day Practical Workshop Plan

This plan assumes 10 programmers with mixed experience. Use 5 pairs, or 3
groups of three plus one facilitator-paired participant.

## Pre-work

Send participants the setup instructions before the workshop. Ask them to run
`pytest --collect-only` and confirm that the suite starts with intentional
failures.

## 09:00-09:20 — Kickoff

Do:

1. explain that the repo is intentionally broken
2. show one bad prompt and one improved prompt
3. explain the baseline, extension, and expert markers

Use `examples/refactor_prompt_demo.py` if you want a quick live prompt demo.

## 09:20-10:10 — Exercise 1: validation

Run `pytest tests/test_01_validation.py`.

Facilitator focus:

- ask AI to explain the request models before editing
- compare Pydantic validation vs. explicit service validation
- keep the fix small

## 10:10-10:20 — Break

## 10:20-11:10 — Exercise 2: pricing

Run `pytest tests/test_02_pricing.py`.

Facilitator focus:

- write down business rules before patching
- watch for AI changing more code than needed
- ask teams how they checked the numbers

## 11:10-12:00 — Exercise 3: security

Run `pytest tests/test_03_security.py`.

Facilitator focus:

- distinguish authentication from authorization
- ask AI for risks, then require tests before fixes
- discuss one suggestion the team rejected

## 12:00-12:30 — Debrief

Each team presents:

1. best prompt
2. weakest AI suggestion
3. one test that saved them
4. one thing they would use tomorrow at work
