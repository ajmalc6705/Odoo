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
{
    'name': 'Restrict Employee Salary',
    'version': '11.0.0.0',
    'category': 'Human Resources',
    'sequence': 1,
    'summary': 'Restrict Employee Salary',
    'description': """
                 Restrict Employee Salary
    """,
    'author': 'Al Kidhma',
    'depends': ['hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'security/resctrict_salary_cancel_security.xml',
        'views/restrict_employee_salary_view.xml'
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
