# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProductPricelistPrint(models.TransientModel):
    _name = 'product.pricelist.print'
    _inherit = ['product.pricelist.print', 'mail.thread']

    @api.multi
    def send_batch(self):
        self.ensure_one()
        for partner in self.partner_ids:
            self.write({
                'partner_id': partner.id,
                'pricelist_id': partner.property_product_pricelist.id,
            })
            self.force_pricelist_send()
