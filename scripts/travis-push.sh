#!/bin/bash

set -e

echo "travis-push.sh"

[[ "$1" == "dryrun" ]] && { echo "dryrun"; exit 0; }

#BRANCH=invenio-3.3
BRANCH=test-travis-push
DATE=$(date '+%y%m%d-%H%M%S')

git config --global user.name oarepo-bot
git config --global user.email noreply@cesnet.cz

git clone -q -b "$BRANCH" https://oarepo-bot:${OAR_BOT}@github.com/oarepo/oarepo-micro-api.git \
 && date '+%y%m%d-%H%M%S' >> tests/.trig.txt \
 && git add tests/.trig.txt \
 && git commit -m "travis commit $DATE (build:$TRAVIS_BUILD_NUMBER result:$TRAVIS_TEST_RESULT)" -m "[skip ci]" \
 && git push
