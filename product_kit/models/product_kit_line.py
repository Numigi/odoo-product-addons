# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductKitLine(models.Model):

    _name = "product.kit.line"
    _description = "Product Kit Component Line"
    _rec_name = "component_id"
    _order = "sequence"

    sequence = fields.Integer()

    product_template_id = fields.Many2one(
        "product.template", ondelete="cascade", required=True, index=True
    )

    component_id = fields.Many2one(
        "product.product", "Component", ondelete="restrict", required=True
    )

    is_important = fields.Boolean()
