import json

from odoo import api, models, _
from odoo.tools import float_round


class ReportBomStructure(models.AbstractModel):
  _inherit = 'report.mrp.report_bom_structure'

  # @api.model
  # def _get_report_values(self, docids, data=None):
  #     docs = []
  #     for bom_id in docids:
  #         bom = self.env['mrp.bom'].browse(bom_id)
  #         candidates = bom.product_id or bom.product_tmpl_id.product_variant_ids
  #         quantity = float(data.get('quantity', 1))
  #         for product_variant_id in candidates.ids:
  #             if data and data.get('childs'):
  #                 doc = self._get_pdf_line(bom_id, product_id=product_variant_id, qty=quantity, child_bom_ids=json.loads(data.get('childs')))
  #             else:
  #                 doc = self._get_pdf_line(bom_id, product_id=product_variant_id, qty=quantity, unfolded=True)
  #             doc['report_type'] = 'pdf'
  #             doc['report_structure'] = data and data.get('report_type') or 'all'
  #             docs.append(doc)
  #         if not candidates:
  #             if data and data.get('childs'):
  #                 doc = self._get_pdf_line(bom_id, qty=quantity, child_bom_ids=json.loads(data.get('childs')))
  #             else:
  #                 doc = self._get_pdf_line(bom_id, qty=quantity, unfolded=True)
  #             doc['report_type'] = 'pdf'
  #             doc['report_structure'] = data and data.get('report_type') or 'all'
  #             docs.append(doc)
  #     return {
  #         'doc_ids': docids,
  #         'doc_model': 'mrp.bom',
  #         'docs': docs,
  #     }

  # @api.model
  # def get_html(self, bom_id=False, searchQty=1, searchVariant=False):
  #     res = self._get_report_data(bom_id=bom_id, searchQty=searchQty, searchVariant=searchVariant)
  #     res['lines']['report_type'] = 'html'
  #     res['lines']['report_structure'] = 'all'
  #     res['lines']['has_attachments'] = res['lines']['attachments'] or any(component['attachments'] for component in res['lines']['components'])
  #     res['lines'] = self.env.ref('mrp.report_mrp_bom')._render({'data': res['lines']})
  #     return res

  # @api.model
  # def get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
  #     lines = self._get_bom(bom_id=bom_id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
  #     return self.env.ref('mrp.report_mrp_bom_line')._render({'data': lines})

  # @api.model
  # def get_operations(self, bom_id=False, qty=0, level=0):
  #     bom = self.env['mrp.bom'].browse(bom_id)
  #     lines = self._get_operation_line(bom, float_round(qty / bom.product_qty, precision_rounding=1, rounding_method='UP'), level)
  #     values = {
  #         'bom_id': bom_id,
  #         'currency': self.env.company.currency_id,
  #         'operations': lines,
  #     }
  #     return self.env.ref('mrp.report_mrp_operation_line')._render({'data': values})

  # @api.model
  # def _get_report_data(self, bom_id, searchQty=0, searchVariant=False):
  #     lines = {}
  #     bom = self.env['mrp.bom'].browse(bom_id)
  #     bom_quantity = searchQty or bom.product_qty or 1
  #     bom_product_variants = {}
  #     bom_uom_name = ''
  #
  #     if bom:
  #         bom_uom_name = bom.product_uom_id.name
  #
  #         # Get variants used for search
  #         if not bom.product_id:
  #             for variant in bom.product_tmpl_id.product_variant_ids:
  #                 bom_product_variants[variant.id] = variant.display_name
  #
  #     lines = self._get_bom(bom_id, product_id=searchVariant, line_qty=bom_quantity, level=1)
  #     return {
  #         'lines': lines,
  #         'variants': bom_product_variants,
  #         'bom_uom_name': bom_uom_name,
  #         'bom_qty': bom_quantity,
  #         'is_variant_applied': self.env.user.user_has_groups('product.group_product_variant') and len(bom_product_variants) > 1,
  #         'is_uom_applied': self.env.user.user_has_groups('uom.group_uom')
  #     }
  def _get_bom_data(self,
                    bom,
                    warehouse,
                    product=False,
                    line_qty=False,
                    bom_line=False,
                    level=0,
                    parent_bom=False,
                    index=0,
                    product_info=False,
                    ignore_stock=False):

    lines = super(ReportBomStructure, self)._get_bom_data(bom,
                                                          warehouse,
                                                          product=False,
                                                          line_qty=False,
                                                          bom_line=False,
                                                          level=0,
                                                          parent_bom=False,
                                                          index=0,
                                                          product_info=False,
                                                          ignore_stock=False)

    lines['code_supplier'] = lines['bom'].code_supplier.name if lines['bom'].code_supplier else " "
    if bom_line:
      lines['code_supplier'] = bom_line.code_supplier.name if bom_line.code_supplier else " "

    return lines

  @api.model
  def _get_component_data(self,
                          parent_bom,
                          warehouse,
                          bom_line,
                          line_quantity,
                          level,
                          index,
                          product_info,
                          ignore_stock=False):
    res = super()._get_component_data(parent_bom,
                                      warehouse,
                                      bom_line,
                                      line_quantity,
                                      level,
                                      index,
                                      product_info,
                                      ignore_stock=False)
    res.update({'code_supplier': bom_line.code_supplier.name})
    return res

  @api.model
  def _get_bom_array_lines(self, data, level, unfolded_ids, unfolded, parent_unfolded=True):
    super()._get_bom_array_lines(data, level, unfolded_ids, unfolded, parent_unfolded=True)
    bom_lines = data['components']
    lines = []
    for bom_line in bom_lines:
      line_unfolded = ('bom_' + str(bom_line['index'])) in unfolded_ids
      line_visible = level == 1 or unfolded or parent_unfolded
      lines.append({
          'bom_id': bom_line['bom_id'],
          'code_supplier': bom_line['code_supplier'],
          'name': bom_line['name'],
          'type': bom_line['type'],
          'quantity': bom_line['quantity'],
          'quantity_available': bom_line['quantity_available'],
          'quantity_on_hand': bom_line['quantity_on_hand'],
          'producible_qty': bom_line.get('producible_qty', False),
          'uom': bom_line['uom_name'],
          'prod_cost': bom_line['prod_cost'],
          'bom_cost': bom_line['bom_cost'],
          'route_name': bom_line['route_name'],
          'route_detail': bom_line['route_detail'],
          'lead_time': bom_line['lead_time'],
          'level': bom_line['level'],
          'code': bom_line['code'],
          'availability_state': bom_line['availability_state'],
          'availability_display': bom_line['availability_display'],
          'visible': line_visible,
      })
      if bom_line.get('components'):
        lines += self._get_bom_array_lines(bom_line, level + 1, unfolded_ids, unfolded,
                                           line_visible and line_unfolded)

    if data['operations']:
      lines.append({
          'name': _('Operations'),
          'type': 'operation',
          'quantity': data['operations_time'],
          'uom': _('minutes'),
          'bom_cost': data['operations_cost'],
          'level': level,
          'visible': parent_unfolded,
      })
      operations_unfolded = unfolded or (parent_unfolded and
                                         ('operations_' + str(data['index'])) in unfolded_ids)
      for operation in data['operations']:
        lines.append({
            'name': operation['name'],
            'type': 'operation',
            'quantity': operation['quantity'],
            'uom': _('minutes'),
            'bom_cost': operation['bom_cost'],
            'level': level + 1,
            'visible': operations_unfolded,
        })
    if data['byproducts']:
      lines.append({
          'name': _('Byproducts'),
          'type': 'byproduct',
          'uom': False,
          'quantity': data['byproducts_total'],
          'bom_cost': data['byproducts_cost'],
          'level': level,
          'visible': parent_unfolded,
      })
      byproducts_unfolded = unfolded or (parent_unfolded and
                                         ('byproducts_' + str(data['index'])) in unfolded_ids)
      for byproduct in data['byproducts']:
        lines.append({
            'name': byproduct['name'],
            'type': 'byproduct',
            'quantity': byproduct['quantity'],
            'uom': byproduct['uom'],
            'prod_cost': byproduct['prod_cost'],
            'bom_cost': byproduct['bom_cost'],
            'level': level + 1,
            'visible': byproducts_unfolded,
        })
    return lines
