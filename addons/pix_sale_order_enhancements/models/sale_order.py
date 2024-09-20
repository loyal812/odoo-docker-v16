from odoo import models, fields, api

LOCKED_FIELD_STATES = {state: [("readonly", True)] for state in {"done", "cancel"}}


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ddt_sale_color = fields.Integer("ddt color", default=0)
    invoice_sale_color = fields.Integer("invoice sale color", default=0)
    ddt_date_invoice = fields.Char(
        string="Data/e DDT",
        comodel_name="stock.delivery.note",
        inverse_name="sale_order_ddt",
        compute="_compute_ddt_invoices_ids",
    )
    commitment_date = fields.Date(
        string="Data prevista consegna",
        copy=False,
        states=LOCKED_FIELD_STATES,
        help="This is the delivery date promised to the customer. "
        "If set, the delivery order will be scheduled based on "
        "this date rather than product lead times.",
    )
    expected_date = fields.Date(
        string="Expected Date",
        compute='_compute_expected_date', store=False,  # Note: can not be stored since depends on today()
        help="Delivery date you can promise to the customer, computed from the minimum lead time of the order lines.")
    

    def _compute_ddt_invoices_ids(self):
        for record in self:
            if record.delivery_note_ids:
                record_string = ""
                for r in record.delivery_note_ids:
                    record_string += f"{r.name} del {r.date}{',' if len(record.delivery_note_ids) > 1 else ''}"
                record.ddt_date_invoice = record_string
            else:
                record.ddt_date_invoice = False
                #record.ddt_date_invoice = ','.join([s.name for s in record.related_delivery_notes])

    @api.depends("order_line.customer_lead", "date_order", "state")
    def _compute_expected_date(self):
        """For service and consumable, we only take the min dates. This method is extended in sale_stock to
        take the picking_policy of SO into account.
        """
        self.mapped("order_line")  # Prefetch indication
        for order in self:
            if order.state == "cancel":
                order.expected_date = False
                continue
            dates_list = order.order_line.filtered(
                lambda line: not line.display_type and not line._is_delivery()
            ).mapped(lambda line: line and line._expected_date())
            if dates_list:
                order.expected_date = min(dates_list)
            else:
                order.expected_date = False

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