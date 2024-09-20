from odoo import api,SUPERUSER_ID


def create_supplier_code(cr,registry):
        env = api.Environment(cr,SUPERUSER_ID,{})

        # da usare SOLO  una volta nell'installazione
        records = env['product.template'].search([])
        for rec in records:
                env_cod = env['supplier.code']

                # seller_ids e variant_seller_ids tendenzialmente hanno i stessi record
                lines = rec.seller_ids if len(rec.seller_ids) > len(rec.variant_seller_ids) else rec.variant_seller_ids
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
                                                        ('product_tmpl_id', '=', new['product_tmpl_id']), ('active', '=', False)],
                                        limit=1)
                                if exist:
                                        exist.update({'active': True})

                                else:

                                        rec.write({
                                                'code_suppliers': [(0, 0, new)]
                                        })
                inactive = env_cod.search([('product_tmpl_id', '=', rec.id), ('active', '=', False)])
                # elimino i codici fornitori non esistenti
                inactive.unlink()
        return True