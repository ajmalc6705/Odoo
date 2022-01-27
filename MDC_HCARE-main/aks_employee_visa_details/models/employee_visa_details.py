# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: Al Kidhma Group
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

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_visa_details_ids = fields.One2many('hr.employee.visa.details.line', 'hr_employee_id', string="Visa Details Line")


class EmployeeVisaDetailsLine(models.Model):
    _name = 'hr.employee.visa.details.line'

    @api.constrains('issued_date', 'expiry_date')
    def start_and_end_date_validation(self):
        if self.expiry_date < self.issued_date:
            raise ValidationError("Expiry Date should not before Issued date")

    hr_employee_id = fields.Many2one('hr.employee', string="Employee", required=1)
    visa_name = fields.Char(string="Visa Name")
    visa_type = fields.Many2one('aks.visa.type', string="Visa Type")
    type = fields.Selection([('employee', 'Employee'), ('family', 'Family')], string="Type")
    relation = fields.Many2one('aks.employee.relation', string="Relation")
    family_member = fields.Many2one('res.partner', string="Family Member", required=1)
    date_of_birth = fields.Date(string="DOB", required=1)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    mobile_no = fields.Char(string="Contact No.")
    issued_date = fields.Date(string="Issued Date")
    expiry_date = fields.Date(string="Expiry Date")
    country_id = fields.Many2one('res.country', string="Country")
