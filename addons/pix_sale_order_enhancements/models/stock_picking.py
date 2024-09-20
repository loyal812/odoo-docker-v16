from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    container = fields.Char(
        string="ID Container", related="delivery_note_id.container"
    )
