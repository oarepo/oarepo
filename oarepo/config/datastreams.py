from typing import Any

from invenio_base.utils import obj_or_import_string
from oarepo.config.base import set_constants_in_caller, get_constant_from_caller, merge_with_caller


def configure_datastreams(readers: dict[str, Any] | None = None, writers: dict[str, Any] | None = None,
                          transformers: dict[str, Any] | None = None)->None:
    # can't move into a function cause of constant_from_caller methods
    if readers:
        objs = {k: obj_or_import_string(v) for k, v in readers.items()}
        VOCABULARIES_DATASTREAM_READERS = merge_with_caller("VOCABULARIES_DATASTREAM_READERS", objs)

    if writers:
        objs = {k: obj_or_import_string(v) for k, v in writers.items()}
        VOCABULARIES_DATASTREAM_WRITERS = merge_with_caller("VOCABULARIES_DATASTREAM_WRITERS", objs)

    if transformers:
        objs = {k: obj_or_import_string(v) for k, v in transformers.items()}
        VOCABULARIES_DATASTREAM_TRANSFORMERS = merge_with_caller("VOCABULARIES_DATASTREAM_TRANSFORMERS", objs)
    set_constants_in_caller(locals())