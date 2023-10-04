# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.addons.product_pack.models.product_product import ProductProduct



def price_compute(self, price_type, uom=False, currency=False, company=False):
    packs, no_packs = self.split_pack_products()
    prices = super(ProductProduct, no_packs).price_compute(
        price_type, uom, currency, company
    )
    for product in packs.with_context(prefetch_fields=False):
        pack_price = 0.0
        for pack_line in product.sudo().pack_line_ids:
            pack_price += pack_line.get_price()
        pricelist_id_or_name = self._context.get("pricelist")
        # if there is a pricelist on the context the returned prices are on
        # that currency but, if the pack product has a different currency
        # it will be converted again by pp._compute_price_rule, so if
        # that is the case we convert the amounts to the pack currency
        if pricelist_id_or_name:
            if isinstance(pricelist_id_or_name, list):
                pricelist_id_or_name = pricelist_id_or_name[0]
            if isinstance(pricelist_id_or_name, str):
                pricelist_name_search = self.env["product.pricelist"].name_search(
                    pricelist_id_or_name, operator="=", limit=1
                )
                if pricelist_name_search:
                    pricelist = self.env["product.pricelist"].browse(
                        [pricelist_name_search[0][0]]
                    )
            elif isinstance(pricelist_id_or_name, int):
                pricelist = self.env["product.pricelist"].browse(
                    pricelist_id_or_name
                )
            # Add condition to not apply conversion for a pricelist with an article of the pack
            not_product_pack_in_pricelist = all(p not in product.sudo().pack_line_ids.mapped('product_id.id')
                                                for p in pricelist.item_ids.mapped('product_id.id'))
            if pricelist and not_product_pack_in_pricelist and pricelist.currency_id != product.currency_id:
                pack_price = pricelist.currency_id._convert(
                    pack_price,
                    product.currency_id,
                    self.company_id or self.env.company,
                    fields.Date.today(),
                )
        prices[product.id] = pack_price
    return prices

ProductProduct.price_compute = price_compute