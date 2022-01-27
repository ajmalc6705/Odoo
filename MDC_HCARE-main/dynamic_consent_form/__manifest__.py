{
    'name': "Dynamic Consent and Fields - HCARE",
    'version': '0.25',
    'sequence': 2,
    'author': 'Al Khidma Systems',
    'category': '',
    'description': 'Dynamic Consent and Fields - HCARE',
    'depends': ['base', 'web', 'pragtech_dental_management','report_letterhead'],
    'data': [
        'views/config_settings.xml',
        'security/ir.model.access.csv',
        'views/consent_details.xml',
        'wizard/field_creation.xml',
        'wizard/consent_form.xml',
        'wizard/update_view.xml',
        'views/appointment.xml',
        'views/fields.xml',
        'views/hcare_dashboard.xml',
        'data/dashboard_data.xml',
        'views/dashboard_view.xml',
        'wizard/table_creation.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
