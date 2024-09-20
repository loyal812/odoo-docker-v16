from odoo import fields, models
import logging

# DONE_READONLY_STATE = {"done": [("readonly", True)]}


class StockDeliveryNote(models.Model):
  _inherit = 'stock.delivery.note'

  note = fields.Html(string="Note", compute='_compute_delivery_note', readonly=False)
  carrier_partner_id = fields.Many2one(comodel_name='res.partner', string='Vettore',related='partner_id.carrier_partner_id', readonly=False)

  def _compute_delivery_note(self):
    for rec in self:
      if rec.sale_ids[0]:
        rec.note = rec.sale_ids[0].note
      else:
        rec.note=False
      
