import re
from datetime import timedelta
from typing import Any

from invenio_i18n import lazy_gettext as _
from invenio_oauthclient.views.client import auto_redirect_login

from .base import load_configuration_variables, set_constants_in_caller


def configure_generic_parameters(
    languages=(("cs", _("Czech")),),
) -> None:
    # see https://inveniordm.docs.cern.ch/install/configuration/ for the meaning
    # of the variables here

    env = load_configuration_variables()

    # generic
    APP_ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
    SITE_UI_URL = (
        env.get("INVENIO_SITE_UI_URL", None)
        or f"https://{env.INVENIO_UI_HOST}:{env.INVENIO_UI_PORT}"
    )
    SITE_API_URL = (
        env.get("INVENIO_SITE_API_URL", None)
        or f"https://{env.INVENIO_API_HOST}:{env.INVENIO_API_PORT}/api"
    )

    # security
    APP_DEFAULT_SECURE_HEADERS: dict[str, Any] = {
        "content_security_policy": {
            "default-src": [
                "'self'",
                "data:",  # for fonts
                "'unsafe-inline'",  # for inline scripts and styles
                "blob:",  # for pdf preview
                # Add your own policies here (e.g. analytics)
            ],
        },
        "content_security_policy_report_only": False,
        "content_security_policy_report_uri": None,
        "force_file_save": False,
        "force_https": True,
        "force_https_permanent": False,
        "frame_options": "sameorigin",
        "frame_options_allow_from": None,
        "session_cookie_http_only": True,
        "session_cookie_secure": True,
        "strict_transport_security": True,
        "strict_transport_security_include_subdomains": True,
        "strict_transport_security_max_age": 31556926,  # One year in seconds
        "strict_transport_security_preload": False,
    }
    # enable local login
    ACCOUNTS_LOCAL_LOGIN_ENABLED = env.INVENIO_ACCOUNTS_LOCAL_LOGIN_ENABLED
    # local login: allow users to register
    SECURITY_REGISTERABLE = env.INVENIO_SECURITY_REGISTERABLE
    # local login: allow users to reset the password
    SECURITY_RECOVERABLE = env.INVENIO_SECURITY_RECOVERABLE
    # local login: allow users to change psw
    SECURITY_CHANGEABLE = env.INVENIO_SECURITY_CHANGEABLE
    # local login: users can confirm e-mail address
    SECURITY_CONFIRMABLE = env.INVENIO_SECURITY_CONFIRMABLE
    # require users to confirm email before being able to login
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = (
        env.INVENIO_SECURITY_LOGIN_WITHOUT_CONFIRMATION
    )
    SESSION_COOKIE_SECURE = True

    # user security settings
    RATELIMIT_GUEST_USER = "5000 per hour;500 per minute"
    RATELIMIT_AUTHENTICATED_USER = "20000 per hour;2000 per minute"
    OAUTHCLIENT_REMOTE_APPS: dict[str, Any] = {}  # configure external login providers
    ACCOUNTS_LOGIN_VIEW_FUNCTION = (
        auto_redirect_login  # autoredirect to external login if enabled
    )
    OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True  # autoredirect to external login

    # database
    SQLALCHEMY_DATABASE_URI = env.get("INVENIO_SQLALCHEMY_DATABASE_URI", None) or (
        "postgresql+psycopg2://"
        f"{env.INVENIO_DATABASE_USER}:{env.INVENIO_DATABASE_PASSWORD}"
        f"@{env.INVENIO_DATABASE_HOST}:{env.INVENIO_DATABASE_PORT}"
        f"/{env.INVENIO_DATABASE_DBNAME}"
    )

    # i18n
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "Europe/Prague"
    I18N_LANGUAGES = list(languages)

    # files
    SEND_FILE_MAX_AGE_DEFAULT = 300
    FILES_REST_STORAGE_FACTORY = "invenio_s3.s3fs_storage_factory"
    S3_ENDPOINT_URL = env.get("INVENIO_S3_ENDPOINT_URL", None) or (
        f"{env.INVENIO_S3_PROTOCOL}://{env.INVENIO_S3_HOST}:{env.INVENIO_S3_PORT}/"
    )
    S3_ACCESS_KEY_ID = env.INVENIO_S3_ACCESS_KEY
    S3_SECRET_ACCESS_KEY = env.INVENIO_S3_SECRET_KEY
    APP_DEFAULT_SECURE_HEADERS["content_security_policy"]["default-src"].append(
        S3_ENDPOINT_URL
    )
    FILES_REST_STORAGE_CLASS_LIST = {
        "L": "Local",
    }
    FILES_REST_DEFAULT_STORAGE_CLASS = "L"

    # user profiles
    USERPROFILES_READ_ONLY = (
        False  # allow users to change profile info (name, email, etc...)
    )

    # oai server
    OAISERVER_ID_PREFIX = SITE_UI_URL
    """The prefix that will be applied to the generated OAI-PMH ids."""

    # search
    SEARCH_INDEX_PREFIX = env.INVENIO_SEARCH_INDEX_PREFIX
    SEARCH_HOSTS = [
        dict(host=env.INVENIO_OPENSEARCH_HOST, port=env.INVENIO_OPENSEARCH_PORT),
    ]
    SEARCH_CLIENT_CONFIG = dict(
        use_ssl=env.INVENIO_OPENSEARCH_USE_SSL,
        verify_certs=env.INVENIO_OPENSEARCH_VERIFY_CERTS,
        ssl_assert_hostname=env.INVENIO_OPENSEARCH_ASSERT_HOSTNAME,
        ssl_show_warn=env.INVENIO_OPENSEARCH_SHOW_WARN,
        ca_certs=env.get("INVENIO_OPENSEARCH_CA_CERTS_PATH", None),
    )
    
    # caches
    INVENIO_CACHE_TYPE = "redis"
    CACHE_REDIS_URL = env.get("INVENIO_CACHE_REDIS_URL", None) or (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_CACHE_DB}"
    )
    ACCOUNTS_SESSION_REDIS_URL = env.get(
        "INVENIO_ACCOUNTS_SESSION_REDIS_URL", None
    ) or (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_SESSION_DB}"
    )
    COMMUNITIES_IDENTITIES_CACHE_REDIS_URL = env.get(
        "INVENIO_COMMUNITIES_IDENTITIES_CACHE_REDIS_URL", None
    ) or (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_COMMUNITIES_CACHE_DB}"
    )

    # json schemas for validation
    RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
    RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"
    JSONSCHEMAS_HOST = SITE_UI_URL

    # vocabularies
    try:
        from oarepo_vocabularies.resources.config import VocabulariesResourceConfig
        from oarepo_vocabularies.services.config import VocabulariesConfig

        VOCABULARIES_SERVICE_CONFIG = VocabulariesConfig
        VOCABULARIES_RESOURCE_CONFIG = VocabulariesResourceConfig
    except ImportError:
        # keep the default Invenio vocabularies config
        pass

    # Redis port redirection
    # ---------------------
    CELERY_BROKER_URL = env.get("INVENIO_CELERY_BROKER_URL", None) or (
        f"amqp://{env.INVENIO_RABBIT_USER}:{env.INVENIO_RABBIT_PASSWORD}"
        f"@{env.INVENIO_RABBIT_HOST}:{env.INVENIO_RABBIT_PORT}/"
    )
    BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = env.get("INVENIO_CELERY_RESULT_BACKEND", None) or (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_CELERY_RESULT_DB}"
    )

    # Instance secret key, used to encrypt stuff (for example, access tokens) inside database
    SECRET_KEY = env.INVENIO_SECRET_KEY

    DASHBOARD_RECORD_CREATE_URL = None

    # Do not add default records as we provide our own compatibility layer
    RECORD_ROUTES = {}
    RECORDS_REST_ENDPOINTS = {}

    # RDM
    INVENIO_RDM_ENABLED = True
    RDM_PERSISTENT_IDENTIFIERS: dict = {}
    RDM_PARENT_PERSISTENT_IDENTIFIERS: dict = {}
    RDM_USER_MODERATION_ENABLED = False
    RDM_RECORDS_ALLOW_RESTRICTION_AFTER_GRACE_PERIOD = False
    RDM_ALLOW_METADATA_ONLY_RECORDS = True
    RDM_DEFAULT_FILES_ENABLED = False
    RDM_SEARCH_SORT_BY_VERIFIED = False
    RDM_RECORDS_RESTRICTION_GRACE_PERIOD = timedelta(days=30)
    """Grace period for changing record access to restricted."""
    RDM_ARCHIVE_DOWNLOAD_ENABLED = True

    # datacite & dois default
    DATACITE_TEST_MODE = True

    MAIL_DEFAULT_SENDER = env.get(
        "INVENIO_MAIL_DEFAULT_SENDER",
        "please-set-invenio_mail_default_sender@test.com",
    )

    if env.get("INVENIO_MAIL_SUPPRESS_SEND", None) is not None:
        MAIL_SUPPRESS_SEND = env.get("INVENIO_MAIL_SUPPRESS_SEND", True)

    # default schemes for identifiers
    import idutils

    def is_researcher_id(identifier):
        pattern = r"^[A-Za-z]+-\d{4}-\d{4}$"
        return bool(re.match(pattern, identifier))

    def is_vedidk(identifier):
        cleaned_identifier = identifier.strip()
        return cleaned_identifier.isdigit() and len(cleaned_identifier) == 7

    def is_scopus_id(identifier):
        return identifier.replace(".0", "").isdigit()

    VOCABULARIES_NAMES_SCHEMES = {
        "orcid": {"label": "ORCID", "validator": idutils.is_orcid},
        "vedidk": {"label": "VEDIDK", "validator": is_vedidk},
        "scopusId": {"label": "Scopus ID", "validator": is_scopus_id},
        "researcherId": {"label": "Researcher ID", "validator": is_researcher_id},
    }

    # List of funders is curated, validators are not needed.
    VOCABULARIES_FUNDER_SCHEMES = {
        "ror": {"label": "ROR", "validator": lambda identifier: True},
        "crossrefFunderId": {
            "label": "CrossrefFunderID",
            "validator": lambda identifier: True,
        },
    }

    # List of affiliations is curated, validators are not needed.
    VOCABULARIES_AFFILIATION_SCHEMES = {
        "ror": {"label": "ROR", "validator": lambda identifier: True},
        "ico": {"label": "ICO", "validator": lambda identifier: True},
        "url": {"label": "URL", "validator": lambda identifier: True},
    }
    RDM_RECORDS_PERSONORG_SCHEMES = {
        "orcid": {"label": _("ORCID"), "validator": idutils.is_orcid},
        "scopusId": {"label": _("ScopusID"), "validator": is_scopus_id},
        "researcherId": {"label": _("ResearcherID"), "validator": is_researcher_id},
        "czenasAutId": {
            "label": _("CzenasAutID"),
            "validator": lambda identifier: True,
        },
        "vedidk": {"label": _("vedIDK"), "validator": is_vedidk},
        "institutionalId": {
            "label": _("InstitutionalID"),
            "validator": lambda identifier: True,
        },
        "isni": {"label": _("ISNI"), "validator": idutils.is_isni},
        "ror": {"label": _("ROR"), "validator": idutils.is_ror},
        "ico": {"label": _("ICO"), "validator": lambda identifier: True},
        "doi": {"label": _("DOI"), "validator": idutils.is_doi},
        "url": {"label": _("URL"), "validator": lambda identifier: True},
    }

    RDM_RECORDS_IDENTIFIERS_SCHEMES = {
        "doi": {"label": _("DOI"), "validator": idutils.is_doi},
        "isbn": {"label": _("ISBN"), "validator": idutils.is_isbn},
    }

    set_constants_in_caller(locals())
