# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.onchange("is_kit")
    def _onchange_is_kit_set_service(self):
        if self.is_kit:
            self.type = "service"
