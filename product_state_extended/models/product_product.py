# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models, api
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange("product_state_id")
    def _onchange_product_state_id(self):
        # Check if this is a onchange triggered by new create
        # If so, we don't check the user's group and let the default
        # settings to be applied
        if self.create_date:
            if self.env.user.has_group(
                "product_state_extended.group_product_state_manager"
            ):
                self._update_product_value()
            else:
                raise UserError(_("You are not allowed to change the product state."))
        else:
            self.with_context(force_to_default_stage=True)._update_product_value()

    def _update_product_value(self):
        if self._context.get("force_to_default_stage"):
            self.product_state_id = self.env["product.state"].search(
                [("default", "=", True)], limit=1
            )
        if self.product_state_id:
            fields_to_update = [
                "sale_ok",
                "purchase_ok",
                "can_be_rented",
                "is_kit",
                "can_be_expensed",
                "pack_ok",
            ]
            for field in fields_to_update:
                setattr(self, field, getattr(self.product_state_id, field))
