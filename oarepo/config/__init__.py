"""Helper classes for better invenio.cfg config file.

To use the configuration, you need to put the following to invenio.cfg:

from invenio_i18n import lazy_gettext as _
from oarepo import config

# glitchtip for reporting incidents
config.initialize_glitchtip()

# i18n
config.initialize_i18n()

env = config.load_configuration_variables()

config.configure_generic_parameters(
    env,
    code="myrepo",
    name=_("My repository"),
    description=_("Description of my repository"),
)

# use the config.<something> here to create high-level configuration of the repository
# or use CONFIG_VARIABLE=VALUE to directly set the configuration variables

config.register_workflow(...)
config.configure_cron(...)
config.configure_vocabulary(...)
config.add_model(...)

"""

try:
    from oarepo_glitchtip import initialize_glitchtip
except ImportError:

    def initialize_glitchtip(
        dsn: str | None = None, deployment_version: str | None = None
    ) -> None:
        raise ImportError("oarepo-glitchtip is not installed")


from .base import load_configuration_variables
from .communities import configure_communities
from .cron import configure_cron
from .generic_parameters import configure_generic_parameters
from .i18n import initialize_i18n
from .models import add_model
from .vocabulary import configure_vocabulary
from .workflows import register_workflow

__all__ = [
    "configure_generic_parameters",
    "initialize_i18n",
    "initialize_glitchtip",
    "register_workflow",
    "configure_cron",
    "configure_vocabulary",
    "add_model",
    "configure_communities",
    "load_configuration_variables",
]
