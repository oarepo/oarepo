from oarepo.config.base import set_constants_in_caller
from invenio_rdm_records.notifications.builders import GrantUserAccessNotificationBuilder
from invenio_records_resources.references.entity_resolvers.results import ServiceResultResolver
from datasets.records.resolvers import RecordByPIDServiceResultResolver
from invenio_notifications.backends.email import EmailNotificationBackend

# todo: in most repositories these are loaded from requests
# the same for entity_resolvers
# do we need this?
def configure_notifications(builders=None, backends=None):
    NOTIFICATIONS_BUILDERS = {
        # Grant user access
        GrantUserAccessNotificationBuilder.type: GrantUserAccessNotificationBuilder,
    }
    NOTIFICATIONS_ENTITY_RESOLVERS = [
            ServiceResultResolver(service_id="users", type_key="user"),
            RecordByPIDServiceResultResolver(service_id="datasets", type_key="datasets")
        ]


    NOTIFICATIONS_BACKENDS = backends or {
        EmailNotificationBackend.id: EmailNotificationBackend(),
    }

    set_constants_in_caller(locals())