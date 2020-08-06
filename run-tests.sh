#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# isort -rc -c -df **/*.py && \       # metapackage, isort not needed
check-manifest --ignore ".travis-*" --ignore "invenio-integration-tests" && \
python setup.py test
