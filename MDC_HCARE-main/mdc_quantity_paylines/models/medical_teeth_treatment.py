# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MedicalTeethTreatment(models.Model):
    _inherit = "medical.teeth.treatment"

    amount = fields.Float('Unit Price After Discount')
    actual_amount = fields.Float('Unit Price', compute='_get_actual_amount', readonly=True)
    qty = fields.Integer('Quantity', compute='_compute_qty')
    subtotal = fields.Float('Subtotal', compute='_compute_qty')

    @api.onchange('description', 'teeth_code_rel')
    def onchange_description(self):
        if self.description:
            qty = 1
            if self.description.apply_quantity_on_payment_lines:
                qty = len(self.teeth_code_rel)
            if qty == 0:
                qty = 1
            self.amount = qty * self.description.lst_price
            self.unit_price = self.description.lst_price

    @api.depends('amount', 'teeth_code_rel')
    def _compute_qty(self):
        for record in self:
            qty = 1
            if record.description.apply_quantity_on_payment_lines:
                qty = len(record.teeth_code_rel)
            if qty == 0:
                qty = 1
            record.qty = qty
            if record.description:
                lst_price = record.description.lst_price * qty
                discount_value = 0
                if record.discount_fixed_percent == 'Fixed':
                    if record.discount_value:
                        discount_value = record.discount_value
                if record.discount_fixed_percent == 'Percent':
                    if record.discount:
                        discount_value = (record.discount * lst_price) / 100
                lst_price -= discount_value
                record.subtotal = lst_price

