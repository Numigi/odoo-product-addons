# © 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    @api.model
    def get_read_access_actions(self):
        res = super().get_read_access_actions()
        additional_actions = [
            "action_open_quants",
            "action_product_tmpl_forecast_report",
            "action_view_stock_move_lines",
            "action_view_orderpoints",
            "action_open_product_lot",
            "action_view_related_putaway_rules",
        ]
        res.extend(additional_actions)
        return res
