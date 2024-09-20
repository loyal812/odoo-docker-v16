# -*- coding: utf-8 -*-
{
    'name': "pix_sale_order_enhancements",

    'summary': """
        Aggiunge funzionalità extra al modulo Vendite.""",

    'description': """
        Aggiunge funzionalità extra al modulo Vendite.
    """,

    'author': "",
    'website': "https://www",
    'license':
        'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','l10n_it_delivery_note','account','stock', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_order.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pix_sale_order_enhancements/static/src/js/widget.js',
        ],
    },
}
