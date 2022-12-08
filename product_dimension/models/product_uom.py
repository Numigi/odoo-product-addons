# © 2017 Savoir-faire Linux
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductUoMWithHasCategoryLength(models.Model):
    """Add a boolean to isolate units of measure of category length."""

    _inherit = 'uom.uom'

    has_category_length = fields.Boolean(
        'Has Category Length', compute='_compute_has_category_length', store=True)

    @api.depends('category_id')
    def _compute_has_category_length(self):
        category_length = self.env.ref('uom.uom_categ_length')
        for uom in self:
            uom.has_category_length = uom.category_id == category_length


class ProductUoMWithHasCategoryWeight(models.Model):
    """Add a boolean to isolate units of measure of category weight."""

    _inherit = 'uom.uom'

    has_category_weight = fields.Boolean(
        'Has Category Weight', compute='_compute_has_category_weight', store=True)

    @api.depends('category_id')
    def _compute_has_category_weight(self):
        category_weight = self.env.ref('uom.product_uom_categ_kgm')
        for uom in self:
            uom.has_category_weight = uom.category_id == category_weight
