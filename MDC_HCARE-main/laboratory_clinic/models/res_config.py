# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lab_bill_type = fields.Selection([
        ('per_lab_order', 'Per Lab Order'),
        ('Bulk', 'Bulk')
    ], string='Bill type for Laboratory', help="Bill type for Laboratory", default='per_lab_order')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        lab_bill_type = ICPSudo.get_param('lab_bill_type')
        res.update({
            'lab_bill_type': lab_bill_type,
                    })
        return res

    @api.multi
    def set_values(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res = super(ResConfigSettings, self).set_values()
        ICPSudo.set_param("lab_bill_type", self.lab_bill_type)
        return res
