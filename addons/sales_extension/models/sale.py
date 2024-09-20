from odoo import models, fields


class SaleOrder(models.Model):
  _inherit = 'sale.order'

  order_line_products = fields.Char(string='Prodotti', compute='_compute_line_products')

  def _compute_line_products(self):
    for rec in self:
      product_lst = []
      for line in rec.order_line:
        product_lst.append(line.product_id.name)
      product_lst = (',').join(product_lst)
      rec.order_line_products = product_lst
