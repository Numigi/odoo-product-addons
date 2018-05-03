# © 2017 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProduct(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Test product',
            'type': 'product',
            'height': 2 * 100,
            'length': 3 * 100,
            'width': 5 * 100,
            'dimension_uom_id': cls.env.ref('product.product_uom_cm').id,
            'weight': 120,
        })

    def test_compute_volume(self):
        """Test that the volume is equal to height * length * width."""
        self.assertEqual(self.product.volume, 30)

    def test_compute_density(self):
        """Test that the density is equal to weigth / volume."""
        self.assertEqual(self.product.density, 4)

    def test_if_volume_is_very_low_then_density_is_not_null(self):
        """Check that the precision in units of measure has no impact on the density."""
        self.product.write({
            'height': 1,
            'length': 1,
            'width': 1,
            'dimension_uom_id': self.env.ref('product.product_uom_cm').id,
            'weight': 1,
        })
        self.assertAlmostEqual(self.product.density, 1 / (0.01 * 0.01 * 0.01))

    def test_height_is_not_negative(self):
        with self.assertRaises(ValidationError):
            self.product.height = -10

    def test_length_is_not_negative(self):
        with self.assertRaises(ValidationError):
            self.product.length = -10

    def test_width_is_not_negative(self):
        with self.assertRaises(ValidationError):
            self.product.width = -10

    def test_weight_is_not_negative(self):
        with self.assertRaises(ValidationError):
            self.product.weight = -10

    def test_on_template_write_set_variant_dimensions(self):
        """Test that on write, the dimensions are correctly set on the related variant.

        This feature only supports products with a single variant.

        In the form view of products with multiple variants, the fields are invisible
        and thus, the user must set the values directly on the variant.
        """
        self.product.product_tmpl_id.write({
            'height': 1,
            'length': 2,
            'width': 3,
        })
        self.product.refresh()
        self.assertEqual(self.product.height, 1)
        self.assertEqual(self.product.length, 2)
        self.assertEqual(self.product.width, 3)

        self.assertEqual(self.product.product_tmpl_id.height, 1)
        self.assertEqual(self.product.product_tmpl_id.length, 2)
        self.assertEqual(self.product.product_tmpl_id.width, 3)

    def test_compute_volume_on_product_template(self):
        """Test that the volume is computed correctly on a product template."""
        self.product.write({
            'height': 1,
            'length': 2,
            'width': 3,
            'dimension_uom_id': self.env.ref('product.product_uom_meter').id,
        })

        template = self.product.product_tmpl_id
        self.assertEqual(template.volume, 1 * 2 * 3)

    def test_compute_density_on_product_template(self):
        """Test that the density is computed correctly on a product template."""
        self.product.write({
            'height': 1,
            'length': 2,
            'width': 3,
            'dimension_uom_id': self.env.ref('product.product_uom_meter').id,
            'weight': 60,
        })

        template = self.product.product_tmpl_id
        self.assertEqual(template.density, 60 / (1 * 2 * 3))
