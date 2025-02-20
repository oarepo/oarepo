from flask_babel import lazy_gettext as _
from marshmallow_i18n_messages import add_i18n_to_marshmallow


def initialize_i18n():
    add_i18n_to_marshmallow(_)
