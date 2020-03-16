# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):

    _inherit = "product.template"

    is_kit = fields.Boolean("Is a Kit")

    kit_line_ids = fields.One2many(
        "product.kit.line", "product_template_id", "Kit Components"
    )

    @api.onchange("is_kit")
    def _onchange_is_kit_set_service(self):
        if self.is_kit:
            self.type = "service"

    @api.constrains("is_kit", "type")
    def _check_kit_must_be_service(self):
        for product in self:
            if product.is_kit and product.type != "service":
                raise ValidationError(
                    _("A kit must strictly be a product of type service.")
                )
