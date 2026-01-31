from invenio_app_rdm import config as rdm_config

from oarepo.config.base import set_constants_in_caller

"""
config.configure_datastream_readers(catch_all=CatchAllReader, zenodo=ZenodoReader)
config.configure_datastream_transformers(catch_all=CatchAllTransformer, zenode=ZenodoTransformer,
                        lindat=LindatTransformerm, id_from_doi=IdFromDOITransformer)
"""



def _transform_datastream_cfg(type_, add_rdm, catch_all, zenodo, lindat, id_from_doi,
                                 **kwargs):
    cfg = {}
    if catch_all:
        cfg["catch-all"] = catch_all
    if zenodo:
        cfg["zenodo"] = zenodo
    if lindat:
        cfg["lindat"] = lindat
    if id_from_doi:
        cfg["id-from-doi"] = id_from_doi
    cfg |= {k.replace("_", "-"): v for k, v in kwargs.items()}
    if add_rdm:
        cfg |= getattr(rdm_config, f"VOCABULARIES_DATASTREAM_{type_.upper()}")
    set_constants_in_caller(cfg)

def configure_datastream_readers(add_rdm=None, catch_all=None, zenodo=None, lindat=None, id_from_doi=None,
                                 **kwargs):
    _transform_datastream_cfg("READERS", add_rdm, catch_all, zenodo, lindat, id_from_doi, **kwargs)


def configure_datastream_writers(add_rdm=None, catch_all=None, zenodo=None, lindat=None, id_from_doi=None,
                                 **kwargs):
    _transform_datastream_cfg("WRITERS", add_rdm, catch_all, zenodo, lindat, id_from_doi, **kwargs)


def configure_datastream_transformers(add_rdm=None, catch_all=None, zenodo=None, lindat=None, id_from_doi=None,
                                 **kwargs):
    _transform_datastream_cfg("TRANSFORMERS", add_rdm, catch_all, zenodo, lindat, id_from_doi, **kwargs)
