#!/usr/bin/env bash

set -euo pipefail

uv venv --clear --python=3.14 .venv
source .venv/bin/activate

uv pip install -e '.[test]'

$(dirname "$0")/run-tests.sh
