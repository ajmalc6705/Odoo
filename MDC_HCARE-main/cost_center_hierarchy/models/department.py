from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class MedicalPhysician(models.Model):
    _inherit = "medical.physician"

    department_id = fields.Many2one('medical.department', string='Department', required=True)
    costcenter_id = fields.Many2one('account.cost.center', string='Cost Center')

    @api.constrains('department_id', 'company_id', 'name')
    def _check_same_company_phys(self):
        if self.company_id:
            if self.department_id.company_id:
                if self.company_id.id != self.department_id.company_id.id:
                    raise ValidationError(_('Error ! Doctor and Department should be of same company'))
            if self.name.company_id:
                if self.company_id.id != self.name.company_id.id:
                    raise ValidationError(_('Error ! Doctor and Physician should be of same company'))
                
    def update_cost_center(self):
        doctor_list = self.env['medical.physician'].search([])
        for doctor in doctor_list:
            if doctor.department_id and doctor.department_id.cost_center_id:
                doctor.costcenter_id = doctor.department_id.cost_center_id and doctor.department_id.cost_center_id.id or False

class MedicalDepartment(models.Model):
    _name = "medical.department"

    name = fields.Char('Name', required=True)
    doctor_ids = fields.One2many('medical.physician', 'department_id', string='Doctors')
    cost_center_id = fields.Many2one('account.cost.center', string='Cost Center',required=False)
    cost_center_dep_ids = fields.One2many('account.cost.center','department_id',string='Cost Centers')


    @api.constrains('cost_center_id', 'company_id')
    def _check_same_company_dep(self):
        if self.company_id:
            if self.cost_center_id.company_id:
                if self.company_id.id != self.cost_center_id.company_id.id:
                    raise ValidationError(_('Error ! Department and Cost center should be of same company'))

    def _default_company(self):
        return self.env['res.company']._company_default_get('res.partner') or self.env.user.company_id.id

    company_id = fields.Many2one('res.company', 'Company', index=True, default=_default_company)