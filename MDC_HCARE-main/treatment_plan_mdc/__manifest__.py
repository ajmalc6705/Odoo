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
    'name': 'Treatment plan without chart',
    'version': '11.0',
    'sequence': 1,
    'description': """
Treatment plan without chart
    """,
    'author': 'Al Khidma Systems',
    'depends': ['pragtech_dental_management'],
    'data': [
        'data/teeth_code.xml',
        'views/medical_teeth_treatment_view.xml',
        'views/tooth_view.xml',
        'views/appointment_view.xml',
        'views/patient_view.xml',
        'views/treatment_plan.xml',
        'views/treatment_plan_action.xml',
        'report/treatment_plan_template.xml',
            ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
