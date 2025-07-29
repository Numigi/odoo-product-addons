# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductBrand(models.Model):

    _inherit = "product.brand"

    active = fields.Boolean(string="Active", default=True)
