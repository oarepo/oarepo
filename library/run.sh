#!/usr/bin/env bash
#
# This script sets up a Python virtual environment, installs necessary packages,
# runs tests and other tasks for libraries which are part of the OARepo Invenio RDM
# flavour.
# 
# Usage: ./run.sh --help
#
#
# (C) 2025 CESNET, z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#
set -euo pipefail

base_dir="$(dirname "$0")"

if [ ! -f "${base_dir}/.runner.sh" ]; then
  echo "Downloading .runner.sh from oarepo repository..." >&2
  curl -o "${base_dir}/.runner.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/runner.sh
  chmod +x "${base_dir}/.runner.sh"
fi

"${base_dir}/.runner.sh" "$@"