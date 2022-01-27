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
    'name': 'Sub Insurar + Referral Doctor',
    'version': '11.0',
    'category': 'Sub Insurar + Referral Doctor',
    'sequence': 2,
    'summary': 'Sub Insurar + Referral Doctor',
    'description': """
    Sub Insurar + Referral Doctor
    """,
    'author': 'Al Khidma Systems',
    'depends': ['base', 'pragtech_dental_management', 'detailed_insurance'],
    'data': [
        'security/ir.model.access.csv',
        'views/subinsurar.xml',
        'views/partner.xml',
        'views/insurance_card.xml',
        'views/appt.xml',
        'views/physician.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
