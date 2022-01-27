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
from datetime import datetime, date
from dateutil import relativedelta


class EmployeeLeavePolicies(models.Model):
    _name = 'hr.employee.leave.policies'
    _rec_name = 'leave_type_id'
    _description = 'Restrict Employee Salary'

    leave_type_id = fields.Many2one('hr.holidays.status', string='Leave Type')
    from_year_range = fields.Integer(string='From Year')
    to_year_range = fields.Integer(string='To Year')
    allocated_days = fields.Integer(string='Allocated Days')
    expire_from = fields.Date(string='Expire From')
    expire_to = fields.Date(string='Expire To')

    @api.constrains('leave_type_id', 'from_year_range', 'to_year_range')
    def _check_same_from_year_range(self):
        for rec in self:
            if rec.leave_type_id:
                policies = self.search([('leave_type_id', '=', rec.leave_type_id.id)])
                for policy in policies:
                    if policy.to_year_range == rec.from_year_range:
                        raise ValidationError(_(" Can't create record with this From Year Range"))

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        flag = False
        difference_in_years = 0
        today = date.today()
        if self.env.context.get('holiday_status_id') and self.env.context.get('employee_id'):
            employee = self.env['hr.employee'].browse(self.env.context.get('employee_id'))
            if employee:
                if employee.contract_ids:
                    for contract in employee.contract_ids:
                        if contract.state == 'open':
                            flag = True
                            now = datetime.now()
                            date_con = datetime.strptime(contract.date_start, "%Y-%m-%d")
                            time_difference = relativedelta.relativedelta(now, date_con)
                            difference_in_years = time_difference.years
        args = args or []
        recs = self.browse()
        if flag and difference_in_years > 0:
            recs = self.search([('leave_type_id', '=', self.env.context.get('holiday_status_id')),
                                ('expire_from', '<=', today),
                                ('expire_to', '>=', today), ('from_year_range', '<=', difference_in_years),
                                ('to_year_range', '>=', difference_in_years)] + args, limit=limit)
        return recs.name_get()
