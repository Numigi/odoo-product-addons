# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from odoo import api, SUPERUSER_ID


def _update_data_translation(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.translation"].search(
        [
            ("src", "=", "Development"),
            ("module", "=", "product_state"),
            ("state", "=", "translated"),
            ("lang", "=", "fr_FR"),
        ]
    ).write({"value": "Développement"})
    env["ir.translation"].search(
        [
            ("src", "=", "Regular"),
            ("module", "=", "product_state"),
            ("state", "=", "translated"),
            ("lang", "=", "fr_FR"),
        ]
    ).write({"value": "Régulier"})
