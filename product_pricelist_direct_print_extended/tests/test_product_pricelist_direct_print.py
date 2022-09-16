# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProductPricelistDirectPrintExtended(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductPricelistDirectPrintExtended, cls).setUpClass()
        cls.pricelist = cls.env.ref('product.list0')

        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner for test',
            'property_product_pricelist': cls.pricelist.id,
            'email': 'test@test.com',
        })
        cls.wiz_obj = cls.env['product.pricelist.print']

    def test_action_pricelist_send_multiple_partner(self):
        self.commercial_partner = self.env['res.partner'].create({
            'name': 'Commercial Partner',
            'is_company': True,
        })
        partner_2 = self.env['res.partner'].create({
            'name': 'Partner for test 2',
            'property_product_pricelist': self.pricelist.id,
            'email': 'test2@test.com',
            'parent_id': self.commercial_partner.id,
        })
        wiz = self.wiz_obj.with_context(
            active_model='res.partner',
            active_ids=[self.partner.id, partner_2.id],
        ).create({})
        wiz.action_pricelist_send()
