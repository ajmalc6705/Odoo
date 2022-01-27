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
    'name': 'QCHP License Alert',
    'version': '11.0',
    'category': 'hr',
    'sequence': 2,
    'summary': 'Employee QCHP License Alert',
    'description': """
        Employee QCHP License Alerting by Mail
    """,
    'author': 'Al Khidma Systems',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/qchp_license_cron.xml',
        'data/qchp_license_alert_mail_template.xml',
        'views/qchp_license_views.xml',
        'views/employee_res_config_settings_views.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
