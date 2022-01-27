# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MedicalInsurance(models.Model):
    _inherit = "medical.insurance"

    def _set_dom_subinsurar(self):
        for card in self:
            card.onchange_company_id()
            card.dom_subinsurar = '1'

    dom_subinsurar = fields.Char(compute='_set_dom_subinsurar')

    @api.onchange('company_id', 'company_id.sub_insurar_ids')
    def onchange_company_id(self):
        user = {'domain': {}}
        sub_insurar_domain = self._get_sub_insurar_id()
        if self.company_id and self.sub_insurar_id not in self.company_id.sub_insurar_ids:
            self.sub_insurar_id = False
        user['domain']['sub_insurar_id'] = sub_insurar_domain
        return user

    def _get_sub_insurar_id(self):
        domain = [('id', 'in', [])]
        if self.company_id and self.company_id.sub_insurar_ids:
            domain = [('id', 'in', self.company_id.sub_insurar_ids.ids)]
        return domain

    sub_insurar_id = fields.Many2one('sub.insurar', string='Sub insurar', domain=_get_sub_insurar_id)



