from __future__ import annotations
from typing import TYPE_CHECKING


from invenio_i18n import lazy_gettext as _
from .base import get_constant_from_caller, load_configuration_variables, set_constants_in_caller

if TYPE_CHECKING:
    from typing import Any


def configure_ui(
    code="myrepo",
    name=_("My Repository"),
    description="",
    use_default_frontpage=False,
    show_frontpage_intro=False,
    analytics=False,
    languages=(("cs", _("Czech")),),
) -> None:
    env = load_configuration_variables()
    
    DEPLOYMENT_VERSION = env.get("INVENIO_DEPLOYMENT_VERSION", "local development") 

    APP_THEME = [code, "oarepo", "semantic-ui"]
    APP_DEFAULT_SECURE_HEADERS: dict[str, Any] = get_constant_from_caller(
        "APP_DEFAULT_SECURE_HEADERS", {}
    )
    APP_DEFAULT_SECURE_HEADERS["content_security_policy"]["default-src"].append(
        # hack for displaying images from another source (this one is for licenses specifically)
        "https://licensebuttons.net/"
    )

    INSTANCE_THEME_FILE = "./less/theme.less"

    # Template config
    BASE_TEMPLATE = "page.html"
    ADMINISTRATION_THEME_BASE_TEMPLATE = "invenio_app_rdm/administration_page.html"
    COVER_TEMPLATE = "invenio_app_rdm/page_cover.html"
    THEME_CSS_TEMPLATE = "css.html"
    THEME_JAVASCRIPT_TEMPLATE = "javascript.html"
    HEADER_TEMPLATE = "header.html"
    THEME_HEADER_TEMPLATE = "header.html"
    THEME_HEADER_LOGIN_TEMPLATE="invenio_app_rdm/header_login.html"
    THEME_FOOTER_TEMPLATE = "footer.html"
    THEME_TRACKINGCODE_TEMPLATE = "oarepo_ui/trackingcode.html"
    THEME_FRONTPAGE_TEMPLATE = "frontpage.html"
    """Front page intro section visibility"""

    # hack:
    # Invenio has problems with order of loading templates. If invenio-userprofiles is loaded
    # before invenio-theme, the userprofile page will not work because base settings page
    # will be taken from userprofiles/semantic-ui/userprofiles/settings/base.html which is faulty.
    # If invenio-theme is loaded first, SETTINGS_TEMPLATE is filled, then userprofiles will use
    # it and the UI loads correctly.
    # This line just makes sure that SETTINGS_TEMPLATE and HEADER_TEMPLATE is always set up.
    SETTINGS_TEMPLATE = "invenio_theme/page_settings.html"
    HEADER_TEMPLATE = "invenio_theme/header.html"
    SEARCH_UI_SEARCH_TEMPLATE = "invenio_app_rdm/records/search.html"

    if analytics and analytics == "matomo" and DEPLOYMENT_VERSION != "local development":
        MATOMO_ANALYTICS_TEMPLATE = "oarepo_ui/matomo_analytics.html"
        MATOMO_ANALYTICS_URL = env.INVENIO_MATOMO_ANALYTICS_URL
        MATOMO_ANALYTICS_SITE_ID = env.INVENIO_MATOMO_ANALYTICS_SITE_ID
        APP_DEFAULT_SECURE_HEADERS["content_security_policy"]["default-src"].append(
            env.INVENIO_MATOMO_ANALYTICS_URL
        )


    # UI Branding & copywriting
    THEME_FRONTPAGE = use_default_frontpage
    THEME_LOGO = "images/invenio-rdm.svg"
    THEME_FRONTPAGE_LOGO = None
    THEME_SITENAME = _(name)
    THEME_FRONTPAGE_TITLE = name
    THEME_SHOW_FRONTPAGE_INTRO_SECTION = show_frontpage_intro
    REPOSITORY_NAME = name
    REPOSITORY_DESCRIPTION = description

    # Build pipeline config
    JAVASCRIPT_PACKAGES_MANAGER = "pnpm"
    ASSETS_BUILDER = "rspack"
    WEBPACKEXT_NPM_PKG_CLS = "pynpm:PNPMPackage"
    WEBPACKEXT_PROJECT = "oarepo_ui.webpack:project"

    # Do not add default records UI as we provide our own compatibility layer
    RECORDS_UI_ENDPOINTS = []

    # TODO: uncomment when certain route is registered to some UI blueprint
    # or move to oarepo-rdm?
    # Not everything could be directly used RN
    APP_RDM_ROUTES = {
        "index": "/",
        "robots": "/robots.txt",
        "help_search": "/help/search",
        # "help_statistics": "/help/statistics",
        # "help_versioning": "/help/versioning",
        # "record_search": "/search",
        "record_detail": "/records/<pid_value>",
        # "record_export": "/records/<pid_value>/export/<export_format>",
        # "record_file_preview": "/records/<pid_value>/preview/<path:filename>",
        # "record_file_download": "/records/<pid_value>/files/<path:filename>",
        # "record_thumbnail": "/records/<pid_value>/thumb<int:size>",
        # "record_media_file_download": "/records/<pid_value>/media-files/<path:filename>",
        # "record_from_pid": "/<any({schemes}):pid_scheme>/<path:pid_value>",
        # "record_latest": "/records/<pid_value>/latest",
        # "dashboard_home": "/me",
        # "deposit_create": "/uploads/new",
        # "deposit_edit": "/uploads/<pid_value>",
    }
    """RDM blueprint routes."""

    set_constants_in_caller(locals())