#!/bin/bash
# Lint and format check script using ruff
# This script mirrors the GitHub Actions lint workflow (.github/workflows/lint.yml):
#   - ruff check .
#   - pyright .
# It auto-fixes formatting and lint issues where possible, then re-runs
# the strict checks at the end so a non-zero exit status is returned if
# anything remains that would fail CI. Run it locally before pushing to
# catch CI failures ahead of time.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Activate the project virtual environment so ruff/pyright are on PATH
if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
elif [ -d "venv" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
fi

echo "========================================"
echo "Running Ruff Lint Check"
echo "========================================"

# Check ruff version
ruff --version

echo ""
echo "========================================"
echo "Running Ruff Format Check"
echo "========================================"

# Check if files need formatting (will fail if not formatted)
if ! ruff format --check . 2>&1; then
    echo ""
    echo "Formatting issues detected. Running ruff format..."
    ruff format .
    echo "Formatting applied."
else
    echo "Code is properly formatted."
fi

echo ""
echo "========================================"
echo "Running Ruff Lint Check (with auto-fix)"
echo "========================================"

# Run ruff check with auto-fix. Auto-fixable issues are fixed in place;
# anything left over is reported and will be re-checked strictly below.
if ruff check . --fix 2>&1; then
    echo ""
    echo "No lint issues found."
else
    echo ""
    echo "Lint issues found and fixed where possible."
    echo "Please review any remaining issues above."
fi

echo ""
echo "========================================"
echo "Final Verification (mirrors GitHub Actions)"
echo "========================================"

# Re-run the exact commands that .github/workflows/lint.yml runs.
# No --fix and no `|| true`: any failure here must propagate to the
# caller (exit non-zero) thanks to `set -e`, just like CI.
echo "Running: ruff check ."
ruff check .

echo ""
# Pyright only scans the production / script paths (no
# ``.``) — scanning the full repo would include ``tmp/`` or
# irrelevant directories. The active code lives at the root
# (coupler.py, params.py, generate_cross_sections.py) and the
# helper scripts under ``scripts/``.
echo "Running: pyright coupler.py params.py generate_cross_sections.py scripts/"
pyright coupler.py params.py generate_cross_sections.py scripts/

echo ""
echo "========================================"
echo "All lint and type checks passed!"
echo "========================================"
