# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: ALKIDHMA
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
    'name': "Employee Grade and Rank",
    'version': '11.0.1.0.0',
    'category': 'Employee',
    'summary': 'Employee Grade and Rank',

    'live_test_url': 'Add youtube video Link',
    'author': 'Al Khidma Systems',
    'license': 'OPL-1',
    'price': '',
    'currency': 'USD',
    'maintainer': 'Al Khidma Systems',
    'support': 'tech@alkhidmasystems.com',
    'website': "http://alkhidmasystems.com",
    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/grade_rank_views.xml',
        'views/employee_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'qweb': [

    ],
}
