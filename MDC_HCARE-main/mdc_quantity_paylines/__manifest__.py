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

{
    'name': 'MDC Quantity on payment lines',
    'version': '11.0',
    'category': 'MDC Quantity(Based on tooth-Not Editable)',
    'sequence': 2,
    'summary': 'MDC Quantity(Based on tooth-Not Editable)',
    'description': """
    Medical
    """,
    'author': 'Al Khidma Systems',
    'depends': ['pragtech_dental_management', 'treatment_plan_mdc'],
    'data': [
        'views/treatment_invoice.xml',
        'views/appointment.xml',
        'views/treatment_plan.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
