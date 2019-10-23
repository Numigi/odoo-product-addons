# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from odoo.tests import common


@ddt
class TestProductCreateGroup(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'Test',
            'login': 'test@test.com',
            'email': 'test@test.com',
            'groups_id': [
                (4, cls.env.ref('base.group_user').id),
                (4, cls.env.ref('product_create_group.group_product_create').id),
            ]
        })
        cls.supplier = cls.env['res.partner'].create({'name': 'Supplier', 'supplier': True})

        cls.attribute = cls.env['product.attribute'].search([], limit=1)

    @data('product.product', 'product.template')
    def test_create_product_with_one_seller(self, model):
        product = self.env[model].sudo(self.user).create({
            'name': 'Wood Table',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id,
                'product_name': 'Wood Table',
                'product_code': 'BT1001',
            })],
        })
        assert len(product.seller_ids) == 1

    def test_create_template_with_multiple_variants(self):
        template = self.env['product.template'].sudo(self.user).create({
            'name': 'Wood Table',
            'attribute_line_ids': [(0, 0, {
                'attribute_id': self.attribute.id,
                'value_ids': [
                    (4, self.attribute.value_ids[0].id),
                    (4, self.attribute.value_ids[1].id),
                ]
            })]
        })
        assert len(template.product_variant_ids) == 2

    def test_change_product_price(self):
        product = self.env['product.product'].sudo(self.user).create({
            'name': 'Wood Table',
            'standard_price': 50,
        })
        product.standard_price = 100
        history_lines = self.env['product.price.history'].search([('product_id', '=', product.id)])
        assert len(history_lines) == 2
