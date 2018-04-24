# © 2017 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models


class ProductTemplateWithWeightInKg(models.Model):
    """Rename the field weight to `Weight in Kg`."""

    _inherit = 'product.template'

    weight = fields.Float(string='Weight in Kg')


class ProductTemplateWithWeightInUoM(models.Model):
    """Add the fields weight_in_uom and weight_uom_id to products."""

    _inherit = 'product.template'

    weight_in_uom = fields.Float(
        related='product_variant_ids.weight_in_uom',
        store=True,
    )

    weight_uom_id = fields.Many2one(
        related='product_variant_ids.weight_uom_id',
        store=True,
    )


class ProductTemplateWithDimensions(models.Model):
    """Add dimension fields to products."""

    _inherit = 'product.template'

    height = fields.Float(
        related='product_variant_ids.height',
        store=True,
    )

    length = fields.Float(
        related='product_variant_ids.length',
        store=True,
    )

    width = fields.Float(
        related='product_variant_ids.width',
        store=True,
    )

    dimension_uom_id = fields.Many2one(
        related='product_variant_ids.dimension_uom_id',
        store=True,
    )


class ProductTemplateWithVolumeDecimalPrecision(models.Model):
    """Add a decimal precision to the volume of a product."""

    _inherit = 'product.template'

    volume = fields.Float(digits=dp.get_precision('Product Volume'))


class ProductTemplateWithDensity(models.Model):
    """Add the field density to products."""

    _inherit = 'product.template'

    density = fields.Float(
        'Density',
        related='product_variant_ids.density',
    )
