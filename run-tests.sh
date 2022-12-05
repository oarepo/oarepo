#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

set -e

echo -e "\noarepo/run_tests.sh"

function cleanup(){
  eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT

ENV0="$(printenv)"

echo "docker-services-cli up (DB:$DB; SEARCH:$SEARCH)"
eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch7} --mq ${MQ:-redis} --env)"

ENV1="$(printenv)"

echo "env diff:"
diff <(echo "$ENV0") <(echo "$ENV1") || true
echo ""

# isort -rc -c -df **/*.py && \       # metapackage, isort not needed
check-manifest --ignore ".travis-*" && \
pytest
