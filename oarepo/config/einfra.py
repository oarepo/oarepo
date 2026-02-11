#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo (see https://github.com/oarepo/oarepo).
#
# oarepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Configuration for oarepo-oidc-einfra module."""
import os
import sys

from .base import load_configuration_variables, set_constants_in_caller


def configure_einfra_oidc() -> None:
    try:
        from oarepo_oidc_einfra import EINFRA_LOGIN_APP
        from oarepo_oidc_einfra import config as oarepo_einfra_config
    except ImportError:
        print("Please install oarepo-oidc-einfra to use E-INFRA OIDC login.")
        sys.exit(1)

    env = load_configuration_variables()
    if os.environ.get("INVENIO_REMOTE_AUTH_ENABLED", "no").lower() in (
        "true",
        "yes",
        "1",
    ):
        OAUTHCLIENT_REMOTE_APPS = {"e-infra": EINFRA_LOGIN_APP}
        # needed for disconnect
        EINFRA = dict(
            consumer_key=env.INVENIO_EINFRA_CONSUMER_KEY,
            consumer_secret=env.INVENIO_EINFRA_CONSUMER_SECRET,
            **{
                k[len("EINFRA_") :].lower(): getattr(oarepo_einfra_config, k)
                for k in dir(oarepo_einfra_config)
                if k.startswith("EINFRA_")
            },
        )
        # do not allow users to change profile info, we take this from EINFRA
        USERPROFILES_READ_ONLY = True
    else:
        OAUTHCLIENT_REMOTE_APPS = {}
    set_constants_in_caller(locals())
