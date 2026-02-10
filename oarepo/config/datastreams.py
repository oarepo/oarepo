from typing import Any

from invenio_base.utils import obj_or_import_string
from oarepo.config.base import set_constants_in_caller, get_constant_from_caller



def configure_datastreams(readers: dict[str, Any] | None = None, writers: dict[str, Any] | None = None,
                          transformers: dict[str, Any] | None = None)->None:
    # can't move into a function cause of constant_from_caller methods
    if readers:
        objs = {k: obj_or_import_string(v) for k, v in readers.items()}
        var_name = "VOCABULARIES_DATASTREAM_READERS"
        original_objs = get_constant_from_caller(var_name)
        set_constants_in_caller({var_name: {**original_objs, **objs}})

    if writers:
        objs = {k: obj_or_import_string(v) for k, v in writers.items()}
        var_name = "VOCABULARIES_DATASTREAM_WRITERS"
        original_objs = get_constant_from_caller(var_name)
        set_constants_in_caller({var_name: {**original_objs, **objs}})

    if transformers:
        objs = {k: obj_or_import_string(v) for k, v in transformers.items()}
        var_name = "VOCABULARIES_DATASTREAM_TRANSFORMERS"
        original_objs = get_constant_from_caller(var_name)
        set_constants_in_caller({var_name: {**original_objs, **objs}})