# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from ast import literal_eval
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class LabRequest(models.Model):
    _inherit = 'lab.request'

    READONLY_STATES_Done = {
        'Done': [('readonly', True)],
    }


    lab_id = fields.Many2one('res.partner', 'Laboratory', required=True, readonly=False,
                              states=READONLY_STATES_Done, track_visibility='onchange',
                              domain = [('is_laboratory','=', True)])
    lab_bill_id = fields.Many2one("account.invoice", "Lab Bill", readonly=True, track_visibility='onchange')

    def create_lab_bill_per_order(self):
        invoice_vals = {}
        invoice_line_vals = []
        bill_id = False
        patient_brw = self.patient_id
        lab_brw = self.lab_id
        vendor_bill_jr_brw = self.env['account.journal'].search([('type', '=', 'purchase'), ('name', '=', 'Vendor Bills'),
                                                     ('company_id', '=', self.company_id.id)])
        cost_center_id = False
        if self.doctor_id:
            if self.doctor_id.department_id:
                if self.doctor_id.department_id:
                    cost_center_id = self.doctor_id.department_id.cost_center_id.id
        for lab_line in self.lab_request_line_ids:
            seller = lab_line.test_id._select_seller(
                partner_id=self.lab_id, quantity=1, date=self.lab_date and self.lab_date[:10],
                uom_id=lab_line.test_id.uom_id)
            price_unit = 0.0
            if seller:
                price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                                     lab_line.test_id.supplier_taxes_id,
                                                                                     lab_line.test_id.supplier_taxes_id,
                                                                                     self.env.user.company_id) if seller else 0.0
                if price_unit and seller and self.env.user.currency_id and seller.currency_id != self.env.user.currency_id:
                    price_unit = seller.currency_id.compute(price_unit, self.env.user.currency_id)
            each_line = [0, False]
            product_dict = {}
            product_dict['product_id'] = lab_line.test_id.id
            product_dict['name'] = lab_line.test_id.name
            product_dict['quantity'] = 1
            product_dict['price_unit'] = price_unit
            # product_dict['price_unit'] = lab_line.sale_price
            acc_obj = self.env['account.account'].search([('name', '=', 'Local Sales'),
                                                          ('user_type_id', '=', 'Income')], limit=1)
            for account_id in vendor_bill_jr_brw:
                product_dict[
                    'account_id'] = account_id.default_debit_account_id.id if account_id.default_debit_account_id else acc_obj.id
            product_dict['cost_center_id'] = cost_center_id
            each_line.append(product_dict)
            invoice_line_vals.append(each_line)
        # Creating invoice dictionary
        invoice_vals['account_id'] = lab_brw.property_account_receivable_id.id
        invoice_vals['company_id'] = self.company_id.id
        invoice_vals['journal_id'] = vendor_bill_jr_brw.id
        invoice_vals['partner_id'] = lab_brw.id
        invoice_vals['type'] = 'in_invoice'
        invoice_vals['journal_type'] = 'purchase'
        invoice_vals['dentist'] = self.doctor_id.id
        # invoice_vals['patient'] = patient_brw.id
        invoice_vals['cost_center_id'] = cost_center_id
        invoice_vals['is_laboratory'] = True
        invoice_vals['appt_id'] = self.appointment_id.id
        invoice_vals['invoice_line_ids'] = invoice_line_vals
        bill_id = self.env['account.invoice'].create(invoice_vals)
        bill_id.action_invoice_open()
        return bill_id

    def completed_request(self):
        inv_id = self.create_patient_invoice()
        config_obj = self.env['ir.config_parameter'].sudo()
        lab_bill_type = config_obj.get_param('lab_bill_type', default='False')
        bill_id = False
        if not lab_bill_type:
            raise UserError('Set Laboratory Bill option under HCARE Settings Laboratory configuration')
        if lab_bill_type == 'per_lab_order':
            bill_id = self.create_lab_bill_per_order()
        vals = {'state': 'Done'}
        if inv_id:
            vals['invoice_id'] = inv_id.id
        if bill_id:
            vals['lab_bill_id'] = bill_id.id
        self.write(vals)