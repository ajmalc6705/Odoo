# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class SubInsurar(models.Model):
    _name = "sub.insurar"

    name = fields.Char(required=True)
