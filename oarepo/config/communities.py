from invenio_administration.generators import Administration
from invenio_communities.generators import (
    CommunityManagersForRole,
)
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_i18n import lazy_gettext as _
from invenio_records_permissions.generators import Disable, SystemProcess
from oarepo_communities.services.permissions.generators import PrimaryCommunityRole

from .base import set_constants_in_caller


class DefaultCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Default Permissions for Community CRUD operations for workflow scenarios."""

    can_create = [Administration(), SystemProcess()]
    can_submit_record = [SystemProcess()]
    can_include_directly = [SystemProcess()]
    can_members_add = [SystemProcess()]
    can_members_search = [
        PrimaryCommunityRole("owner"),
        PrimaryCommunityRole("curator"),
        SystemProcess(),
    ]
    can_members_search_public = [
        PrimaryCommunityRole("owner"),
        PrimaryCommunityRole("curator"),
        SystemProcess(),
    ]
    can_members_update = [
        CommunityManagersForRole(),
        SystemProcess(),
    ]
    can_members_delete = can_members_update
    can_request_membership = [Disable()]


def configure_communities(communities_roles=None):
    COMMUNITIES_REGISTER_UI_BLUEPRINT = False
    COMMUNITIES_PERMISSION_POLICY = DefaultCommunitiesPermissionPolicy
    COMMUNITIES_ROLES = communities_roles or [
        # note: order matters, roles should be sorted by importance
        # from the most important to the least
        dict(
            name="owner",
            title=_("Community owner"),
            description=_("Can manage community."),
            is_owner=True,
            can_manage=True,
            can_manage_roles=["owner", "curator", "member"],
        ),
        dict(
            name="curator",
            title=_("Curator"),
            description=_("Can curate records."),
            can_manage=True,
            # NTK decision: curator should NOT be able to manage curators
            can_manage_roles=["member"],
        ),
        dict(
            name="member",
            title=_("Member"),
            description=_("Community member with read permissions."),
        ),
    ]
    set_constants_in_caller(locals())
