# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProduct(common.SavepointCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "My Product"})
        cls.template = cls.product.product_tmpl_id
        cls.product_2 = cls.env["product.product"].create(
            {"name": "My Product 2"}
        )

        cls.po = cls.env["purchase.order"].create(
            {
                "partner_id": cls.env.user.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "name": "/",
                            "product_qty": 1,
                            "price_unit": 1,
                            "date_planned": "2020-01-01",
                        },
                    )
                ],
            }
        )

    def test_template__purchase_quotation_count(self):
        assert self.template.purchase_quotation_count == 1
        assert self.template.purchase_order_count == 0

    def test_product__purchase_quotation_count(self):
        assert self.product.purchase_quotation_count == 1
        assert self.product_2.purchase_quotation_count == 0

    def test_template__open_purchase_quotation_list(self):
        domain = self.template.open_purchase_quotation_list()["domain"]
        assert self.env["purchase.order"].search(domain) == self.po

    def test_product__open_purchase_quotation_list(self):
        domain = self.product.open_purchase_quotation_list()["domain"]
        assert self.env["purchase.order"].search(domain) == self.po

        domain = self.product_2.open_purchase_quotation_list()["domain"]
        assert not self.env["purchase.order"].search(domain)

    def test_template__purchase_order_count(self):
        self.po.button_confirm()
        assert self.template.purchase_quotation_count == 0
        assert self.template.purchase_order_count == 1

    def test_product__purchase_order_count(self):
        self.po.button_confirm()
        assert self.product.purchase_order_count == 1
        assert self.product_2.purchase_order_count == 0

    def test_template__open_purchase_order_list(self):
        self.po.button_confirm()
        domain = self.template.open_purchase_order_list()["domain"]
        assert self.env["purchase.order"].search(domain) == self.po

    def test_product__open_purchase_order_list(self):
        self.po.button_confirm()
        domain = self.product.open_purchase_order_list()["domain"]
        assert self.env["purchase.order"].search(domain) == self.po

        domain = self.product_2.open_purchase_order_list()["domain"]
        assert not self.env["purchase.order"].search(domain)
