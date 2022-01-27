# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError
from ast import literal_eval


class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    @api.multi
    def insurance_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        return self.env.ref('mdc_service_bill.insurance_invoice_pdf').report_action(self)
