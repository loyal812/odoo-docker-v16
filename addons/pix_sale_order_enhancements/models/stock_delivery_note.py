from odoo import models, fields, api

DDT_COLOR_MAP = {"draft": 0, "confirm": 1, "invoiced": 4, "done": 10}
DDT_COLOR_STATE = ["confirm", "invoiced", "done"]


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def default_partner_shipping_ddt(self):
        picking_id = self.env['stock.picking'].browse(self._context.get('active_id', False))
        return picking_id.sale_id.partner_id

    partner_shipping_ddt = fields.Many2one("res.partner", required=False,
                                         default=default_partner_shipping_ddt, string="Cliente")

    ddt_sale_color = fields.Integer(
        "ddt color",
        default=0,
        compute="_compute_ddt_sale_color",
    )
    container = fields.Char(string="ID Container")

    def _compute_ddt_sale_color(self):
        for record in self:
            if record.state in DDT_COLOR_STATE:
                draft_count = 0
                if record.invoice_ids:
                    for invoice in record.invoice_ids:
                        if invoice.state == "draft":
                            draft_count += 1
                        if draft_count:
                            record.ddt_sale_color = DDT_COLOR_MAP.get("confirm", 0)
                        else:
                            record.ddt_sale_color = DDT_COLOR_MAP.get("done", 0)
                else:
                    record.ddt_sale_color = DDT_COLOR_MAP.get("draft", 0)
            else:
                record.ddt_sale_color = DDT_COLOR_MAP.get("draft", 0)

class StockDeliveryNoteCreateWizard(models.TransientModel):
    _inherit = "stock.delivery.note.create.wizard"
    
    def default_partner_shipping_ddt(self):
        picking_id = self.env['stock.picking'].browse(self._context.get('active_id', False))
        return picking_id.sale_id.partner_id
    
    partner_shipping_ddt = fields.Many2one("res.partner",
                                         required=False, readonly=True,
                                         default=default_partner_shipping_ddt)