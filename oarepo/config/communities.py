from invenio_i18n import lazy_gettext as _

from .base import set_constants_in_caller


def configure_communities(communities_roles=None):
    COMMUNITIES_REGISTER_UI_BLUEPRINT = False
    COMMUNITIES_ROLES = communities_roles or [
        # note: order matters, roles should be sorted by importance
        # from the most important to the least
        dict(
            name="owner",
            title=_("Community owner"),
            description=_("Can manage community."),
            is_owner=True,
            can_manage=True,
            can_manage_roles=["owner", "curator", "submitter", "member"],
        ),
        dict(
            name="curator",
            title=_("Curator"),
            description=_("Can curate records."),
            can_manage=True,
            # NTK decision: curator should NOT be able to manage curators
            can_manage_roles=["submitter", "member"],
        ),
        dict(
            name="member",
            title=_("Member"),
            description=_("Community member with read permissions."),
        ),
    ]
    set_constants_in_caller(locals())
