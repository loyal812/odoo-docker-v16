#-*- coding: utf-8 -*-
import xmlrpc.client
from odoo import http, _
from odoo.http import Controller, route, dispatch_rpc, request
#from jose import jwt
import logging

_logger = logging.getLogger(__name__)


class RPC(Controller):
  """Handle RPC connections."""

  @route('/testapi', type='json', auth="none", save_session=False, cors='*')
  def jsonrpc(self, service, method, token, args):

    #C:\Projects\Python\github\odoo\odoo\http.py
    #C:\Projects\Python\github\odoo\odoo\service\model.py

    # TODO: validate token....

    #data = jwt.decode(token, key=None, options={"verify_signature":False })
    #data = jwt.decode(token, key=None, options={"verify_signature":False,'verify_exp': False,'verify_aud':False })

    #_logger.info(data)

    #company = 'Company 1'
    #args[2][0].extend([['company_id.name', '=', company]])

    args = [request.env.cr.dbname, 2, '09b16807a61bd4f19f06e7054d079bb946fa4213', *args]  #database, integer, API key

    return dispatch_rpc(service, method, args)

  @http.route('/actions_saleorder', type='json', auth='public')
  def confirm_saleorder(self, **rec):

    if rec['id']:
      sale_order = request.env['sale.order'].sudo().search([('id', '=', rec['id'])])
      for so in sale_order:
        if(rec['action'] == 'confirm'): #Works
            so.action_confirm()
        if(rec['action'] == 'cancel'):
            wizard = request.env['sale.order.cancel'].sudo().with_context(**{'order_id': so.id}).create({'order_id': so.id,'email_from':''})
            wizard.action_cancel()
        if(rec['action'] == 'draft'):
            so.action_draft() #Works
      args = {'success': True, 'message': 'Success', 'ID': rec['id']}
    return args

  @http.route('/create_partner', type='json', auth='public')
  def create_partner(self, **rec):
    # logging.info('here')
    # if request.jsonrequest:
    if rec['name']:
      sale_oder = request.env['res.partner'].sudo().create(vals)
      if sale_oder:
        vals = {'name': rec['name']}
        logging.info(sale_oder)
        args = {'success': True, 'message': 'Success', 'ID': sale_oder.id}
      else:
          args = {'success': False, 'message': 'No sale order found'}
    return args

  @http.route('/update_partner', type='json', auth='public')
  def update_partner(self, **rec):

    if rec['id']:
      partner = request.env['res.partner'].sudo().search([('id', '=', rec['id'])])
      if partner:
        partner.sudo().write(rec)
      args = {'success': True, 'message': 'success'}
    return args

  @http.route('/delete_partner', type='json', auth='public')
  def delete_partner(self, **rec):

    if rec['id']:
      partner = request.env['res.partner'].sudo().search([('id', '=', rec['id'])])
      if partner:
        partner.sudo().unlink()
      args = {'success': True, 'message': 'success'}
    return args

  @http.route('/create_attachment', type='json', auth='public')
  def create_attachment(self, **rec):
      if rec['type']:
          attachment = self.action_create_attachment(rec['data'], rec['model'], rec['id'], rec['file_name'])
          if attachment:
              args = {'success': True, 'message': 'Success', 'ID': rec['id']}
          else:
              args = {'success': False, 'message': 'Fail', 'ID': rec['id']}
      return args

  def action_create_attachment(self, base64img, model, rec_id, file_name):
      attachment = request.env['ir.attachment'].sudo().create({
          'name': file_name,
          'type': 'binary',
          'datas': base64img,
          'res_model': model,
          'res_id': rec_id
      })
      return attachment