from invenio_app_rdm import config as app_rdm_config

from oarepo import initial_rdm_config as config


def test_flavour_defaults_follow_upstream():
    assert config.MAX_CONTENT_LENGTH == app_rdm_config.MAX_CONTENT_LENGTH
    assert config.FILES_REST_PERMISSION_FACTORY is app_rdm_config.files_rest_permission_factory
    assert config.APP_RDM_RECORD_THUMBNAIL_SIZES == app_rdm_config.APP_RDM_RECORD_THUMBNAIL_SIZES
    assert config.COMMUNITIES_ERROR_HANDLERS == app_rdm_config.COMMUNITIES_ERROR_HANDLERS
    assert config.REQUESTS_ERROR_HANDLERS == app_rdm_config.REQUESTS_ERROR_HANDLERS
    assert config.USERS_RESOURCES_SERVICE_SCHEMA is app_rdm_config.USERS_RESOURCES_SERVICE_SCHEMA
    assert config.ACCOUNTS_USER_PREFERENCES_SCHEMA is app_rdm_config.ACCOUNTS_USER_PREFERENCES_SCHEMA


def test_endpoint_rate_limits_keep_the_local_login_ones():
    assert config.RATELIMIT_PER_ENDPOINT["security.login"]
    assert config.RATELIMIT_PER_ENDPOINT["invenio_oauthclient.login"]


def test_defaults_do_not_share_state_with_upstream():
    # mutating a default in invenio.cfg must not leak into invenio_app_rdm.config
    for name in (
        "COMMUNITIES_ERROR_HANDLERS",
        "REQUESTS_ERROR_HANDLERS",
        "APP_RDM_RECORD_THUMBNAIL_SIZES",
        "FORMATTER_BADGES_ALLOWED_TITLES",
        "FORMATTER_BADGES_TITLE_MAPPING",
    ):
        assert getattr(config, name) is not getattr(app_rdm_config, name), name


def test_enforcing_defaults_are_left_to_oarepo_config():
    # these would change the behaviour of every library's test suite
    for name in (
        "REST_CSRF_ENABLED",
        "ACCESS_CACHE",
        "ACCOUNTS_LOGIN_RATELIMIT",
        "SQLALCHEMY_ENGINE_OPTIONS",
        "DB_VERSIONING_USER_MODEL",
    ):
        assert not hasattr(config, name), name


def test_administration_versions():
    assert [package for package, _ in config.ADMINISTRATION_DISPLAY_VERSIONS][-1] == "invenio-app-rdm"
