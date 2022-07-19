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
{
    "name": "Free of Cost  V14",
    "summary": "Application for make free product based on the condition"
               "In Sales and Purchase  Module",
    "author": "Ajmal C",
    'email': 'ajmalc6705@gmail.com',
    "website": "",
    "category": "Sale",
    "version": "14.1.1.1",
    # 'price': 0,
    'sequence': 1,
    "license": "AGPL-3",
    'images': ['static/description/main_screenshot.png'],
    "depends": ["sale_management", "purchase", ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_custom_views.xml',
        'views/purchase_order_custom_views.xml',
        'views/free_of_cost_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
