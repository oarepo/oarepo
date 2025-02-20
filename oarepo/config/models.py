import logging
from typing import Any

from .base import get_constant_from_caller, set_constants_in_caller

log = logging.getLogger("config.models")


def add_model(model_package_name: str) -> None:
    GLOBAL_SEARCH_MODELS: list[Any] = get_constant_from_caller(
        "GLOBAL_SEARCH_MODELS", []
    )

    try:
        from invenio_base.utils import obj_or_import_string

        model_definition = obj_or_import_string(
            model_package_name + ":" + "MODEL_DEFINITION"
        )
        GLOBAL_SEARCH_MODELS.append(model_definition)
    except ImportError:
        log.error(
            "Could not import model definition from package: %s. Has the model been compiled?",
            model_package_name,
        )
    set_constants_in_caller(locals())
