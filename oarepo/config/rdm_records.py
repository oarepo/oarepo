import idutils
from invenio_rdm_records.config import always_valid
from invenio_i18n import lazy_gettext as _
from invenio_base.utils import obj_or_import_string
from oarepo.config.base import set_constants_in_caller


def configure_rdm_records(app_rdm_detail_side_bar_templates=None, permission_policy = None):

    RDM_RECORDS_PERSONORG_SCHEMES = {
        "orcid": {"label": _("ORCID"), "validator": idutils.is_orcid, "datacite": "ORCID"},
        "isni": {"label": _("ISNI"), "validator": idutils.is_isni, "datacite": "ISNI"},
        "gnd": {"label": _("GND"), "validator": idutils.is_gnd, "datacite": "GND"},
        "ror": {"label": _("ROR"), "validator": idutils.is_ror, "datacite": "ROR"},
        "researcherid": {
            "label": _("ResearcherID"),
            "validator": always_valid,
            "datacite": "ResearcherID",
        },
        "scopusid": {
            "label": _("Scopus Author ID"),
            "validator": always_valid,
            "datacite": "Scopus Author ID",
        },
        # funders are given crossref DOI, so we need to enable it as well
        "doi": {"label": _("DOI"), "validator": idutils.is_doi, "datacite": "DOI"},
    }

    # separate for ui things?
    APP_RDM_DETAIL_SIDE_BAR_TEMPLATES = app_rdm_detail_side_bar_templates
    APP_RDM_IDENTIFIER_SCHEMES_UI = {
        "orcid": {
            "url_prefix": "http://orcid.org/",
            "icon": "images/orcid.svg",
            "label": "ORCID",
        },
        "ror": {
            "url_prefix": "https://ror.org/",
            "icon": "images/ror-icon.svg",
            "label": "ROR",
        },
        "gnd": {
            "url_prefix": "http://d-nb.info/gnd/",
            "icon": "images/gnd-icon.svg",
            "label": "GND",
        },
    }

    RDM_RECORDS_IDENTIFIERS_SCHEMES = {
        "ark": {"label": _("ARK"), "validator": idutils.is_ark, "datacite": "ARK"},
        "arxiv": {"label": _("arXiv"), "validator": idutils.is_arxiv, "datacite": "arXiv"},
        "ads": {
            "label": _("Bibcode"),
            "validator": idutils.is_ads,
            "datacite": "bibcode",
        },
        "crossreffunderid": {
            "label": _("Crossref Funder ID"),
            "validator": always_valid,
            "datacite": "Crossref Funder ID",
        },
        "doi": {"label": _("DOI"), "validator": idutils.is_doi, "datacite": "DOI"},
        "ean13": {"label": _("EAN13"), "validator": idutils.is_ean13, "datacite": "EAN13"},
        "eissn": {"label": _("EISSN"), "validator": idutils.is_issn, "datacite": "EISSN"},
        "grid": {"label": _("GRID"), "validator": always_valid, "datacite": "GRID"},
        "handle": {
            "label": _("Handle"),
            "validator": idutils.is_handle,
            "datacite": "Handle",
        },
        "igsn": {"label": _("IGSN"), "validator": always_valid, "datacite": "IGSN"},
        "isbn": {"label": _("ISBN"), "validator": idutils.is_isbn, "datacite": "ISBN"},
        "isni": {"label": _("ISNI"), "validator": idutils.is_isni, "datacite": "ISNI"},
        "issn": {"label": _("ISSN"), "validator": idutils.is_issn, "datacite": "ISSN"},
        "istc": {"label": _("ISTC"), "validator": idutils.is_istc, "datacite": "ISTC"},
        "lissn": {"label": _("LISSN"), "validator": idutils.is_issn, "datacite": "LISSN"},
        "lsid": {"label": _("LSID"), "validator": idutils.is_lsid, "datacite": "LSID"},
        "pmid": {"label": _("PMID"), "validator": idutils.is_pmid, "datacite": "PMID"},
        "purl": {"label": _("PURL"), "validator": idutils.is_purl, "datacite": "PURL"},
        "upc": {"label": _("UPC"), "validator": always_valid, "datacite": "UPC"},
        "url": {"label": _("URL"), "validator": idutils.is_url, "datacite": "URL"},
        "urn": {"label": _("URN"), "validator": idutils.is_urn, "datacite": "URN"},
        "w3id": {"label": _("W3ID"), "validator": always_valid, "datacite": "w3id"},
        "other": {"label": _("Other"), "validator": always_valid, "datacite": "Other"},
    }
    """These are used for references, main, alternate and related identifiers."""

    RDM_RECORDS_RELATED_IDENTIFIERS_SCHEMES = RDM_RECORDS_IDENTIFIERS_SCHEMES
    """This variable is used to separate related identifiers."""

    RDM_RECORDS_LOCATION_SCHEMES = {
        "wikidata": {"label": _("Wikidata"), "validator": always_valid},
        "geonames": {"label": _("GeoNames"), "validator": always_valid},
    }

    RDM_CITATION_STYLES = [
        ("iso690-author-date-cs", _("ČSN ISO 690")),
        ("apa", _("APA")),
        ("harvard-cite-them-right", _("Harvard")),
        ("modern-language-association", _("MLA")),
        ("vancouver", _("Vancouver")),
        ("chicago-fullnote-bibliography", _("Chicago")),
        ("ieee", _("IEEE")),
    ]
    """List of citation style """

    RDM_CITATION_STYLES_DEFAULT = "iso690-author-date-cs"
    """Default citation style"""

    # todo: in model?
    RDM_PERMISSION_POLICY = obj_or_import_string(permission_policy)


    set_constants_in_caller(locals())