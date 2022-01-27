# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TeethCode(models.Model):
    _inherit = "teeth.code"

    child = fields.Boolean('Child Tooth')
