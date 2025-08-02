#!/usr/bin/env bash

set -euo pipefail

base_dir="$(dirname "$0")"

if [ ! -f "${base_dir}/.runner.sh" ]; then
  echo "Downloading .runner.sh from oarepo repository..."
  curl -o "${base_dir}/.runner.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/runner.sh
  chmod +x "${base_dir}/.runner.sh"
fi

"${base_dir}/.runner.sh" "$@"