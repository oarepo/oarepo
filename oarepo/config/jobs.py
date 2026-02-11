from oarepo.config.base import set_constants_in_caller


def configure_jobs(permission_policy=None, logging_level=None):

    from invenio_jobs.services.permissions import (
        JobLogsPermissionPolicy as InvenioJobLogsPermissionPolicy,
    )
    from oarepo_runtime.services.generators import AdministrationWithQueryFilter

    class JobLogsPermissionPolicy(InvenioJobLogsPermissionPolicy):
        """Permission policy for job logs."""

        can_read = [AdministrationWithQueryFilter()]

    # invenio-jobs configuration
    APP_LOGS_PERMISSION_POLICY = permission_policy or JobLogsPermissionPolicy
    JOBS_LOGGING_LEVEL = logging_level or "INFO"
    set_constants_in_caller(locals())
