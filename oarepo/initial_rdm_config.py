#
# Copyright (c) 2026 CESNET z.s.p.o.
#
# This file is a part of oarepo (see https://github.com/oarepo/oarepo).
#
# oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Initial configuration which replaces RDM service with oarepo extensions.

This file is loaded once when invenio starts up. It's entrypoint is called
0000-initial-oarepo-config so that other config entrypoints can override it.

The reason it is not in the oarepo-config is that almost all oarepo libraries
need some kind of invenio configuration to work and putting it to the oarepo-config
would create a circular dependency - because oarepo-config is dependent on those
libraries.

The aim is to put non-conflicting configuration here, and potentially override
it inside the oarepo-config.
"""

from __future__ import annotations

import re
from datetime import timedelta
from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING, Any, TypedDict

import idutils
from invenio_app import config as app_config
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

APP_RDM_MODERATION_REQUEST_SORT_OPTIONS = app_rdm_config.APP_RDM_MODERATION_REQUEST_SORT_OPTIONS

APP_RDM_MODERATION_REQUEST_SEARCH = app_rdm_config.APP_RDM_MODERATION_REQUEST_SEARCH

APP_RDM_MODERATION_REQUEST_FACETS = app_rdm_config.APP_RDM_MODERATION_REQUEST_FACETS

PREVIEWER_PREFERENCE = app_rdm_config.PREVIEWER_PREFERENCE

PREVIEWER_CONTAINER_ITEM_PREFERENCE = app_rdm_config.PREVIEWER_CONTAINER_ITEM_PREFERENCE

PREVIEWABLE_ZIP_PREVIEWER_NATIVE_EXTENSIONS = app_rdm_config.PREVIEWABLE_ZIP_PREVIEWER_NATIVE_EXTENSIONS

IIIF_PREVIEW_TEMPLATE = app_rdm_config.IIIF_PREVIEW_TEMPLATE

IIIF_SIMPLE_PREVIEWER_SIZE = app_rdm_config.IIIF_SIMPLE_PREVIEWER_SIZE

IIIF_SIMPLE_PREVIEWER_NATIVE_EXTENSIONS = app_rdm_config.IIIF_SIMPLE_PREVIEWER_NATIVE_EXTENSIONS

# invenio notifications

# this is in fact overridden in our oarepo_requests
NOTIFICATIONS_BACKENDS = app_rdm_config.NOTIFICATIONS_BACKENDS

# this is also overridden in our oarepo_requests
NOTIFICATIONS_BUILDERS = app_rdm_config.NOTIFICATIONS_BUILDERS

NOTIFICATIONS_ENTITY_RESOLVERS = app_rdm_config.NOTIFICATIONS_ENTITY_RESOLVERS

# required for share notifications, otherwise they fail
NOTIFICATIONS_SETTINGS_VIEW_FUNCTION = app_rdm_config.notification_settings
"""View function for notification settings."""

# InvenioRDM flavour defaults
# ===========================
# Upstream applies the settings below through invenio_app_rdm.config, which is
# not loaded in OARepo (it would bring back the stock RDM record UI, routes and
# templates). They are inert or purely corrective, so they are safe as defaults
# of every OARepo application, test suites included.
#
# Defaults that switch on enforcement (REST_CSRF_ENABLED, ACCESS_CACHE, the
# ACCOUNTS_*_RATELIMIT limits) or depend on the deployment (the database
# connection pool, the rate limiting storage) are applied by oarepo-config's
# configure_generic_parameters instead.
#
# Deliberately not copied: DB_VERSIONING_USER_MODEL - it decides whether the
# SQLAlchemy-Continuum `transaction` table has a `user_id` column, i.e. it is
# part of the database schema of existing deployments.

MAX_CONTENT_LENGTH = app_rdm_config.MAX_CONTENT_LENGTH
"""Max size of form data (multipart/urlencoded) request bodies.

Streamed file uploads are not affected, see invenio_files_rest.app.
"""

FILES_REST_PERMISSION_FACTORY = app_rdm_config.files_rest_permission_factory
"""Deny the legacy invenio-files-rest REST API (/api/files).

It does not honour record permissions; records-resources serves all files instead.
"""

FILES_REST_CHECKSUM_VERIFICATION_URI_PREFIXES: list[str] = []
"""URI prefixes of the files whose checksums should be verified (empty = all)."""

RATELIMIT_PER_ENDPOINT = {
    **app_config.RATELIMIT_PER_ENDPOINT,
    # external (OIDC/OAuth) login - same budget as the local login views
    "invenio_oauthclient.login": "10 per minute",
    "invenio_oauthclient.signup": "10 per minute",
    # DOI/ARK badges are embedded in third-party pages
    "invenio_formatter_badges.badge": "120 per minute",
}
"""Rate limits of individual endpoints, replacing the per-user limits there."""

INDEXER_MQ_PUBLISH_KWARGS = {
    "retry": True,
    "retry_policy": {
        "interval_start": 0,  # first retry immediately,
        "interval_step": 2,  # then wait 2s longer after every retry,
        "interval_max": 30,  # but never more than 30s between retries
        "max_retries": 20,
    },
}
"""Retry publishing to the indexing queue (for ~10 minutes at most) instead of losing the index update."""

APP_RDM_RECORD_THUMBNAIL_SIZES = list(app_rdm_config.APP_RDM_RECORD_THUMBNAIL_SIZES)
"""Allowed record thumbnail sizes; required by the record thumbnail view."""

APP_RDM_DISPLAY_DECIMAL_FILE_SIZES = True
"""Display file sizes in powers of 1000 (KB, ...), the unit quotas are defined in."""

APP_RDM_DEPOSIT_FORM_AUTOCOMPLETE_NAMES = app_rdm_config.APP_RDM_DEPOSIT_FORM_AUTOCOMPLETE_NAMES

APP_RDM_DEPOSIT_FORM_CUSTOM_FIELD_DEFAULTS: dict[str, Any] = {}

APP_RDM_RECORD_LANDING_PAGE_FAIR_SIGNPOSTING_LEVEL_1_ENABLED = False

APP_RDM_SUBCOMMUNITIES_LABEL = app_rdm_config.APP_RDM_SUBCOMMUNITIES_LABEL

APP_RDM_FILES_INTEGRITY_REPORT_TEMPLATE = app_rdm_config.APP_RDM_FILES_INTEGRITY_REPORT_TEMPLATE

APP_RDM_FILES_INTEGRITY_REPORT_SUBJECT = app_rdm_config.APP_RDM_FILES_INTEGRITY_REPORT_SUBJECT

FORMATTER_BADGES_ALLOWED_TITLES = list(app_rdm_config.FORMATTER_BADGES_ALLOWED_TITLES)

FORMATTER_BADGES_TITLE_MAPPING = dict(app_rdm_config.FORMATTER_BADGES_TITLE_MAPPING)

COMMUNITIES_ERROR_HANDLERS = dict(app_rdm_config.COMMUNITIES_ERROR_HANDLERS)
"""Report an invalid community visibility as HTTP 400 instead of an internal server error."""

REQUESTS_ERROR_HANDLERS = dict(app_rdm_config.REQUESTS_ERROR_HANDLERS)
"""Report invalid access restrictions as HTTP 400 instead of an internal server error."""

COMMUNITIES_SUB_INVITATION_REQUEST_CLS = app_rdm_config.COMMUNITIES_SUB_INVITATION_REQUEST_CLS
"""RDM specific request type for subcommunity invitations."""

# The "Notifications" page of the user settings stores preferences.notifications;
# without these schemas the value is neither validated on save nor exposed to
# the notification recipient filters.
ACCOUNTS_USER_PREFERENCES_SCHEMA = app_rdm_config.ACCOUNTS_USER_PREFERENCES_SCHEMA
"""The schema used for validation of the user preferences."""

USERS_RESOURCES_SERVICE_SCHEMA = app_rdm_config.USERS_RESOURCES_SERVICE_SCHEMA
"""Schema used by the users service."""


def _installed_versions(*packages: str) -> list[tuple[str, str]]:
    versions = []
    for package in packages:
        try:
            versions.append((package, f"v{version(package)}"))
        except PackageNotFoundError:
            pass
    return versions


ADMINISTRATION_DISPLAY_VERSIONS = _installed_versions("oarepo", "invenio-app-rdm")
"""Show the OARepo and InvenioRDM versions in the administration panel."""
