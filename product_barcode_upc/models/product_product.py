# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    upc = fields.Char("UPC", copy=False)

    _sql_constraints = [
        ('upc_uniq', 'unique(upc)', "A UPC can only be assigned to one product!"),
    ]

    @api.model
    def get_all_products_by_barcode(self):
        res = super().get_all_products_by_barcode()
        products = self.search_read(
            [
                ("upc", "not in", list(res.keys())),
                "|",
                ("barcode", "!=", None),
                ("upc", "!=", None),
                ("type", "!=", "service")],
            ["upc", "display_name", "uom_id", "tracking"]
        )
        products_by_upc = {product.pop("upc"): product for product in products}
        res.update(products_by_upc)
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
        product_ids = []
        if name and operator in positive_operators:
            product_ids = self._search([('upc', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
        if product_ids:
            return self.browse(product_ids).name_get()
        else:
            return super()._name_search(name, args, operator, limit, name_get_uid)
