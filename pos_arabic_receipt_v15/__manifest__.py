{
    'name': 'POS Arabic Receipt V15',
    'summary': 'POS arabic receipt as per the industrial Standard',
    'description': """POS arabic receipt as per the industrial Standard""",
    "version": "15.2.1.1",
    'sequence': 1,
    'email': 'ajmalc6705@gmail.com',
    'website': '',
    'category': 'Point of Sale',
    'author': 'Ajmal',
    'price': 10.00,
    'currency': 'EUR',
    'license': 'LGPL-3',
    "live_test_url": "",
    'depends': ['point_of_sale'],
    
    'data': [

        'views/product_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],

    'assets': {
        'point_of_sale.assets': [
            'pos_arabic_receipt_v15/static/src/js/models.js',
        ],
        'web.assets_qweb': [
            'pos_arabic_receipt_v15/static/src/xml/templates.xml',
        ],

    },

    'installable': True,
    'auto_install': False,
    'application': True,
}
