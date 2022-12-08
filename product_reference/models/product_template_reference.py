# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplateReference(models.Model):

    _name = 'product.template.reference'
    _description = 'Product Template Reference'

    reference_type_id = fields.Many2one(
        'product.template.reference.type', 'Type', required=True)
    value = fields.Char('Value', required=True)
    product_id = fields.Many2one('product.template', copy=False)
