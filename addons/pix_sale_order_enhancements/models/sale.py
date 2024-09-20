from odoo import models, fields


class SaleOrder(models.Model):
  _inherit = 'sale.order'

  order_line_products = fields.Char(string='Prodotti', compute='_compute_line_products')

  def _compute_line_products(self):
    for rec in self:
      product_lst = []
      for line in rec.order_line:
        if(line.product_id.name != False):
          product_lst.append(line.product_id.name)
      
      if(product_lst != False):
        product_lst_join = ','.join(product_lst)
      else:
        product_lst_join = False

      rec.order_line_products = product_lst_join