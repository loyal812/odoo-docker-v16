# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "Ricerca prodotti per codice fornitore",
    'version': "1.0.0.0",
    'author': "AIR-kp",
    'summary': 'Ricerca prodotti per codice fornitore',
    'description' : 'Ricerca prodotti per codice fornitore',
    'license':'OPL-1',
    'category': "Extra Tools",
    'data':[
        'security/ir.model.access.csv',
        #la vista seguente mostra il menù dei codici
        'views/code_supplier.xml',
        'views/sale_order.xml',
        'views/product_search.xml',
        'views/mrp.xml',
        'data/scheduler.xml',
        'reports/cod_suppl_order_document.xml'

            ],
    'website': 'https://www.air-srl.com',
    'depends': ['sale','product','purchase','sale_management','mrp','repair','uom'],
    'installable': True,
    'auto_install': False,
    'images':['static/description/icon.png'],
    'post_init_hook':'create_supplier_code'
}