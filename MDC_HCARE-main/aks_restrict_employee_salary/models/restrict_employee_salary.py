# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: Al Kidhma
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class RestrictEmployeeSalary(models.Model):
    _name = 'restrict.employee.salary'
    _rec_name = 'employee_id'
    _description = 'Restrict Employee Salary'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    remarks = fields.Text(string='Remarks')
    state = fields.Selection([
        ('draft', "Draft"), ('approved', "Approved"), ('cancel', 'Cancel')], default='draft')

    @api.onchange('end_date', 'start_date')
    def _onchange_report_type(self):
        for rec in self:
            if rec.end_date and rec.start_date:
                if rec.end_date < rec.start_date:
                    raise ValidationError("End date must be greater than start date")

    @api.multi
    def action_approve_employee_salary_restriction(self):
        return self.write({'state': 'approved'})

    @api.multi
    def action_cancel_employee_salary_restriction(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def restrict_employee_salary(self, employee, from_date, to_date, basic_salary):
        net_salary = basic_salary
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        restrict_employee = self.env['restrict.employee.salary'].search(
            [('employee_id', '=', employee), ('state', '=', 'approved')])

        total_days = 0
        for restrict_emp in restrict_employee:
            start_date = datetime.strptime(restrict_emp.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(restrict_emp.end_date, "%Y-%m-%d")
            if start_date >= from_date and end_date <= to_date:
                no_of_days = (end_date - start_date).days
            elif start_date > from_date and end_date > to_date:
                no_of_days = (end_date - to_date).days
            elif start_date < from_date and end_date < to_date:
                no_of_days = (end_date - from_date).days

            total_days = total_days + no_of_days
        payslip_total_days = ((to_date - from_date).days + 1)
        salary_for_one_day = net_salary / payslip_total_days

        deduction = salary_for_one_day * total_days
        return -deduction
