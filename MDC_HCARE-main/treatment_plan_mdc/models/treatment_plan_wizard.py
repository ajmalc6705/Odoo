from datetime import date
from odoo.exceptions import Warning
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
import time
import base64
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)


class PlanWizard(models.TransientModel):
    _inherit = 'treatment.plan.wizard'

    @api.multi
    @api.model
    @api.depends('doctor')
    def _compute_operations(self):
        if 'operation_ids' in self._context :
            oper_ids = self.env['medical.teeth.treatment'].search([('id', 'in', self._context['operation_ids'])])
        else :
            oper_obj = self.env['medical.teeth.treatment']
            if self.appt_id:
                oper_ids = oper_obj.search([('patient_id', '=', self.appt_id.patient.id), ('state', 'in', ['planned'])])
            else:
                oper_ids = False
        self.operations = oper_ids

    @api.onchange("appt_id")
    def onchange_appt(self):
        for record in self:
            if record.appt_id:
                record.doctor = record.appt_id.doctor.name.name
                record.patient = record.appt_id.patient_name

    @api.multi
    def action_confirm(self):
        if 'operation_ids'  in self._context.keys() :
            act_id = self.env.context.get('active_ids', [])
            appt = self.env['medical.appointment'].search([('id', '=', self._context['default_appt_id'])])
            appt.write({'plan_signature': self.plan_signature,
                        'treatment_plan_date': self.updated_date,
                        })
            data = {'ids': self.id,'docs':self}
            patient = ""
            if appt:
                patient = appt.patient.name_get()[0][1]
                data, data_format = self.env.ref('treatment_plan_mdc.report_treatment_plan3_pdf').render(self.id,
                                                                                                         data=data)
                att_id = self.env['ir.attachment'].create({
                'name': 'Treatment_Plan_' + fields.Date.context_today(self) ,
                'type': 'binary',
                'datas': base64.encodestring(data),
                'datas_fname': patient + '_treatment_plan.pdf',
                'res_model': 'medical.appointment',
                'res_id': appt.id,
                'mimetype': 'application/pdf'
                })

        else :
            act_id = self.env.context.get('active_ids', [])
            appt = self.env['medical.appointment'].search([('id', 'in', act_id)])
            appt.write({'plan_signature': self.plan_signature,
                        'treatment_plan_date': self.updated_date,
                        })
            appt.attach_treatment_plan()