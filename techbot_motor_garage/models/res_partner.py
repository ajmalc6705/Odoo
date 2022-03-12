# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

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
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_count = fields.Integer(compute='_compute_vehicle_count', string='Vehicles')

    def _compute_vehicle_count(self):
        """         Override original method to Count Customer Vehicle         """
        fleet_obj = self.env['fleet.vehicle']
        for partner in self:
            partner.vehicle_count = fleet_obj.search_count([('driver_id', '=', partner.id)])
            _logger.info("partner.vehicle_count %s", partner.vehicle_count)

    def get_partner_vehicles(self):
        """
        Return an action that display fleet records related for the given partners.
        """
        fleet_obj = self.env['fleet.vehicle']
        vehicle_ids = fleet_obj.search([('driver_id', '=', self.id)]).mapped('id')
        return {
            'domain': [('id', 'in', vehicle_ids)],
            'name': _('Vehicles'),
            'view_type': 'kanban',
            'view_mode': 'kanban,tree,form',
            'res_model': 'fleet.vehicle',
            'view_id': False,
            'context': {'default_driver_id': self.id},
            'type': 'ir.actions.act_window'
        }




