import inspect

from flask_babel import LazyString
from invenio_base.utils import obj_or_import_string
from oarepo_workflows import WorkflowRequestPolicy
from oarepo_workflows.services.permissions import DefaultWorkflowPermissions

from .base import get_constant_from_caller, set_constants_in_caller


def register_workflow(
    workflow_code: str,
    workflow_name: "str | LazyString",
    permissions_policy: "str | DefaultWorkflowPermissions",
    requests_policy: "str | WorkflowRequestPolicy",
):
    from flask_babel import lazy_gettext as _
    from oarepo_requests.services.permissions.workflow_policies import (
        CreatorsFromWorkflowRequestsPermissionPolicy,
    )
    from oarepo_workflows import Workflow

    WORKFLOWS = get_constant_from_caller("WORKFLOWS", {})
    permission_policy_cls = obj_or_import_string(permissions_policy)
    assert inspect.isclass(permission_policy_cls) and issubclass(
        permission_policy_cls, DefaultWorkflowPermissions
    )

    requests_policy_cls = obj_or_import_string(requests_policy)
    assert inspect.isclass(requests_policy_cls) and issubclass(
        requests_policy_cls, WorkflowRequestPolicy
    )

    WORKFLOWS[workflow_code] = Workflow(
        label=_(workflow_name),
        permission_policy_cls=permission_policy_cls,
        request_policy_cls=requests_policy_cls,
    )
    REQUESTS_PERMISSION_POLICY = get_constant_from_caller(
        "REQUESTS_PERMISSION_POLICY", CreatorsFromWorkflowRequestsPermissionPolicy
    )
    set_constants_in_caller(locals())
