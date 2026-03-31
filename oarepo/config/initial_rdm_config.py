#
# Copyright (c) 2026 CESNET z.s.p.o.
#
# This file is a part of oarepo (see https://github.com/oarepo/oarepo).
#
# oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Initial configuration which replaces RDM service with oarepo extensions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from invenio_app_rdm import config as rdm_config  # noqa

if TYPE_CHECKING:
    from collections.abc import Callable

# TODO: Why not to add other RDM routes here?
APP_RDM_ROUTES = {
    "index": "/",
    "robots": "/robots.txt",
    "help_search": "/help/search",
    "help_statistics": "/help/statistics",
    # "help_versioning": "/help/versioning", #noqa
    "record_search": "/search",
    "record_detail": "/records/<pid_value>",
    "record_export": "/records/<pid_value>/export/<export_format>",
    "record_file_preview": "/records/<pid_value>/preview/<path:filename>",
    "record_file_download": "/records/<pid_value>/files/<path:filename>",
    "record_thumbnail": "/records/<pid_value>/thumb<int:size>",
    "record_media_file_download": "/records/<pid_value>/media-files/<path:filename>",
    "record_from_pid": "/<any({schemes}):pid_scheme>/<path:pid_value>",
    "record_latest": "/records/<pid_value>/latest",
    # "dashboard_home": "/me", #noqa
    # "deposit_create": "/uploads/new", #noqa
    "deposit_edit": "/uploads/<pid_value>",
}

# OAI-PMH
# =======
# See https://github.com/inveniosoftware/invenio-oaiserver/blob/master/invenio_oaiserver/config.py
# (Using GitHub because documentation site out-of-sync at time of writing)


OAISERVER_SEARCH_CLS = "invenio_rdm_records.oai:OAIRecordSearch"
"""Class for record search."""

OAISERVER_ID_FETCHER = "invenio_rdm_records.oai:oaiid_fetcher"
"""OAI ID fetcher function."""

OAISERVER_LAST_UPDATE_KEY = "updated"
"""Record update key."""

OAISERVER_CREATED_KEY = "created"
"""Record created key."""

OAISERVER_RECORD_CLS = "invenio_rdm_records.records.api:RDMRecord"
"""Record retrieval class."""

OAISERVER_RECORD_SETS_FETCHER = "invenio_oaiserver.percolator:find_sets_for_record"
"""Record's OAI sets function."""

OAISERVER_RECORD_INDEX = "oaisource"
"""oaisource is a mapping alias for records that can be sent over OAI-PMH.

To mark your model as oaisource, add `oarepo_rdm.oai.oai_presets` to your model's presets."""

# TODO: oarepo extension, maybe not needed
OAISERVER_RECORD_LIST_SETS_FETCHER = "invenio_oaiserver.percolator:sets_search_all"

"""Specify a search index with records that should be exposed via OAI-PMH."""

OAISERVER_GETRECORD_FETCHER = "invenio_rdm_records.oai:getrecord_fetcher"
"""Record data fetcher for serialization."""

# extra oarepo extensions - TODO: maybe not needed
OAISERVER_NEW_PERCOLATOR_FUNCTION = "invenio_oaiserver.percolator:_new_percolator"
# TODO: maybe not needed
OAISERVER_DELETE_PERCOLATOR_FUNCTION = "invenio_oaiserver.percolator:_delete_percolator"

# cleared rest endpoints
RECORDS_REST_ENDPOINTS: list[Any] = []

APP_RDM_USER_DASHBOARD_ROUTES = {
    "uploads": "/me/uploads",
    "communities": "/me/communities",
    "requests": "/me/requests",
}
"""Routes for user dashboard"""

USER_DASHBOARD_MENU_OVERRIDES: dict[str, str] = {}
"""Menu overrides for user dashboard"""

RDM_SEARCH_USER_COMMUNITIES = {
    "facets": ["visibility", "type"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""User communities search configuration"""

RDM_SEARCH_USER_REQUESTS = {
    "facets": ["type", "status"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""User requests search configuration"""


RDM_COMMUNITIES_ROUTES = {
    "community-detail": "/communities/<pid_value>/records",
    "community-home": "/communities/<pid_value>/",
    "community-browse": "/communities/<pid_value>/browse",
    "community-static-page": "/communities/<pid_value>/pages/<path:page_slug>",
    "community-collection": "/communities/<pid_value>/collections/<tree_slug>/<collection_slug>",
}
"""Communities routes from app RDM."""


COMMUNITIES_RECORDS_SEARCH = {
    "facets": ["access_status", "resource_type", "language"],
    "sort": ["bestmatch", "newest", "oldest", "version"],
}
"""Communities records search configuration."""


RDM_REQUESTS_ROUTES = {
    "user-dashboard-request-details": "/me/requests/<uuid:request_pid_value>",
    "community-dashboard-request-details": "/communities/<pid_value>/requests/<uuid:request_pid_value>",
    "community-dashboard-invitation-details": "/communities/<pid_value>/invitations/<uuid:request_pid_value>",
}
"""Routes for requests in RDM."""


class ExternalLinkConfig(TypedDict):
    """Configuration for an external link on the record landing page."""

    id: str
    render: Callable[..., Any]


APP_RDM_RECORD_LANDING_PAGE_EXTERNAL_LINKS: list[ExternalLinkConfig] = []
"""External links to be shown on record landing page."""
