#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# Oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

echo "push_2_micro-api.sh"

[[ "$1" == "dryrun" ]] && { echo "dryrun"; exit 0; }

DATE=$(date '+%y%m%d-%H%M%S')
VERSION_PY='oarepo/version.py'
# grab full version string:
OAREPO_VER=$(sed -n '/^__version__ / {s/^[^"]\+"\([0-9\.]\+\)"$/\1/;p}' "$VERSION_PY")

# grab 2-number version string:
OAREPO_VER2=$(sed -n '/^[0-9\.]\+$/ {s/^\([0-9]\+\.[0-9]\+\)\..*$/\1/;p }' <<<"$OAREPO_VER")
BRANCH="invenio-$OAREPO_VER2"
URL="https://oarepo-bot:${OAR_BOT}@github.com/oarepo/oarepo-micro-api.git"
DIR=oarepo-micro-api

git config --global user.name oarepo-bot
git config --global user.email noreply@cesnet.cz

# chechout and push+tag new version number to oarepo-micro-api
git clone -q -b master "$URL" "$DIR"
( cd "$DIR"; git checkout "$BRANCH" || git checkout -B "$BRANCH" )
./scripts/generate_micro-api_setup.sh "$OAREPO_VER"
cd "$DIR"
MICROAPI_VERSION_PY='oarepo_micro_api/version.py'
MICROAPI_VER=$(sed -n '/^__version__ / {s/^[^"\x27]\+["\x27]\([0-9.]\+\)["\x27]$/\1/;p}' "$MICROAPI_VERSION_PY")
echo "MICROAPI_VER(tag):$MICROAPI_VER; BRANCH:$BRANCH"
#git add .travis.yml setup.py oarepo_micro_api/version.py
#git commit -m "GH action commit $DATE (run: $GITHUB_ACTION/$GITHUB_RUN_NUMBER)"
#git push --set-upstream origin "$BRANCH"
#git tag -a "$MICROAPI_VER" -m "based on oarepo $OAREPO_VER"
#git push origin "$MICROAPI_VER"

echo "Done: $?"
