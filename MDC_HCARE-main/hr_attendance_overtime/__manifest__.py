# -*- coding: utf-8 -*-
{
    'name': 'HR Overtime Management',
    'version': '10.0.1.0.0',
    'summary': 'Overtime Payment Based On Attendance',
    'category': 'Human Resources',
    'author': 'Al Khidma Systems',
    'company': '',
       'website': 'http://www.alkhidmasystems.com',
    'depends': ['hr_payroll', 'hr_attendance', 'hr_leaves_solution'],
    'data': [
        'views/hr_config_settings.xml',
        'views/contract.xml',
        'data/salary_rule.xml',
    ],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
