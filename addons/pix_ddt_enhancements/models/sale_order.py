from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
    carrier_partner_id = fields.Many2one(
        "res.partner",
        string="Vettore",
        tracking=True,
        readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",related='partner_id.carrier_partner_id'
    )

