# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProductNameSearch(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({'name': 'Supplier', 'supplier': True})

        cls.table = cls.env['product.product'].create({
            'name': 'Wood Table',
            'type': 'product',
            'default_code': 'WT2001',
            'seller_ids': [(0, 0, {
                'name': cls.supplier.id,
                'product_name': 'Brown Table',
                'product_code': 'BT1001',
            })],
        })

        cls.chair = cls.env['product.product'].create({
            'name': 'Wood Chair',
            'type': 'product',
            'default_code': 'WC2001',
            'seller_ids': [(0, 0, {
                'name': cls.supplier.id,
                'product_name': 'Brown Chair',
                'product_code': 'BC1001',
            })],
        })

    def _search(self, name, operator='ilike'):
        items = self.env['product.product'].name_search(name, operator=operator, limit=999999)
        return self.env['product.product'].browse([el[0] for el in items])

    def test_search_by_product_name(self):
        res = self._search('Wood')
        assert self.table in res
        assert self.chair in res

        res = self._search('Wood Table')
        assert self.table in res
        assert self.chair not in res

        res = self._search('Wood Chair')
        assert self.table not in res
        assert self.chair in res

    def test_search_by_product_default_code(self):
        res = self._search('2001')
        assert self.table in res
        assert self.chair in res

        res = self._search('WT2001')
        assert self.table in res
        assert self.chair not in res

        res = self._search('WC2001')
        assert self.table not in res
        assert self.chair in res

    def test_search_by_supplier_product_name(self):
        res = self._search('Brown')
        assert self.table in res
        assert self.chair in res

        res = self._search('Brown Table')
        assert self.table in res
        assert self.chair not in res

        res = self._search('Brown Chair')
        assert self.table not in res
        assert self.chair in res

    def test_search_by_supplier_product_code(self):
        res = self._search('1001')
        assert self.table in res
        assert self.chair in res

        res = self._search('BT1001')
        assert self.table in res
        assert self.chair not in res

        res = self._search('BC1001')
        assert self.table not in res
        assert self.chair in res

    def test_name_search_with_negative_operator(self):
        """Test that the module does not break the standard behavior of negative operators.

        The module only supports positive operators (i.e. `ilike`).
        If a negative operator is given, the supplier info will not be checked.
        """
        items = self._search('WT2001', operator='!=')
        assert self.table not in items
        assert self.chair in items
