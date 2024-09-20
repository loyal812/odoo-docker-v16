from odoo import models, fields, api

INVOICE_COLOR_MAP = {"not_paid": 1, "in_payment": 2, "paid": 10, "partial": 3}


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_sale_color = fields.Integer(
        "invoice color", default=0, compute="_compute_invoice_sale_color",
    )

    def _compute_invoice_sale_color(self):
        for record in self:
            if record.state == "canceled":
                record.invoice_sale_color = 0
            else:
                record.invoice_sale_color = INVOICE_COLOR_MAP.get(
                    record.payment_state, 0
                )
