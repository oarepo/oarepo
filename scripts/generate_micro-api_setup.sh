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
OAREPO_VER=${1:?Version string expected}

python -m pip install --upgrade pip
pip install bump

# oarepo-micro-api version from version.py:
PREV_MICROAPI_VER=$(sed -n '/^__version__ / {s/^[^"\x27]\+["\x27]\([0-9.]\+\)["\x27]$/\1/;p}' "$VERSION_PY")
# grab 2-number oarepo-micro-api version string:
PREV_MICROAPI_VER2=$(sed -n '/^[0-9\.]\+$/ {s/^\([0-9]\+\.[0-9]\+\)\..*$/\1/;p }' <<<"$PREV_MICROAPI_VER")
# grab 2-number oarepo version string:
OAREPO_VER2=$(sed -n '/^[0-9\.]\+$/ {s/^\([0-9]\+\.[0-9]\+\)\..*$/\1/;p }' <<<"$OAREPO_VER")

# if there is new invenio version, update 1st two numbers accordingly
[[ "$OAREPO_VER2" != "$PREV_MICROAPI_VER2" ]] && sed -i "/^__version__ / {s/[\"'][0-9.]\+[\"']/\"$OAREPO_VER2.0\"/}" "$VERSION_PY"

# bump version.py + catch new value:
NEW_MICROAPI_VER=$(bump "$VERSION_PY" "$VERSION_PY")

# inject NEW_MICROAPI_VER into setup.py as default OAREPO_VERSION:
sed -i "/^OAREPO_VERSION/ s/os.environ.get('OAREPO_VERSION', '[0-9\.a-z]\+')/os.environ.get('OAREPO_VERSION', '$OAREPO_VER')/" "${SETUP_PY}"

# inject NEW_MICROAPI_VER into .travis.yml as OAREPO_VERSION in matrix:
sed -i "/^ \+matrix:/,/^\$/ s/OAREPO_VERSION=\([^ ]\+\) /OAREPO_VERSION=$OAREPO_VER /" "${TRAVIS_YML}"

echo "Done: $?"
