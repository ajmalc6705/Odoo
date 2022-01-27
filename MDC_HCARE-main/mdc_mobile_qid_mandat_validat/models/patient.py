# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import ValidationError
import re


# class MedicalPatient(models.Model):
#     _inherit = "medical.patient"

    # @api.onchange('qid')
    # def onchange_qid(self):
    #     if self.qid:
    #         if re.match("^(\d{11})$", self.qid) == None:
    #             raise ValidationError("Enter valid 11 digits QID")
