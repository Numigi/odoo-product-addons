# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dangerous_good = fields.Boolean(string="Is a Dangerous Good")
    un_number = fields.Char(string="UN Number")
    shipping_name = fields.Char()
    hazard_class = fields.Selection(
        selection=[
            ("class_1", "Class 1 Explosives"),
            ("class_2", "Class 2 Gases"),
            ("class_3", "Class 3 Flammable Liquids"),
            ("class_4", "Class 4 Substances / Products"),
            ("class_5", "Class 5 Oxidizing Substances"),
            ("class_6", "Class 6 Toxic and Infectious Substances"),
            ("class_7", "Class 7 Radioactive Materials"),
            ("class_8", "Class 8 Corrosive Substances"),
            ("class_9", "Class 9 Miscellaneous Products, Substances or Organisms"),
        ]
    )
    packing_group = fields.Selection(
        selection=[("I", "I"), ("II", "II"), ("III", "III")]
    )
    dangerous_good_notes = fields.Text()
