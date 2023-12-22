# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS bundles for oarepo-ui.

You include one of the bundles in a page like the example below (using
``base`` bundle as an example):

 .. code-block:: html

    {{ webpack['base.js']}}

"""
import json
from pathlib import Path

from invenio_assets.webpack import WebpackThemeBundle

# load dependencies from react-dependencies.json in this directory
dependencies = json.loads((Path(__file__).parent / "react-dependencies.json").read_text())

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes=dependencies,
)
