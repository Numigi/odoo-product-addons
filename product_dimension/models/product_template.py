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
    """Add the fields weight_in_uom and specific_weight_uom_id to products."""

    _inherit = 'product.template'

    weight_in_uom = fields.Float(
        related='product_variant_ids.weight_in_uom',
        readonly=False,
        store=True,
    )

    specific_weight_uom_id = fields.Many2one(
        related='product_variant_ids.specific_weight_uom_id',
        readonly=False,
        store=True,
    )


class ProductTemplateWithDimensions(models.Model):
    """Add dimension fields to products."""

    _inherit = 'product.template'

    height = fields.Float(
        related='product_variant_ids.height',
        readonly=False,
        store=True,
    )

    length = fields.Float(
        related='product_variant_ids.length',
        readonly=False,
        store=True,
    )

    width = fields.Float(
        related='product_variant_ids.width',
        readonly=False,
        store=True,
    )

    dimension_uom_id = fields.Many2one(
        related='product_variant_ids.dimension_uom_id',
        readonly=False,
        store=True,
    )


class ProductTemplatePropagateFieldsOnCreate(models.Model):
    """Properly save dimensions on the variant when creating a product template.

    At the creation of the product template, the related field values are not passed
    over to the related variant, because the variant is created after the template.

    Therefore, those fields need to be propagated to the variant after the create process.
    """

    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        template = super().create(vals)

        fields_to_propagate = (
            'weight_in_uom', 'specific_weight_uom_id',
            'height', 'length', 'width', 'dimension_uom_id',
        )

        vals_to_propagate = {k: v for k, v in vals.items() if k in fields_to_propagate}

        for variant in template.product_variant_ids:
            # Only write values that are different from the variant's default value.
            changed_values_to_propagate = {
                k: v for k, v in vals_to_propagate.items()
                if (v or variant[k]) and v != variant[k]
            }
            variant.write(changed_values_to_propagate)

        return template


class ProductTemplateWithVolumeRelated(models.Model):
    """Make the volume related to the volume on the variant.

    In the odoo source code, the field volume is computed instead of related.

    The problem is that when the volume is recomputed on product.product
    (because a dimension changes), the new volume is not propagated to product.template.

    In other words, the following use of api.depends:

        @api.depends('product_variant_ids', 'product_variant_ids.volume')

    does not work if volume is computed (even if it is stored).
    """

    _inherit = 'product.template'

    volume = fields.Float(
        related='product_variant_ids.volume',
        store=True,
    )


class ProductTemplateWithDensity(models.Model):
    """Add the field density to products."""

    _inherit = 'product.template'

    density = fields.Float(
        'Density',
        related='product_variant_ids.density',
        store=True,
    )
