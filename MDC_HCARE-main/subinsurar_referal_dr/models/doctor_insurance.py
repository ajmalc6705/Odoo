# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DoctorInsurance(models.Model):
    _name = "doctor.insurance"

    ins_company_id = fields.Many2one('res.partner', string='Insurance Company', required=True,
                                     domain="[('is_insurance_company', '=', '1')]")
    physician_id = fields.Many2one('medical.physician', 'Doctor', required=True)
    doctor_no = fields.Char(string="Doctor No.", required=True)
