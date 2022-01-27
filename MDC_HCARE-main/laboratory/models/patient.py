# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    lab_ids = fields.One2many('lab.request', 'patient_id', 'Lab Orders')
    
    @api.multi
    def unlink(self):
        for patient in self:
            lab_request = self.env['lab.request'].search([('patient_id','=',patient.id)])
            if lab_request:
                lab_request_line = self.env['lab.request.lines'].search([('lab_request_id','in',lab_request.ids)])
                lab_request_line.unlink()
            lab_request.unlink()
        return super(MedicalPatient, self).unlink()
