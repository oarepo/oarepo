import functools
import inspect
import json
import os
import re
from datetime import timedelta
from pathlib import Path

from dotenv import dotenv_values
from flask.config import Config
from flask_babel import lazy_gettext as _
from invenio_oauthclient.views.client import auto_redirect_login
from oarepo_global_search.proxies import global_search_view_function


def set_constants_in_caller(constants):
    """
    Sets the constants in the caller's globals.

    Example:

    mymodule:
      import config
      config.doit()
      print(MY_CONSTANT)

    config:
        def doit():
            set_constants_in_caller({"MY_CONSTANT": 42})
    """
    # Get the caller's frame
    current_frame = inspect.currentframe()
    assert current_frame is not None, "Cannot get the current frame"

    config_func_frame = current_frame.f_back
    assert config_func_frame is not None, "Cannot get the config function frame"

    invenio_cfg_frame = config_func_frame.f_back
    assert invenio_cfg_frame is not None, "Cannot get the invenio.cfg frame"

    # Get the caller's globals
    caller_globals = invenio_cfg_frame.f_globals

    for key, value in constants.items():
        if re.match(r"^[A-Z0-9_]+$", key):
            caller_globals[key] = value

    del invenio_cfg_frame
    del config_func_frame
    del current_frame


def get_constant_from_caller(name, default=None):
    """
    Get constant from the caller frame and optionally return a default value
    if not found.

    Example:

    mymodule:
      import config

      MY_CONSTANT = 42
      config.doit()

    config:
        def doit():
            # prints 42
            print(getet_constant_from_caller("MY_CONSTANT", 20))

    """
    current_frame = inspect.currentframe()
    assert current_frame is not None, "Cannot get the current frame"

    config_func_frame = current_frame.f_back
    assert config_func_frame is not None, "Cannot get the config function frame"

    invenio_cfg_frame = config_func_frame.f_back
    assert invenio_cfg_frame is not None, "Cannot get the invenio.cfg frame"

    caller_globals = invenio_cfg_frame.f_globals
    del invenio_cfg_frame
    del config_func_frame
    del current_frame

    return caller_globals.get(name, default)


def get_invenio_cfg_path():
    if os.environ.get("INVENIO_INSTANCE_PATH"):
        return Path(os.environ["INVENIO_INSTANCE_PATH"]) / "invenio.cfg"

    cf = inspect.currentframe()
    while cf:
        if cf.f_code.co_filename.endswith("invenio.cfg"):
            return cf.f_code.co_filename
        cf = cf.f_back
    del cf
    raise ValueError("Cannot find invenio.cfg file in the stack")


# Import the configuration from the local .env if it exists
# and overwrite it with environment variables
# Loading it this way so could interpolate values
@functools.lru_cache(maxsize=1)
def load_configuration_variables():
    """
    Import variables from external location.

    * highest priority are environment variables starting with INVENIO_
    * then variables from .env file in the local directory
    * finally variables from the "variables" file in the root of the repository

    The values of those variables are converted to python types if possible.
    """
    env = Config(os.path.dirname(__file__))
    # lowest priority are variables
    bundled_env = Path(get_invenio_cfg_path()).parent / "variables"
    if bundled_env.exists():
        vals = dotenv_values(str(bundled_env))
        env.from_mapping(vals)

    # then overwrite it with .env file in the local directory
    if Path(".env").exists():
        vals = dotenv_values(".env")
        env.from_mapping(vals)

    # finally overwrite it with environment variables
    env.from_mapping({k: v for k, v in os.environ.items() if k.startswith("INVENIO_")})

    # transform values from strings to their actual types
    for k, v in list(env.items()):
        setattr(env, k, transform_value(v))

    return env


def transform_value(x):
    """Convert string from environment to python type."""
    if not isinstance(x, str):
        return x
    if x == "False":
        return False
    if x == "True":
        return True
    try:
        return json.loads(x)
    except:
        return x


def configure_generic_parameters(
    ns,
    env,
    code="myrepo",
    name="My Repository",
    description="",
    languages=(("cs", _("Czech")),),
):
    # see https://inveniordm.docs.cern.ch/install/configuration/ for the meaning
    # of the variables here

    # generic
    APP_ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]
    SITE_UI_URL = f"https://{env.INVENIO_UI_HOST}:{env.INVENIO_UI_PORT}"
    SITE_API_URL = f"https://{env.INVENIO_API_HOST}:{env.INVENIO_API_PORT}/api"

    # security
    APP_DEFAULT_SECURE_HEADERS = {
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
    RATELIMIT_GUEST_USER = "5000 per hour;500 per minute"
    RATELIMIT_AUTHENTICATED_USER = "20000 per hour;2000 per minute"
    OAUTHCLIENT_REMOTE_APPS = {}  # configure external login providers
    ACCOUNTS_LOGIN_VIEW_FUNCTION = (
        auto_redirect_login  # autoredirect to external login if enabled
    )
    OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True  # autoredirect to external login

    # database
    SQLALCHEMY_DATABASE_URI = (
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
    S3_ENDPOINT_URL = (
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
    SEARCH_UI_SEARCH_TEMPLATE = "invenio_search_ui/search.html"
    SEARCH_UI_SEARCH_VIEW = global_search_view_function
    GLOBAL_SEARCH_MODELS = []

    # caches
    INVENIO_CACHE_TYPE = "redis"
    CACHE_REDIS_URL = (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_CACHE_DB}"
    )
    ACCOUNTS_SESSION_REDIS_URL = (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_SESSION_DB}"
    )
    COMMUNITIES_IDENTITIES_CACHE_REDIS_URL = (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_COMMUNITIES_CACHE_DB}"
    )

    # json schemas for validation
    RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
    RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"
    JSONSCHEMAS_HOST = SITE_UI_URL

    # vocabularies
    from oarepo_vocabularies.resources.config import VocabulariesResourceConfig
    from oarepo_vocabularies.services.config import VocabulariesConfig

    VOCABULARIES_SERVICE_CONFIG = VocabulariesConfig
    VOCABULARIES_RESOURCE_CONFIG = VocabulariesResourceConfig

    # Redis port redirection
    # ---------------------
    CELERY_BROKER_URL = (
        f"amqp://{env.INVENIO_RABBIT_USER}:{env.INVENIO_RABBIT_PASSWORD}"
        f"@{env.INVENIO_RABBIT_HOST}:{env.INVENIO_RABBIT_PORT}/"
    )
    BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = (
        f"redis://{env.INVENIO_REDIS_HOST}:{env.INVENIO_REDIS_PORT}"
        f"/{env.INVENIO_REDIS_CELERY_RESULT_DB}"
    )

    # Instance secret key, used to encrypt stuff (for example, access tokens) inside database
    SECRET_KEY = env.INVENIO_SECRET_KEY

    # hack:
    # Invenio has problems with order of loading templates. If invenio-userprofiles is loaded
    # before invenio-theme, the userprofile page will not work because base settings page
    # will be taken from userprofiles/semantic-ui/userprofiles/settings/base.html which is faulty.
    # If invenio-theme is loaded first, SETTINGS_TEMPLATE is filled, then userprofiles will use
    # it and the UI loads correctly.
    #
    # This line just makes sure that SETTINGS_TEMPLATE is always set up.
    SETTINGS_TEMPLATE = "invenio_theme/page_settings.html"

    # ui
    APP_THEME = [code, "oarepo", "semantic-ui"]
    INSTANCE_THEME_FILE = "./less/theme.less"
    APP_DEFAULT_SECURE_HEADERS["content_security_policy"]["default-src"].append(
        # hack for displaying images from another source (this one is for licenses specifically)
        "https://licensebuttons.net/"
    )

    THEME_HEADER_TEMPLATE = "header.html"
    THEME_FOOTER_TEMPLATE = "footer.html"
    THEME_JAVASCRIPT_TEMPLATE = "base/javascript.html"
    THEME_TRACKINGCODE_TEMPLATE = "oarepo_ui/trackingcode.html"
    THEME_CSS_TEMPLATE = "base/css.html"

    # remove when you create your own title page
    THEME_FRONTPAGE = False

    # Header logo
    THEME_LOGO = "images/logo-invenio-white.svg"

    THEME_SITENAME = _(name)
    THEME_FRONTPAGE_TITLE = name
    THEME_FRONTPAGE_TEMPLATE = "frontpage.html"
    THEME_FRONTPAGE_LOGO = None

    REPOSITORY_NAME = name
    REPOSITORY_DESCRIPTION = description

    # We set this to avoid bug: https://github.com/inveniosoftware/invenio-administration/issues/180
    THEME_HEADER_LOGIN_TEMPLATE = "header_login.html"

    BASE_TEMPLATE = "oarepo_ui/base_page.html"

    WEBPACKEXT_PROJECT = "oarepo_ui.webpack:project"

    # RDM
    INVENIO_RDM_ENABLED = True
    RDM_PERSISTENT_IDENTIFIERS = {}
    RDM_USER_MODERATION_ENABLED = False
    RDM_RECORDS_ALLOW_RESTRICTION_AFTER_GRACE_PERIOD = False
    RDM_ALLOW_METADATA_ONLY_RECORDS = True
    RDM_DEFAULT_FILES_ENABLED = False
    RDM_SEARCH_SORT_BY_VERIFIED = False
    RDM_RECORDS_RESTRICTION_GRACE_PERIOD = timedelta(days=30)
    """Grace period for changing record access to restricted."""

    set_constants_in_caller(locals())
