from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class TreatmentInvoice(models.Model):
    _inherit = "treatment.invoice"

    amount = fields.Float("Unit Price After Discount", required=True)
    actual_amount = fields.Float('Unit Price', compute='_get_actual_amount')
    qty = fields.Integer('Quantity', compute='_compute_qty')
    subtotal = fields.Float('Subtotal', compute='_compute_qty')

    @api.onchange('discount', 'discount_value', 'qty', 'unit_price')
    def _onchange_discount_value(self):
        qty = 1
        if self.description.apply_quantity_on_payment_lines:
            qty = len(self.teeth_code_rel)
        if qty == 0:
            qty = 1
        if self.discount_fixed_percent == 'Fixed':
            if self.discount_value > (self.actual_amount * qty):
                raise UserError(_('Please Enter Discount properly.'))
        if self.discount_fixed_percent == 'Percent':
            if self.discount > 100:
                raise UserError(_('Discount Percentage should not be greater than 100'))
        if self.description:
            qty = 1
            if self.description.apply_quantity_on_payment_lines:
                qty = len(self.teeth_code_rel)
            if qty == 0:
                qty = 1
            unit_price = self._fetch_unit_price()
            lst_price = unit_price * qty
            if self.discount_fixed_percent == 'Fixed':
                if self.discount_value > lst_price:
                    raise UserError(_('Please Enter Discount properly.'))
                else:
                    discount_value = 0
                    if self.discount_value:
                        discount_value = self.discount_value
                    discount_value = round(discount_value / self.qty, 2)
                    self.amount = lst_price - discount_value
            elif self.discount_fixed_percent == 'Percent':
                if self.discount > 100:
                    raise UserError(_('Discount Percentage should not be greater than 100'))
                else:
                    discount_value = 0
                    if self.discount:
                        discount_value = (self.discount * lst_price) / 100
                    self.amount = lst_price - discount_value
            else:
                self.amount = lst_price
        else:
            self.amount = 0
            self.actual_amount = 0
            self.discount_fixed_percent = False
            self.discount = 0
            self.discount_value = 0

    @api.depends('amount', 'teeth_code_rel', 'unit_price')
    def _compute_qty(self):
        for record in self:
            qty = 1
            if record.description:
                if record.description.apply_quantity_on_payment_lines:
                    qty = len(record.teeth_code_rel)
            if qty == 0:
                qty = 1
            record.qty = qty
            if record.description:
                unit_price = record._fetch_unit_price()
                lst_price = unit_price * qty
                discount_value = 0
                if record.discount_fixed_percent == 'Fixed':
                    if record.discount_value:
                        discount_value = record.discount_value
                    record.subtotal = lst_price - discount_value
                    record.amount = lst_price - discount_value
                elif record.discount_fixed_percent == 'Percent':
                    if record.discount:
                        discount_value = (record.discount * lst_price) / 100
                    lst_price -= discount_value
                    record.subtotal = lst_price
                    record.amount = lst_price
                else:
                    record.subtotal = lst_price
                    record.amount = lst_price
