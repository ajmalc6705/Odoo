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


class FreeOfCostReason(models.Model):
    _name = 'foc.reason'
    _description = 'Free of Cost Reason '

    name = fields.Char(string='Reason')
