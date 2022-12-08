# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class ProductKitLine(models.Model):

    _name = "product.kit.line"
    _description = "Product Kit Component Line"
    _rec_name = "component_id"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char("Description", translate=True)

    product_template_id = fields.Many2one(
        "product.template", ondelete="cascade", required=True, index=True
    )

    component_id = fields.Many2one("product.product", "Component", ondelete="restrict")

    uom_id = fields.Many2one("uom.uom", "Unit of Measure")

    quantity = fields.Float(
        digits=dp.get_precision("Product Unit of Measure"), default=1
    )

    is_important = fields.Boolean()

    display_type = fields.Selection(
        [("line_section", "Section"), ("line_note", "Note")],
    )

    @api.onchange("component_id")
    def onchange_component(self):
        if self.component_id:
            self._set_default_name()
            self._set_default_uom()

    def _set_default_name(self):
        self.name = self.component_id.get_product_multiline_description_sale()

    def _set_default_uom(self):
        self.uom_id = self.component_id.uom_id

    @api.constrains("component_id", "uom_id")
    def _check_component_uom_category(self):
        for line in self:
            component = line.component_id
            uom = line.uom_id
            if component.uom_id.category_id != uom.category_id:
                raise ValidationError(
                    _(
                        "The component {component} is defined on the kit {kit} "
                        "with the unit of measure {uom}. "
                        "This unit of measure is incompatible with the unit "
                        "of measure defined on the component ({component_uom})."
                    ).format(
                        component=component.display_name,
                        component_uom=component.uom_id.display_name,
                        kit=line.product_template_id.display_name,
                        uom=uom.display_name,
                    )
                )
