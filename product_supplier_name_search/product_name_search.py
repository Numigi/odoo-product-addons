# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.osv.expression import AND


class ProductWithSupplierInfoSearch(models.Model):

    _inherit = "product.product"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super().name_search(name=name, args=args, operator=operator, limit=limit)

        # The module only supports position operators.
        positive_operators = ["=", "ilike", "=ilike", "like", "=like"]
        if operator not in positive_operators:
            return res

        if limit is None or len(res) < limit:
            suppliers = self.env["product.supplierinfo"].search(
                [
                    "|",
                    ("product_code", operator, name),
                    ("product_name", operator, name),
                ]
            )

            if suppliers:
                product_ids_already_found = [p[0] for p in res]
                remaining_limit = limit - len(res) if limit else None
                domain = AND(
                    (
                        args or [],
                        [
                            ("product_tmpl_id.seller_ids", "in", suppliers.ids),
                            ("id", "not in", product_ids_already_found),
                        ],
                    )
                )
                products_from_supplier_info = self.search(domain, limit=remaining_limit)

                res += products_from_supplier_info.name_get()

        return res
