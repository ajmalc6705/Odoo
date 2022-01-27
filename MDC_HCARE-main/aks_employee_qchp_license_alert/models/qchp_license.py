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

import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class EmployeeQCHPLicense(models.Model):
    _name = 'aks.employee.qchp.license'

    def get_number_of_days(self):
        return self.env['ir.config_parameter'].sudo().get_param('aks_employee_qchp_license_alert.number_of_days')

    def _action_send_qchp_license_alert(self):
        qchp_notify = self.env['ir.config_parameter'].sudo().get_param('aks_employee_qchp_license_alert.qchp_license_alert_days_before')
        if qchp_notify:
            number_of_days = self.get_number_of_days()
            qchp_license = self.env['aks.employee.qchp.license'].search([])
            for qchp_rec in qchp_license:
                for line in qchp_rec.qchp_license_line_ids:
                    date_end = datetime.datetime.strptime(line.end_date, '%Y-%m-%d').date()
                    date_diff = relativedelta(datetime.date.today(), date_end).days
                    if date_diff == int(number_of_days):
                        template_id = qchp_rec.env.ref('aks_employee_qchp_license_alert.qchp_license_alert_template').id
                        template = qchp_rec.env['mail.template'].browse(template_id)
                        template.send_mail(qchp_rec.id, force_send=True)

    employee_id = fields.Many2one('hr.employee', string="Employee", required=1)
    date = fields.Datetime(string="Date", readonly=True, default=lambda self: fields.datetime.now())
    qchp_license_line_ids = fields.One2many('aks.employee.qchp.license.line', 'qchp_license_id', string="QCHP License Line")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id)


class EmployeeQCHPLicenseLine(models.Model):
    _name = 'aks.employee.qchp.license.line'

    @api.constrains('start_date', 'end_date')
    def start_and_end_date_validation(self):
        if self.end_date < self.start_date:
            raise ValidationError("End Date should not before Start date")

    qchp_license_id = fields.Many2one('aks.employee.qchp.license')
    company_id = fields.Many2one(related='qchp_license_id.company_id', string="Company")
    employee_id = fields.Many2one(related='qchp_license_id.employee_id', string="Employee")
    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    point = fields.Float(string="Points")
    remark = fields.Text(string="Remarks")
