from odoo import models,fields

class StockPicking(models.Model):
  _inherit = 'stock.picking'

  delivery_note_carrier_id = fields.Many2one(
        "res.partner", string="DN Vettore",related='partner_id.carrier_partner_id'
    )

