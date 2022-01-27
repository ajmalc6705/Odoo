# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Product(models.Model):
    _inherit = 'product.product'

    is_lab_test = fields.Boolean('Lab test?')