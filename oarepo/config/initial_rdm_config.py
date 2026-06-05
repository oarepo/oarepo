#
# Copyright (c) 2026 CESNET z.s.p.o.
#
# This file is a part of oarepo (see https://github.com/oarepo/oarepo).
#
# oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Initial configuration which replaces RDM service with oarepo extensions. This is the place where we will keep
most RDM related configuration (all that is possible) in order to avoid keeping it in oarepo-rdm which then creates
a problem, where every package needs to depend on oarepo-rdm."""

from __future__ import annotations

import re
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypedDict

import idutils
from invenio_app_rdm import config as app_rdm_config
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records import config as rdm_records_config

if TYPE_CHECKING:
    from collections.abc import Callable

APP_RDM_ROUTES = app_rdm_config.APP_RDM_ROUTES
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

APP_RDM_USER_DASHBOARD_ROUTES = app_rdm_config.APP_RDM_USER_DASHBOARD_ROUTES
"""Routes for user dashboard"""

USER_DASHBOARD_MENU_OVERRIDES: dict[str, str] = {}
"""Menu overrides for user dashboard"""

RDM_SEARCH_USER_COMMUNITIES = app_rdm_config.RDM_SEARCH_USER_COMMUNITIES
"""User communities search configuration"""
# TODO: invenio's config is different, should we use theirs?
RDM_SEARCH_USER_REQUESTS = {
    "facets": ["type", "status"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""User requests search configuration"""


RDM_COMMUNITIES_ROUTES = app_rdm_config.RDM_COMMUNITIES_ROUTES
"""Communities routes from app RDM."""


COMMUNITIES_RECORDS_SEARCH = app_rdm_config.COMMUNITIES_RECORDS_SEARCH
"""Communities records search configuration."""


RDM_REQUESTS_ROUTES = app_rdm_config.RDM_REQUESTS_ROUTES
"""Routes for requests in RDM."""


class ExternalLinkConfig(TypedDict):
    """Configuration for an external link on the record landing page."""

    id: str
    render: Callable[..., Any]


APP_RDM_RECORD_LANDING_PAGE_EXTERNAL_LINKS: list[ExternalLinkConfig] = []
"""External links to be shown on record landing page."""


def is_researcher_id(identifier: str) -> bool:
    """Validate ResearcherID format: letters, dash, 4 digits, dash, 4 digits."""
    pattern = r"^[A-Za-z]+-\d{4}-\d{4}$"
    return bool(re.fullmatch(pattern, identifier))


def is_vedidk(identifier: str) -> bool:
    """Validate vedIDK: 7-digit numeric string (whitespace ignored)."""
    cleaned_identifier = identifier.strip()
    return cleaned_identifier.isdigit() and len(cleaned_identifier) == 7  # noqa: PLR2004


def is_scopus_id(identifier: str) -> bool:
    """Validate Scopus Author ID: numeric, tolerating a trailing ``.0``."""
    return bool(re.fullmatch(r"\d+(?:\.0)?", identifier))


RDM_RECORDS_PERSONORG_SCHEMES = {
    **rdm_records_config.RDM_RECORDS_PERSONORG_SCHEMES,
    "scopusid": {
        "label": _("Scopus Author ID"),
        "validator": is_scopus_id,
        "datacite": "Scopus Author ID",
    },
    "researcherid": {
        "label": _("Researcher ID"),
        "validator": is_researcher_id,
        "datacite": "ResearcherID",
    },
    "czenasautid": {
        "label": _("CzenasAutID"),
        "validator": lambda _: True,
    },
    "vedidk": {"label": _("vedIDK"), "validator": is_vedidk},
    "institutionalid": {
        "label": _("InstitutionalID"),
        "validator": lambda _: True,
    },
    "ico": {"label": _("ICO"), "validator": lambda _: True},
    "doi": {"label": _("DOI"), "validator": idutils.is_doi, "datacite": "DOI"},  # pyright: ignore[reportAttributeAccessIssue]
    "url": {"label": _("URL"), "validator": lambda _: True},
    "grid": {"label": _("GRID"), "validator": lambda _: True},
}
"""Default values for person/org schemes."""

RDM_RECORDS_IDENTIFIERS_SCHEMES = rdm_records_config.RDM_RECORDS_IDENTIFIERS_SCHEMES
"""Default values for identifiers schemes."""
RDM_RECORDS_RELATED_IDENTIFIERS_SCHEMES = RDM_RECORDS_IDENTIFIERS_SCHEMES
"""This variable is used to separate related identifiers."""
INVENIO_RDM_ENABLED = True
RDM_PERSISTENT_IDENTIFIERS: dict = {}
RDM_PARENT_PERSISTENT_IDENTIFIERS: dict = {}
RDM_USER_MODERATION_ENABLED = False
RDM_RECORDS_ALLOW_RESTRICTION_AFTER_GRACE_PERIOD = False
RDM_ALLOW_METADATA_ONLY_RECORDS = True
RDM_DEFAULT_FILES_ENABLED = True
RDM_SEARCH_SORT_BY_VERIFIED = False
RDM_RECORDS_RESTRICTION_GRACE_PERIOD = timedelta(days=30)
"""Grace period for changing record access to restricted."""
RDM_ARCHIVE_DOWNLOAD_ENABLED = True


RDM_RECORDS_LOCATION_SCHEMES = rdm_records_config.RDM_RECORDS_LOCATION_SCHEMES
"""Default values for location schemes."""

RDM_CITATION_STYLES = [
    *app_rdm_config.RDM_CITATION_STYLES,
    ("iso690-author-date-cs", _("ČSN ISO 690")),
]
"""Available citation styles for records."""
RDM_CITATION_STYLES_DEFAULT = "iso690-author-date-cs"
"""Default citation style for records."""

APP_RDM_MODERATION_REQUEST_SORT_OPTIONS = (
    app_rdm_config.APP_RDM_MODERATION_REQUEST_SORT_OPTIONS
)

APP_RDM_MODERATION_REQUEST_SEARCH = app_rdm_config.APP_RDM_MODERATION_REQUEST_SEARCH

APP_RDM_MODERATION_REQUEST_FACETS = app_rdm_config.APP_RDM_MODERATION_REQUEST_FACETS
