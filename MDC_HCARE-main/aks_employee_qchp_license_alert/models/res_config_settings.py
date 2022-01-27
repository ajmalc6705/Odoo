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


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    qchp_license_alert_days_before = fields.Boolean(string="Alert QCHP License")
    number_of_days = fields.Integer(string='Number of Days', default=1)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('aks_employee_qchp_license_alert.qchp_license_alert_days_before', self.qchp_license_alert_days_before)
        self.env['ir.config_parameter'].sudo().set_param('aks_employee_qchp_license_alert.number_of_days', self.number_of_days)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            qchp_license_alert_days_before=self.env['ir.config_parameter'].sudo().get_param('aks_employee_qchp_license_alert.qchp_license_alert_days_before'),
            number_of_days=int(self.env['ir.config_parameter'].sudo().get_param('aks_employee_qchp_license_alert.number_of_days')),
        )
        return res
