# -*- coding: utf-8 -*-
{
    'name': "sales_extension",

    'summary': """
        ITA : Colonna aggiuntiva sulla vista SALES
        ENG : Extra column on SALES view
        """,

    'description': """
        ITA : Colonna aggiuntiva sulla vista SALES
        ENG : Extra column on SALES view
    """,

    'author': "",
    'website': "",
    'license':
        'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.1.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        'views/sale_order.xml',
    ],
}
