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
    'name': 'Laboratory Management(Paying by Clinic to Laboratory)',
    'version': '11.0',
    'category': 'Laboratory Management',
    'sequence': 2,
    'summary': 'Laboratory Management',
    'description': """
    Medical
    """,
    'author': 'Al Khidma Systems',
    'depends': ['pragtech_dental_management', 'laboratory'],
    'data': [
        'views/res_config.xml',
        'views/lab_request.xml',
        'views/invoice.xml',
        'views/partner.xml',
        'views/lab_test.xml',
        # 'reports/report_lab_order.xml',
            ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
