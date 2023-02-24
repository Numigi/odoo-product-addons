# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import api, models
from odoo.addons.product_pricelist_direct_print_extended.wizards.\
    product_pricelist_print import ProductPricelistPrint


def send_batch(self):
    self.ensure_one()
    for partner in self.partner_ids:
        self.write({
            'partner_id': partner.id,
            'pricelist_id': partner.property_product_pricelist.id,
        })
        self.with_context(partner_id=partner.id).force_pricelist_send()


ProductPricelistPrint.send_batch = send_batch


class ProductPricelistPrintChatter(models.TransientModel):
    _inherit = 'product.pricelist.print'

    def generate_report(self, template_id):
        report = self.env.ref(
            'product_pricelist_direct_print.action_report_product_pricelist')
        result, _  = report._render_qweb_pdf([self.id])
        result = base64.b64encode(result)
        new_attachment_id = self.env['ir.attachment'].create({
            'name': self.pricelist_id.name,
            'datas': result,
        })
        template_id.attachment_ids = [(6, 0, [new_attachment_id.id])]

    def message_composer_action(self):
        self.ensure_one()
        template_id = self.env.ref(
            'product_pricelist_direct_print_chatter.'
            'email_template_edi_pricelist_chatter')
        if not template_id.attachment_ids:
            self.generate_report(template_id)
        compose_form_id = self.env.ref(
            'mail.email_compose_message_wizard_form').id
        ctx = {
            'default_composition_mode': 'comment',
            'default_res_id': self._context.get('active_id'),
            'default_model': self._context.get('active_model'),
            'default_use_template': bool(template_id.id),
            'default_template_id': template_id.id,
            'default_notify': True,
            'pricelist_name': self.pricelist_id.name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def force_pricelist_send(self):
        template_id = self.env.ref(
            'product_pricelist_direct_print_chatter.'
            'email_template_edi_pricelist_chatter')
        if not template_id.attachment_ids:
            self.generate_report(template_id)
        composer = self.env['mail.compose.message'].with_context({
            'default_composition_mode': 'comment',
            'default_notify': True,
            'default_res_id': self._context.get('partner_id'),
            'default_model': self._context.get('active_model'),
            'default_use_template': bool(template_id.id),
            'default_template_id': template_id.id,
        }).sudo().create({})
        values = composer.onchange_template_id(
            template_id.id, 'comment', self._context.get('active_model'),
            self._context.get('partner_id'))['value']
        composer.write(values)
        composer.with_context(
            pricelist_name=self.pricelist_id.name).send_mail()
