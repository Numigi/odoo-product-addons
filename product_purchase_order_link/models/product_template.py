# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    purchase_quotation_count = fields.Integer(compute="_compute_purchase_order_count")

    purchase_order_count = fields.Integer(compute="_compute_purchase_order_count")

    def _compute_purchase_order_count(self):
        for product in self:
            domain = self._get_purchase_order_domain()
            orders = self.env["purchase.order"].search(domain)
            quotations = orders.filtered(
                lambda o: o.state in ("draft", "sent", "to approve")
            )
            product.purchase_quotation_count = len(quotations)
            product.purchase_order_count = len(orders - quotations)

    def open_purchase_quotation_list(self):
        action = self.env.ref("purchase.purchase_rfq").read()[0]
        action["domain"] = self._get_purchase_order_domain()
        action["context"] = {"search_default_draft": True}
        return action

    def open_purchase_order_list(self):
        action = self.env.ref("purchase.purchase_form_action").read()[0]
        action["domain"] = self._get_purchase_order_domain()
        action["context"] = {"search_default_approved": True}
        return action

    def _get_purchase_order_domain(self):
        return [("order_line.product_id", "in", self.product_variant_ids.ids)]


class ProductProduct(models.Model):

    _inherit = "product.product"

    purchase_quotation_count = fields.Integer(compute="_compute_purchase_order_count")

    purchase_order_count = fields.Integer(compute="_compute_purchase_order_count")

    _compute_purchase_order_count = ProductTemplate._compute_purchase_order_count
    open_purchase_quotation_list = ProductTemplate.open_purchase_quotation_list
    open_purchase_order_list = ProductTemplate.open_purchase_order_list

    def _get_purchase_order_domain(self):
        return [("order_line.product_id", "in", self.ids)]
