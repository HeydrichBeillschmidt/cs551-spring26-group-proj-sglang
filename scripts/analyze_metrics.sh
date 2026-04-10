#!/usr/bin/env bash
# Summarize one SGLang benchmark JSONL file into a CSV in the same directory.
#
# Usage:
#   bash repo_root/scripts/analyze_metrics.sh <bench_metrics.jsonl>
#
# Example:
#   bash repo_root/scripts/analyze_metrics.sh repo_root/logs/sharegpt/20260410-120000/bench_metrics.jsonl

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: bash repo_root/scripts/analyze_metrics.sh <bench_metrics.jsonl>"
    exit 1
fi

INPUT_FILE="$1"
REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

if [[ -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
    PYTHON="${CONDA_PREFIX}/bin/python"
else
    PYTHON="${PYTHON:-python3}"
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: benchmark file not found: $INPUT_FILE"
    exit 1
fi

OUTDIR="$(dirname "$INPUT_FILE")"
OUTCSV="$OUTDIR/bench_metrics.csv"

echo "Summarizing benchmark log:"
echo "  Input : $INPUT_FILE"
echo "  Output: $OUTCSV"

"$PYTHON" "$REPO_ROOT/scripts/parse_metrics.py" "$INPUT_FILE" "$OUTCSV"

echo "Done."
