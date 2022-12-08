# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    upc = fields.Char("UPC", copy=False)

    _sql_constraints = [
        ("upc_uniq", "unique(upc)", "A UPC can only be assigned to one product!")
    ]

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        res = super()._name_search(name, args, operator, limit, name_get_uid)
        if res:
            return res
        args = args or []
        positive_operators = ["=", "ilike", "=ilike", "like", "=like"]
        product_ids = []
        if name and operator in positive_operators:
            product_ids = self._search(
                [("upc", operator, name)] + args, limit=limit, access_rights_uid=name_get_uid
            )
        if product_ids:
            return product_ids
        return res
