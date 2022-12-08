# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class TestProductBarcodeUPC(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.upc = "9876543210"
        cls.barcode = "1234567890"
        cls.product = cls.env["product.product"].create(
            {"name": "My Product", "upc": cls.upc, "barcode": cls.barcode}
        )

    def test_upc(self):
        result = self.env["product.product"].get_all_products_by_barcode()
        assert self.upc in result

    def test_barcode(self):
        result = self.env["product.product"].get_all_products_by_barcode()
        assert self.barcode in result

    def test_upc_with_barcode_empty(self):
        self.product.barcode = None
        result = self.env["product.product"].get_all_products_by_barcode()
        assert self.upc in result

    def test_barcode_with_upc_empty(self):
        self.product.upc = None
        result = self.env["product.product"].get_all_products_by_barcode()
        assert self.barcode in result
