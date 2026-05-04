#!/usr/bin/env bash
set -euo pipefail
pytest --collect-only -q
pytest tests/test_01_validation.py::test_valid_order_can_be_created -q
