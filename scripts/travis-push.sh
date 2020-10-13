#!/bin/bash

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
  && echo "$DATE" >> tests/.trig.txt \
  && git add .travis.yml setup.py tests/.trig.txt \
  && git commit -m "travis commit $DATE (build:$TRAVIS_BUILD_NUMBER result:$TRAVIS_TEST_RESULT)" -m "[skip ci]" \
  && git push --set-upstream origin "$BRANCH"
