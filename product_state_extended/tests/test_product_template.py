# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form

from odoo.addons.product_state.tests.test_product_state import (
    TestProductState,
)


class TestProductTemplate(TestProductState):
    def test_product_with_product_state(self):
        product_state_sellable = self.env.ref("product_state.product_state_sellable")
        product_state_sellable.write(
            {
                "sale_ok": True,
                "purchase_ok": True,
                "can_be_rented": False,
                "is_kit": True,
                "can_be_expensed": True,
                "pack_ok": False,
            }
        )

        product_template = Form(self.env["product.template"])
        product_template.name = "Test Product Template"
        product = product_template.save()

        self.assertEqual(
            self.env.ref("product_state.product_state_sellable"),
            product.product_state_id,
        )
        self.assertTrue(product_state_sellable.sale_ok)
        self.assertTrue(product_state_sellable.purchase_ok)
        self.assertFalse(product_state_sellable.can_be_rented)
        self.assertTrue(product_state_sellable.is_kit)
        self.assertTrue(product_state_sellable.can_be_expensed)
        self.assertFalse(product_state_sellable.pack_ok)

        self.assertTrue(product.sale_ok)
        self.assertTrue(product.purchase_ok)
        self.assertFalse(product.can_be_rented)
        self.assertTrue(product.is_kit)
        self.assertTrue(product.can_be_expensed)
        self.assertFalse(product.pack_ok)

        # Test if raising error when user is not allowed to change product state
        user = self.env.ref("base.user_demo")
        user.groups_id -= self.env.ref(
            "product_state_extended.group_product_state_manager"
        )
        self.env = self.env(user=user)
        with self.assertRaises(Exception):
            product.product_state_id = self.env.ref("product_state.product_state_draft")
            product._onchange_product_state_id()

        # Now user is allowed to change product state
        user.groups_id += self.env.ref(
            "product_state_extended.group_product_state_manager"
        )
        self.env = self.env(user=user)
        product.with_user(user).product_state_id = self.env.ref(
            "product_state.product_state_obsolete"
        )
        product.with_user(user)._onchange_product_state_id()
        self.assertEqual(
            self.env.ref("product_state.product_state_obsolete"),
            product.product_state_id,
        )
        self.assertFalse(product.sale_ok)
        self.assertFalse(product.purchase_ok)
        self.assertFalse(product.can_be_rented)
        self.assertFalse(product.is_kit)
        self.assertFalse(product.can_be_expensed)
        self.assertFalse(product.pack_ok)
