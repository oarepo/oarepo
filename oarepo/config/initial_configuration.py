"""This module provides initial configuration for OARepo-based repositories.

It is registered as invenio_config.module entrypoint so is loaded early in
the application initialization. This allows other modules to access/modify its
configuration options.
"""

THEME_FRONTPAGE = False
"""Enable frontpage theme."""
