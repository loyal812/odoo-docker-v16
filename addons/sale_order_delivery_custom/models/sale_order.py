from odoo import fields,models

class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"
    sale_id = fields.Many2one(comodel_name='sale.order')


class SaleOrderFix(models.Model):
  _inherit = 'sale.order'

  related_delivery_notes = fields.One2many(comodel_name='stock.delivery.note', inverse_name='sale_id', string='Related Delivery Notes',compute='_compute_related_delivery')

  

  
  def _compute_related_delivery(self):
     
    for rec in self:
      rec.related_delivery_notes = False
      for item in rec.picking_ids:
          rec.related_delivery_notes = rec.related_delivery_notes + item.delivery_note_id


class StockDeliveryNote(models.Model):
   _inherit = 'stock.delivery.note'

   ddt_color = fields.Integer(
        "ddt_color", default=6
    )
  

   

