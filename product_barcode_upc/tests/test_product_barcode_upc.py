# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase
from odoo.tools.float_utils import float_compare, float_round


class TestProductBarcodeU(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Template = cls.env["product.template"].create({
            "name": "Customer A",
            "customer": True,
        })
        cls.product_weight_pound = cls.env["product.product"].create({
            "name": "Product Pound",
            "uom_id": cls.unit_uom.id,
            "specific_weight_uom_id": cls.pound_uom.id,
            "weight_in_uom": 100,
        })
        cls.product_weight_gram = cls.env["product.product"].create({
            "name": "Product Gram",
            "uom_id": cls.unit_uom.id,
            "specific_weight_uom_id": cls.gram_uom.id,
            "weight_in_uom": 200,
        })
        cls.product_uom_days = cls.env["product.product"].create({
            "name": "Product Gram",
            "uom_id": cls.day_uom.id,
            "uom_po_id": cls.day_uom.id,
            "specific_weight_uom_id": cls.gram_uom.id,
            "weight_in_uom": 200,
        })

    def _create_simple_sale_order(self, product, product_uom=None):
        """
        test_search_product_{template|variant}_by_{name|barcode|upc}_{with|without}_result
        """
        if not product_uom:
            product_uom = self.unit_uom
        so = self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "order_line": [(0, 0, {
                "product_id": product.id,
                "product_uom_qty": 2,
                "product_uom": product_uom.id,
                "price_unit": 1,
            })]
        })
        return so

    def _assert_weight(self, so_weight, expected_weight, uom=None):
        if not uom:
            precision_rounding = 0.01
        else:
            precision_rounding = uom.rounding
        # weight_in_kg formula: qty * sol's uom_factor * product's weight (kg)
        # weight_in_lb formula: qty * sol's uom_factor * product's weight (kg) * 2.20462
        self.assertEqual(
            float_compare(
                so_weight,
                expected_weight,
                precision_digits=precision_rounding
            ),
            0
        )

    def test_product_with_weight_in_lb(self):
        so = self._create_simple_sale_order(product=self.product_weight_pound)
        self._assert_weight(so.weight_in_kg, 2 * 1 * (100/2.20462), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 2 * 1 * 100, uom=self.lb_uom)

    def test_product_with_weight_in_other_uom(self):
        so = self._create_simple_sale_order(product=self.product_weight_gram)
        self._assert_weight(so.weight_in_kg, 2 * 1 * (200/1000), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 2 * 1 * (200/1000) * 2.20462, uom=self.lb_uom)

    def test_sale_order_line_with_custom_uom(self):
        so = self._create_simple_sale_order(
            product=self.product_weight_gram, product_uom=self.dozen_uom)
        self._assert_weight(so.weight_in_kg, 2 * 12 * (200/1000), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 2 * 12 * (200/1000) * 2.20462, uom=self.lb_uom)

    def test_sale_order_line_update(self):
        so = self._create_simple_sale_order(
            product=self.product_weight_pound, product_uom=self.dozen_uom)
        # update qty
        so.order_line[0].product_uom_qty = 4
        self._assert_weight(so.weight_in_kg, 4 * 12 * (100/2.20462), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 4 * 12 * 100, uom=self.lb_uom)
        # update uom
        so.order_line[0].product_uom = self.unit_uom.id
        self._assert_weight(so.weight_in_kg, 4 * 1 * (100/2.20462), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 4 * 1 * 100, uom=self.lb_uom)
        # update product
        so.order_line[0].product_id = self.product_weight_gram.id
        self._assert_weight(so.weight_in_kg, 4 * 1 * (200/1000), uom=self.kgm_uom)
        self._assert_weight(so.weight_in_lb, 4 * 1 * (200/1000) * 2.20462, uom=self.lb_uom)

    def test_multiple_sale_order_lines(self):
        so = self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "order_line": [
                (0, 0, {
                    "product_id": self.product_weight_pound.id,
                    "product_uom_qty": 2,
                    "product_uom": self.unit_uom.id,
                    "price_unit": 1,
                }),
                (0, 0, {
                    "product_id": self.product_weight_gram.id,
                    "product_uom_qty": 4,
                    "product_uom": self.unit_uom.id,
                    "price_unit": 1,
                }),
                (0, 0, {
                    "product_id": self.product_weight_pound.id,
                    "product_uom_qty": 6,
                    "product_uom": self.dozen_uom.id,
                    "price_unit": 1,
                }),
            ]
        })
        self._assert_weight(
            so.weight_in_kg,
            (
                (2 * 1 * (100 / 2.20462))
                + (4 * 1 * (200 / 1000))
                + (6 * 12 * (100 / 2.20462))
            ),
            uom=self.kgm_uom
        )
        self._assert_weight(
            so.weight_in_lb,
            (
                (2 * 1 * 100)
                + (4 * 1 * (200/1000)) * 2.20462
                + (6 * 12 * 100)
            ),
            uom=self.lb_uom
        )
