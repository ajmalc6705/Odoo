# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MedicalAppointment(models.Model):
    _inherit = "medical.appointment"

    referral_dr_id = fields.Many2one('referral.dr', string='Referral Doctor', track_visibility='onchange')



