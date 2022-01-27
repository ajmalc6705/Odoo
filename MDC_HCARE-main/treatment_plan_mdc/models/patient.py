# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64


class MedicalPatient(models.Model):
    _inherit = "medical.patient"

    teeth_treatment_ids = fields.One2many('medical.teeth.treatment', 'patient_id', 'Operations', readonly=False)

    @api.multi
    def action_view_treatment_plan(self):
        treatment_plans = self.mapped('teeth_treatment_ids')
        action = self.env.ref('treatment_plan_mdc.action_medical_teeth_treatment').read()[0]
        action['display_name'] = 'Treatment Plans'
        action['context'] = {'search_default_group_by_treatment_plan_number': 1}
        if treatment_plans:
            action['domain'] = [('id', 'in', treatment_plans.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
