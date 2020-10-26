#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# Oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

echo "generate_micro-api_setup.sh"

SETUP_PY='oarepo-micro-api/setup.py'
TRAVIS_YML='oarepo-micro-api/.travis.yml'
VERSION_PY='oarepo-micro-api/oarepo_micro_api/version.py'
NEWVER=${1:?Version string expected}

# inject NEWVER into setup.py as default OAREPO_VERSION
sed -i "/^OAREPO_VERSION/ s/os.environ.get('OAREPO_VERSION', '[0-9\.a-z]\+')/os.environ.get('OAREPO_VERSION', '$NEWVER')/" "${SETUP_PY}"

# inject NEWVER into .travis.yml as OAREPO_VERSION in matrix
sed -i "/^ \+matrix:/,/^\$/ s/OAREPO_VERSION=\([^ ]\+\) /OAREPO_VERSION=$NEWVER /" "${TRAVIS_YML}"

# modify version.py
sed -i "/^__version__ / {s/\x27[0-9.]\+\x27/\x27$NEWVER\x27/}" "${VERSION_PY}"

echo "Done: $?"
