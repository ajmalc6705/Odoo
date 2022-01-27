# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MedicalAppointment(models.Model):
    _inherit = "medical.appointment"

    operation_ids = fields.One2many('medical.teeth.treatment', compute='_compute_operations')
    seq_treatment_number = fields.Char(string='Treatment No.', copy=False, readonly=True,
                   index=True, default=lambda self: _(''))
    have_pending_treatments = fields.Integer(string='# of Treatments', compute='_compute_pending_treatment')

    @api.depends('operation_ids')
    def _compute_pending_treatment(self):
        for record in self:
            record.have_pending_treatments = len(set(record.operation_ids.ids))

    @api.model
    def create(self, vals):
        vals['seq_treatment_number'] = self.env['ir.sequence'].next_by_code('appt_treatment_number_seq') or _('')
        result = super(MedicalAppointment, self).create(vals)
        return result

    @api.multi
    @api.model
    @api.depends('state')
    def _compute_operations(self):
        oper_obj = self.env['medical.teeth.treatment']
        for rcd in self:
            if rcd.patient and rcd.doctor.dental and rcd.state in ['checkin', 'ready', 'done', 'visit_closed']:
                oper_ids = oper_obj.search([('patient_id', '=', rcd.patient.id),
                                            ('appt_id', '!=', rcd.id),
                                            ('state', 'in', ['planned', 'in_progress'])])
            else:
                oper_ids = False
            rcd.operation_ids = oper_ids

    def button_pending_treatment(self):
        operation_ids = self.mapped('operation_ids')
        action_id = self.env.ref('treatment_plan_mdc.action_medical_teeth_treatment').read()[0]
        action_id['domain'] = [('id', 'in', operation_ids.ids)]
        action_id['target'] = 'new'
        action_id['context'] = {'search_default_group_by_treatment_plan_number': 1}
        return action_id

    @api.multi
    def action_view_treatment_plan(self):
        treatment_plans = self.mapped('patient.teeth_treatment_ids')
        action = self.env.ref('treatment_plan_mdc.action_medical_teeth_treatment').read()[0]
        action['display_name'] = 'Treatment Plans'
        action['context'] = {'search_default_group_by_treatment_plan_number': 1,'search_default_appt_id': self.id}
        if treatment_plans:
            action['domain'] = [('id', 'in', treatment_plans.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

