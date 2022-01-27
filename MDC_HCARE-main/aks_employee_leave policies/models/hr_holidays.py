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


class Holidays(models.Model):
    _inherit = "hr.holidays"

    leave_policies_id = fields.Many2one('hr.employee.leave.policies', string='Leave Policy')

    @api.onchange('leave_policies_id')
    def onchange_leave_policies_id(self):
        if self.leave_policies_id:
            self.number_of_days_temp = self.leave_policies_id.allocated_days

    @api.onchange('holiday_status_id', 'employee_id')
    def onchange_holiday_status_id(self):
        self.leave_policies_id = False
        self.number_of_days_temp = 0
