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
    'name': 'Company Id To Custom Models',
    'version': '11.0',
    'category': 'Uncategorized',
    'sequence': 2,
    'summary': 'Company Id To Custom Models',
    'description': """
        Adding Company field and set default value in all custom models
    """,
    'author': 'Al Khidma Systems',
    'depends': [
        'aks_employee_visa_details',
        'aks_restrict_employee_salary',
        'auto_backup',
        'calendar_scheduler',
        'dynamic_consent_form',
        'hr_complete_solution',
        'hr_contract_salary_rule',
        'hr_final_settlement',
        'laboratory',
        'pragtech_dental_management',
        'service_consumable',
        'staffcommission_mdc',
        'subinsurar_referal_dr',
    ],
    'data': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

