# -*- coding: utf-8 -*-
# from odoo import http


# class PixSaleOrderEnhancements(http.Controller):
#     @http.route('/pix_sale_order_enhancements/pix_sale_order_enhancements', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pix_sale_order_enhancements/pix_sale_order_enhancements/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pix_sale_order_enhancements.listing', {
#             'root': '/pix_sale_order_enhancements/pix_sale_order_enhancements',
#             'objects': http.request.env['pix_sale_order_enhancements.pix_sale_order_enhancements'].search([]),
#         })

#     @http.route('/pix_sale_order_enhancements/pix_sale_order_enhancements/objects/<model("pix_sale_order_enhancements.pix_sale_order_enhancements"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pix_sale_order_enhancements.object', {
#             'object': obj
#         })
