from odoo import models, api


class ResPartner(models.Model):
  _inherit = 'res.partner'

  @api.onchange('vat', 'country_id')
  def _l10n_it_onchange_vat(self):
    ...
