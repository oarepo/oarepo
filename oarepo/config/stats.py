#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-rdm (see https://github.com/oarepo/oarepo-rdm).
#
# oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Configuration for invenio-stats module."""

from .base import set_constants_in_caller



# Invenio-Stats
# =============
# See https://invenio-stats.readthedocs.io/en/latest/configuration.html
#     https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py#L120

def configure_stats(
        enable: bool = True,
) -> None:
    
    STATS_REGISTER_RECEIVERS = enable

    from invenio_app_rdm.config import STATS_EVENTS, STATS_AGGREGATIONS, STATS_QUERIES, STATS_PERMISSION_FACTORY
    set_constants_in_caller(locals())