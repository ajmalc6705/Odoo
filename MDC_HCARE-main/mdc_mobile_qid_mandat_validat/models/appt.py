# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import re


class MedicalAppointment(models.Model):
    _inherit = "medical.appointment"

    @api.multi
    def checkin(self):
        if not self.qid:
            raise ValidationError(_('QID is mandatory.'))
        return super(MedicalAppointment, self).checkin()

    # @api.one
    # @api.constrains('qid')
    # def constrains_qid(self):
    #     if self.qid:
    #         if re.match("^(\d{11})$", self.qid) == None:
    #             raise ValidationError("Enter valid 11 digits QID")
