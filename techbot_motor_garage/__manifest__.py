# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

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
    'name': 'Car Workshop Management System Odoo version 15',
    'version': '15.0.1.0.1',
    'summary': 'Complete Vehicle Workshop Garage Operations ',
    'description': 'Vehicle workshop operations & Its reports',
    'category': 'Industries',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'fleet',
        'sale',
        'sale_management',
        'account_accountant',
        'stock',
        'project',
        'contacts',
    ],
    'data': [
        'report/fleet_report.xml',
        'report/fleet_report_templates.xml',
        'data/fleet_mail_template_data.xml',
        'data/ir_sequence_data.xml',
        'report/job_card.xml',
        'report/job_card_template.xml',
        'views/sale_order_views.xml',
        'views/fleet_view.xml',
        'views/res_partner_view.xml',


        # 'security/workshop_security.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
