from typing import Any

from .base import get_constant_from_caller, set_constants_in_caller


def configure_vocabulary(code: str, **kwargs: Any) -> None:
    INVENIO_VOCABULARY_TYPE_METADATA = get_constant_from_caller(
        "INVENIO_VOCABULARY_TYPE_METADATA", {}
    )
    INVENIO_VOCABULARY_TYPE_METADATA[code] = kwargs

    set_constants_in_caller(locals())
