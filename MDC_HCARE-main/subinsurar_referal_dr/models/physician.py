# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MedicalPhysician(models.Model):
    _inherit = "medical.physician"

    doctor_insurance_ids = fields.One2many('doctor.insurance', 'physician_id', 'Insurance Numbers')
