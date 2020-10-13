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
NEWVER=${1:?Version string expected}

#    /'oarepo\(\[[a-z]\+\]\)\?~={version}'\.format(/ s/'oarepo\(\[[a-z]\+\]\)\?~={version}'\.format(/'oarepo\1=={version}'.format(/
sed -i "
    /^OAREPO_VERSION/ s/os.environ.get('OAREPO_VERSION', '[0-9\.a-z]\+')/os.environ.get('OAREPO_VERSION', '$NEWVER')/
  " ${SETUP_PY}

sed -i "
    /^ \+matrix:/,/^\$/ s/OAREPO_VERSION=\([^ ]\+\) /OAREPO_VERSION=$NEWVER /
  " ${TRAVIS_YML}
