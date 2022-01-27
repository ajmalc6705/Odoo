from odoo import api, fields, models

class TreatementPlanReport(models.AbstractModel):
    _name = 'report.treatment_plan_mdc.report_treatment_plan_multi_pdf'

    @api.multi
    def get_report_values(self, docids, data=None):
        operation_ids = self.env['medical.teeth.treatment'].search([('id', 'in', self._context['operation_ids'])])
        data['operation_ids']= operation_ids

        return data


