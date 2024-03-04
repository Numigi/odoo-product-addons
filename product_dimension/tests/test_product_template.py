# © 2017 Savoir-faire Linux
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProductTemplate(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gram = cls.env.ref('uom.product_uom_gram')
        cls.kg = cls.env.ref('uom.product_uom_kgm')
        cls.cm = cls.env.ref('uom.product_uom_cm')

        cls.height = 30
        cls.length = 40
        cls.width = 50
        cls.weight = 1
        cls.weight_in_uom = 1000
        cls.volume = 0.3 * 0.4 * 0.5
        cls.density = cls.weight / cls.volume

    def test_create_product_template_with_dimensions_propagated_to_variant(self):
        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'height': self.height,
            'length': self.length,
            'width': self.width,
            'dimension_uom_id': self.cm.id,
        })

        self.template.refresh()
        self.assertEqual(self.template.height, self.height)
        self.assertEqual(self.template.length, self.length)
        self.assertEqual(self.template.width, self.width)
        self.assertEqual(self.template.dimension_uom_id, self.cm)

        self.assertEqual(self.template.product_variant_ids.height, self.height)
        self.assertEqual(self.template.product_variant_ids.length, self.length)
        self.assertEqual(self.template.product_variant_ids.width, self.width)
        self.assertEqual(self.template.product_variant_ids.dimension_uom_id, self.cm)

    def test_create_product_template_with_weight_uom_propagated_to_variant(self):
        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'weight_in_uom': self.weight_in_uom,
            'specific_weight_uom_id': self.gram.id,
        })

        self.template.refresh()
        self.assertEqual(self.template.weight_in_uom, self.weight_in_uom)
        self.assertEqual(self.template.specific_weight_uom_id, self.gram)
        self.assertEqual(self.template.weight, self.weight)

        self.assertEqual(
            self.template.product_variant_ids.weight_in_uom, self.weight_in_uom
        )
        self.assertEqual(
            self.template.product_variant_ids.specific_weight_uom_id, self.gram
        )
        self.assertEqual(self.template.product_variant_ids.weight, self.weight)

    def test_create_product_template_with_weight_propagated_to_variant(self):
        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'weight': 1,
        })

        self.template.refresh()
        self.assertEqual(self.template.weight_in_uom, 1)
        self.assertEqual(self.template.specific_weight_uom_id, self.kg)
        self.assertEqual(self.template.weight, 1)

        self.assertEqual(self.template.product_variant_ids.weight_in_uom, 1)
        self.assertEqual(
            self.template.product_variant_ids.specific_weight_uom_id, self.kg
        )
        self.assertEqual(self.template.product_variant_ids.weight, 1)

    def test_create_product_template_with_volume_computed_on_variant(self):
        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'height': self.height,
            'length': self.length,
            'width': self.width,
            'dimension_uom_id': self.cm.id,
        })

        self.template.refresh()

        self.assertAlmostEqual(self.template.volume, self.volume, 2)
        self.assertAlmostEqual(self.template.product_variant_ids.volume, self.volume, 2)

    def test_create_product_template_then_density_computed_on_variant(self):
        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'weight_in_uom': self.weight_in_uom,
            'specific_weight_uom_id': self.gram.id,
            'height': self.height,
            'length': self.length,
            'width': self.width,
            'dimension_uom_id': self.cm.id,
        })

        self.template.refresh()

        self.assertAlmostEqual(self.template.density, self.density, 2)
        self.assertAlmostEqual(
            self.template.product_variant_ids.density, self.density, 2
        )
