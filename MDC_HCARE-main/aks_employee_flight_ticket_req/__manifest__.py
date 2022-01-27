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
    'name': 'Employee Flight Ticket Request',
    'version': '11.0',
    'category': 'hr',
    'sequence': 2,
    'summary': 'Employee Flight Ticket Request',
    'description': """
        Employee Flight Ticket Request and the eligibility checking
    """,
    'author': 'Al Khidma Systems',
    'depends': ['hr', 'aks_employee_grade_master', 'aks_employee_visa_details'],
    'data': [
        'security/ir.model.access.csv',
        'security/flight_ticket_security.xml',
        'views/employee_grade_views.xml',
        'views/hr_employee_ticket_views.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
