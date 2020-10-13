#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# Oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

echo "travis-push.sh"

[[ "$1" == "dryrun" ]] && { echo "dryrun"; exit 0; }

DATE=$(date '+%y%m%d-%H%M%S')
VERSION_PY='oarepo/version.py'
NEWVER=$(sed -n '/^__version__ / {s/^[^"]\+"\([0-9\.]\+\)"$/\1/;p}' "$VERSION_PY")
BRANCH="oarepo-$NEWVER"
URL="https://oarepo-bot:${OAR_BOT}@github.com/oarepo/oarepo-micro-api.git"
DIR=oarepo-micro-api

git config --global user.name oarepo-bot
git config --global user.email noreply@cesnet.cz

{
  git clone -q -b "$BRANCH" "$URL" "$DIR" \
    || git clone -q -b master "$URL" "$DIR"
} \
  && ./scripts/generate_micro-api_setup.sh "$NEWVER" \
  && cd "$DIR" \
  && git checkout -b "$BRANCH" \
  && git add .travis.yml setup.py \
  && git commit -m "travis commit $DATE (build:$TRAVIS_BUILD_NUMBER result:$TRAVIS_TEST_RESULT)" \
  && git push --set-upstream origin "$BRANCH"
