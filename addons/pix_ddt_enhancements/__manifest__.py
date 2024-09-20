# -*- coding: utf-8 -*-
{
    'name': "pix_ddt_enhancements",

    'summary': """
        Aggiunge funzionalità extra al modulo DDT.""",

    'description': """
        Aggiunge funzionalità extra al modulo DDT.
    """,

    'author': "",
    'website': "https://www",
    'license':
        'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.4',

    # any module necessary for this one to work correctly
    'depends': ['pix_sale_order_enhancements', 'contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/stock_delivery_note.xml',
    ],
}
