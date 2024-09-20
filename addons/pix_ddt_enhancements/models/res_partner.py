from odoo import models, fields

class ResPartner(models.Model):
  _inherit = 'res.partner'

  carrier_partner_id = fields.Many2one(
      "res.partner",
      string="Vettore",
      tracking=True,
      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
  )