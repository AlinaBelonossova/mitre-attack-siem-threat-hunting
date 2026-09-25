#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/2] Processing IOC data"
python3 "$ROOT/scripts/process_iocs.py"

echo
echo "[2/2] Running tests"
cd "$ROOT"
python3 -m unittest discover -s tests -v

echo
echo "Week 3 checks completed successfully."
