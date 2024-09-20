from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    code_supplier = fields.Many2one("supplier.code", domain=[('active', '=', True)])

    @api.onchange('code_supplier')
    def onchange_code_supplier(self):
        try:
            if self.code_supplier:
                if self.code_supplier.product_id and self.code_supplier.product_tmpl_id:
                    return self.update({'product_id': self.code_supplier.product_id.id,'product_tmpl_id': self.code_supplier.product_tmpl_id.id})
                elif self.code_supplier.product_id:
                    return self.update({'product_id': self.code_supplier.product_id.id})
                elif self.code_supplier.product_tmpl_id:
                    vals = {'product_tmpl_id': self.code_supplier.product_tmpl_id.id}
                    product_id = self.env['product.product'].search(
                        [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)])
                    if len(product_id.ids) == 1:
                        vals['product_id'] = product_id.id
                    return self.update(vals)
        except Exception as ex:
            _logger.error(f'onchange_code_supplier {self.id} - {ex}')
class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    code_supplier = fields.Many2one("supplier.code", domain=[('active', '=', True)])

    @api.onchange('product_id')
    def onchange_product_id(self):
        try:
            _logger.info(f"onchange_product_id: {self.id}")

            env_cod = self.env['supplier.code']
            sc = env_cod.search([('product_tmpl_id', '=', self.product_tmpl_id.id),('active','=',True)], limit=1)

            if sc:
                self.code_supplier = sc.id
                return self.update({'code_supplier': sc.id})
        except Exception as ex:
            _logger.error(f'onchange_product_id {self.id} - {ex}')

    @api.onchange('code_supplier')
    def onchange_code_supplier(self):
        _logger.info(f"onchange_code_supplier: {self.id}")
        try:
            if self.code_supplier:
                if self.code_supplier.product_id and self.code_supplier.product_tmpl_id:
                    return self.update({'product_id': self.code_supplier.product_id.id,
                                        'product_tmpl_id': self.code_supplier.product_tmpl_id.id})
                elif self.code_supplier.product_id:
                    return self.update({'product_id': self.code_supplier.product_id.id})
                elif self.code_supplier.product_tmpl_id:
                    vals = {'product_tmpl_id': self.code_supplier.product_tmpl_id.id}
                    product_id = self.env['product.product'].search(
                        [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)])
                    if len(product_id.ids) == 1:
                        vals['product_id'] = product_id.id
                    return self.update(vals)
        except Exception as ex:
            _logger.error(f'onchange_code_supplier {self.id} - {ex}')

class RepairOrder(models.Model):
    _inherit = "repair.order"

    code_supplier = fields.Many2one("supplier.code", domain=[('active', '=', True)])

    @api.onchange('code_supplier')
    def onchange_code_supplier(self):
        try:
            if self.code_supplier:
                if self.code_supplier.product_id:
                    return self.update({'product_id': self.code_supplier.product_id.id})
                elif self.code_supplier.product_tmpl_id:
                    product_id = self.env['product.product'].search(
                        [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)])
                    if len(product_id.ids) == 1:
                        return self.update({'product_id': product_id.id})
                    else:
                        return {
                            'domain': {'product_id': [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)]}}
        except Exception as ex:
            _logger.error(f'onchange_code_supplier {self.id} - {ex}')

class RepairLine(models.Model):
    _inherit = "repair.line"

    code_supplier = fields.Many2one("supplier.code", domain=[('active', '=', True)])

    @api.onchange('code_supplier')
    def onchange_code_supplier(self):
        try:
            if self.code_supplier:
                if self.code_supplier.product_id:
                    return self.update({'product_id': self.code_supplier.product_id.id})
                elif self.code_supplier.product_tmpl_id:
                    product_id = self.env['product.product'].search(
                        [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)])
                    if len(product_id.ids) == 1:
                        return self.update({'product_id': product_id.id})
                    else:
                        return {
                            'domain': {'product_id': [('product_tmpl_id', 'in', self.code_supplier.product_tmpl_id.ids)]}}
        except Exception as ex:
            _logger.error(f'onchange_code_supplier {self.id} - {ex}')
