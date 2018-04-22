# © 2017 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProductWeightInUoM(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
        })

        cls.gram = cls.env.ref('product.product_uom_gram')
        cls.kg = cls.env.ref('product.product_uom_kgm')

    def test_when_update_weight_then_weight_in_uom_is_updated(self):
        """Test that when the weight is set, then the weight in uom is also updated."""
        self.product.weight = 10

        self.product.refresh()
        self.assertEqual(self.product.weight, 10)
        self.assertEqual(self.product.weight_in_uom, 10)
        self.assertEqual(self.product.weight_uom_id, self.kg)

    def test_when_update_weight_if_has_weight_uom_then_weight_uom_id_is_not_changed(self):
        """Test that when the weight is set, the current uom on the product is kept."""
        self.product.weight_uom_id = self.gram

        self.product.weight = 10

        self.product.refresh()
        self.assertEqual(self.product.weight, 10)
        self.assertEqual(self.product.weight_in_uom, 10 * 1000)
        self.assertEqual(self.product.weight_uom_id, self.gram)

    def test_when_update_weight_in_uom_then_weight_is_updated(self):
        """Test that when the weight in uom is set, then the weight in kg is also updated."""
        self.product.write({
            'weight_in_uom': 10 * 1000,
            'weight_uom_id': self.gram.id,
        })

        self.product.refresh()
        self.assertEqual(self.product.weight, 10)
        self.assertEqual(self.product.weight_in_uom, 10 * 1000)
        self.assertEqual(self.product.weight_uom_id, self.gram)

    def test_on_write_weight_in_uom_supersedes_weight(self):
        """Test that on write, if weight and weight_in_uom are given, weight_in_uom is kept."""
        self.product.write({
            'weight': 9,
            'weight_in_uom': 10 * 1000,
            'weight_uom_id': self.gram.id,
        })

        self.product.refresh()
        self.assertEqual(self.product.weight, 10)
        self.assertEqual(self.product.weight_in_uom, 10 * 1000)
        self.assertEqual(self.product.weight_uom_id, self.gram)

    def test_on_create_if_weight_is_given_then_weight_in_uom_is_set(self):
        """Test that on create, if weight is given, then weight in uom is set."""
        product = self.env['product.product'].create({
            'name': 'New Product',
            'type': 'product',
            'weight': 10,
        })

        product.refresh()
        self.assertEqual(product.weight, 10)
        self.assertEqual(product.weight_in_uom, 10)
        self.assertEqual(product.weight_uom_id, self.kg)

    def test_on_create_if_weight_in_uom_is_given_then_weight_is_set(self):
        """Test that on create, if weight is given, then weight in uom is set."""
        product = self.env['product.product'].create({
            'name': 'New Product',
            'type': 'product',
            'weight_in_uom': 10 * 1000,
            'weight_uom_id': self.gram.id,
        })

        product.refresh()
        self.assertEqual(product.weight, 10)
        self.assertEqual(product.weight_in_uom, 10 * 1000)
        self.assertEqual(product.weight_uom_id, self.gram)

    def test_on_create_weight_in_uom_supersedes_weight(self):
        """Test that on create, if weight and weight_in_uom are given, weight_in_uom is kept."""
        product = self.env['product.product'].create({
            'name': 'New Product',
            'type': 'product',
            'weight': 9,
            'weight_in_uom': 10 * 1000,
            'weight_uom_id': self.gram.id,
        })

        product.refresh()
        self.assertEqual(product.weight, 10)
        self.assertEqual(product.weight_in_uom, 10 * 1000)
        self.assertEqual(product.weight_uom_id, self.gram)
