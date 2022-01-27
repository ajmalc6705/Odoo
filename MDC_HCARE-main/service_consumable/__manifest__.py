# -*- coding: utf-8 -*-
{
    'name': 'Consumables for Service Products',
    'version': '1.5',
    'category': 'Accounting',
    'author': 'Al Khidma Systems',
    'website': 'http://www.alkhidmasystems.com',
    'license': 'AGPL-3',
    'depends': ['product', 'pragtech_dental_management'],
    'data': [
             'security/consumable_security.xml',
             'security/ir.model.access.csv',
             'wizard/service_consumables.xml',
             'reports/report.xml',
             'reports/report_service_consumables.xml',
             'wizard/stock_reversal.xml',
             'views/physician.xml',
             'views/stock_picking.xml',
             'views/product.xml',
             'views/appointment.xml',
             ],

    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
