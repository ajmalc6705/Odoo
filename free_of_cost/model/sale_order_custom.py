# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Ajmal C
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#    Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    foc_reason_id = fields.Many2one('foc.reason', store=True, string='Reason')
    foc = fields.Boolean('Non Billable', default=0)

    @api.onchange('foc')
    def _free_of_cost(self):
        for rec in self:
            if rec.foc == True:
                rec.price_unit = 0
