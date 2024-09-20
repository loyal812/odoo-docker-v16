from odoo import fields, models, api


class SaleOrderLine(models.Model):
        _inherit = 'sale.order.line'

        code_supplier = fields.Many2one('supplier.code',domain=[('active','=',True)])

        @api.onchange('code_supplier')
        def onchange_code_supplier(self):
                if self.code_supplier:
                        if self.code_supplier.product_id:
                                return self.update({'product_id':self.code_supplier.product_id.id})
                        elif self.code_supplier.product_tmpl_id:
                                product_id = self.env['product.product'].search([('product_tmpl_id','in',self.code_supplier.product_tmpl_id.ids)])
                                if len(product_id.ids) == 1:
                                        return self.update({'product_id': product_id.id})
                                else:
                                        return {'domain':{'product_id' : [('product_tmpl_id','in',self.code_supplier.product_tmpl_id.ids)]}}