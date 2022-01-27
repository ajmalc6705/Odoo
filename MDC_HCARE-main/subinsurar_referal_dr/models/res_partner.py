# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Partner(models.Model):
    _inherit = "res.partner"

    sub_insurar_ids = fields.Many2many('sub.insurar')



