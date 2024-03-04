# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class TestProductBarcodeUPC(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product_attribute = cls.env['product.attribute'].create({'name': 'Size'})
        size_value_l = cls.env['product.attribute.value'].create([{
            'name': 'L',
            'attribute_id': product_attribute.id,
        }])
        cls.product_template = cls.env["product.template"].create({
            "name": "Product Template",
            "barcode": "123456789",
        })
        cls.env['product.template.attribute.line'].create({
            'attribute_id': product_attribute.id,
            'product_tmpl_id': cls.product_template.id,
            'value_ids': [(6, 0, [size_value_l.id])],
        })
        cls.variant_a1 = cls.product_template.product_variant_ids[0]

        cls.variant_a1.upc = "0123456789"
        cls.product_product = cls.env["product.product"].create({
            "name": "Product Product",
            "barcode": "987654321",
            "upc": "9876543210",
        })

    def _check_search_product_by_field(self, product_type, value, result_length):
        res = self.env[product_type]._name_search(name=value, operator="=")
        self.assertEqual(len(res), result_length)

    def test_search_product_template_by_name_with_result(self):
        self._check_search_product_by_field("product.template", "Product Template", 1)

    def test_search_product_template_by_name_without_result(self):
        self._check_search_product_by_field("product.template", "aaa", 0)

    def test_search_product_template_by_barcode_with_result(self):
        self._check_search_product_by_field("product.template", "123456789", 1)

    def test_search_product_template_by_barcode_without_result(self):
        self._check_search_product_by_field("product.template", "000", 0)

    def test_search_product_template_by_upc_with_result(self):
        self._check_search_product_by_field("product.template", "0123456789", 1)

    def test_search_product_template_by_upc_without_result(self):
        self._check_search_product_by_field("product.template", "111", 0)

    def test_search_product_product_by_name_with_result(self):
        self._check_search_product_by_field("product.product", "Product Product", 1)

    def test_search_product_product_by_name_without_result(self):
        self._check_search_product_by_field("product.product", "zzz", 0)

    def test_search_product_product_by_barcode_with_result(self):
        self._check_search_product_by_field("product.product", "987654321", 1)

    def test_search_product_product_by_barcode_without_result(self):
        self._check_search_product_by_field("product.product", "999", 0)

    def test_search_product_product_by_upc_with_result(self):
        self._check_search_product_by_field("product.product", "9876543210", 1)

    def test_search_product_product_by_upc_without_result(self):
        self._check_search_product_by_field("product.product", "888", 0)
