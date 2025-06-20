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
echo "docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch7} --mq ${MQ:-redis} --env"
docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch7} --mq ${MQ:-redis} --env
eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch7} --mq ${MQ:-redis} --env)"
ENV1="$(printenv)"
echo "env diff:"
diff <(echo "$ENV0") <(echo "$ENV1") || true
echo ""

echo -e "\nsearch-service GET:"
wget -q --waitretry=1 --retry-connrefused -T 10 -O - http://127.0.0.1:9200

# isort -rc -c -df **/*.py && \       # metapackage, isort not needed
check-manifest --ignore ".travis-*" --ignore-bad-ideas 'oarepo/collected_translations/**/*.mo' && \
pytest
