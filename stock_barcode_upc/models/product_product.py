# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def get_all_products_by_barcode(self):
        res = super().get_all_products_by_barcode()
        products = self.search_read(
            [("upc", "!=", None), ("type", "!=", "service")],
            ["upc", "display_name", "uom_id", "tracking"],
        )
        products_by_upc = {
            product.pop("upc"): product
            for product in products
            if product["upc"] not in res
        }
        res.update(products_by_upc)
        return res
