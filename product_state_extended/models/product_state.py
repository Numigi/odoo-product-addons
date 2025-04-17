# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    sale_ok = fields.Boolean(string="Can be Sold")
    purchase_ok = fields.Boolean(string="Can be Purchased")
    can_be_rented = fields.Boolean(string="Can be Rented")
    is_kit = fields.Boolean(string="Is a Kit")
    can_be_expensed = fields.Boolean(string="Can be Expensed")
    pack_ok = fields.Boolean(string="Can be a Pack")
