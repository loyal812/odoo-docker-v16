from odoo import fields, models, api


class SupplierCode(models.Model):
  _name = 'supplier.code'

  seller_id = fields.Many2one('res.partner', 'Fornitore')
  name = fields.Char('Codice Fornitore', required=1)
  product_id = fields.Many2one('product.product', 'Variante Prodotto')
  product_tmpl_id = fields.Many2one('product.template', 'Modello Prodotto', required=1)
  active = fields.Boolean(default=True)
  type = fields.Selection(related='product_tmpl_id.type', store=True)

  def inactive_ids(self):
    for rec in self:
      rec.active = False

  def update_supplier_code(self):

    # da usare SOLO  una volta nell'installazione
    records = self.env['product.template'].search([])
    for rec in records:
      env_cod = self.env['supplier.code']

      # seller_ids e variant_seller_ids tendenzialmente hanno i stessi record
      lines = rec.seller_ids if len(rec.seller_ids) > len(
          rec.variant_seller_ids) else rec.variant_seller_ids
      rec.code_suppliers.inactive_ids()
      for line in lines:
        new = {}
        if not line.product_code:
          continue
        else:
          new['name'] = line.product_code
          new['seller_id'] = line.name.id
          new['product_tmpl_id'] = line.product_tmpl_id.id
          new['product_id'] = line.product_id.id or False
          exist = env_cod.search([('name', '=', new['name']), ('seller_id', '=', new['seller_id']),
                                  ('product_id', '=', new['product_id']),
                                  ('product_tmpl_id', '=', new['product_tmpl_id']),
                                  ('active', '=', False)],
                                 limit=1)
          if exist:
            exist.update({'active': True})

          else:

            rec.write({'code_suppliers': [(0, 0, new)]})
      inactive = env_cod.search([('product_tmpl_id', '=', rec.id), ('active', '=', False)])
      # elimino i codici fornitori non esistenti
      inactive.unlink()


class ProductTemplate(models.Model):
  _inherit = 'product.template'

  code_suppliers = fields.One2many('supplier.code',
                                   'product_tmpl_id',
                                   string='Codici forn.',
                                   domain=[('active', '=', True)])

  #teoricamente non dovrebbe mai essere triggerata, ma se dovesse ...
  @api.model
  def create(self, vals):
    res = super(ProductTemplate, self).create(vals)

    if res.seller_ids:

      codici = [
          (5, 0, 0),
      ]

      for line in res.seller_ids:

        codice = {}
        if not line.product_code:
          continue
        else:
          codice['seller_id'] = line.name.id
          codice['name'] = line.product_code
          codice['product_tmpl_id'] = line.product_tmpl_id.id
          codice['product_id'] = line.product_id.id
        codice = (0, 0, codice)
        codici.append(codice)
      res.write({'code_suppliers': codici})

    return res

  def write(self, vals):
    res = super(ProductTemplate, self).write(vals)
    try:
      if vals.get('seller_ids') or vals.get('variant_seller_ids'):
        env_cod = self.env['supplier.code']
        #seller_ids e variant_seller_ids tendenzialmente hanno i stessi record
        lines = self.seller_ids if len(self.seller_ids) > len(
            self.variant_seller_ids) else self.variant_seller_ids
        self.code_suppliers.inactive_ids()
        for line in lines:
          new = {}
          if not line.product_code:
            continue
          else:
            new['name'] = line.product_code
            new['seller_id'] = line.name.id
            new['product_tmpl_id'] = line.product_tmpl_id.id
            new['product_id'] = line.product_id.id or False
            exist = env_cod.search([('name', '=', new['name']),
                                    ('seller_id', '=', new['seller_id']),
                                    ('product_id', '=', new['product_id']),
                                    ('product_tmpl_id', '=', new['product_tmpl_id']),
                                    ('active', '=', False)],
                                   limit=1)
            if exist:
              exist.update({'active': True})

            else:

              self.write({'code_suppliers': [(0, 0, new)]})
        inactive = env_cod.search([('product_tmpl_id', '=', self.id), ('active', '=', False)])
        #elimino i codici fornitori non esistenti
        inactive.unlink()
    except:
      pass
    return res
