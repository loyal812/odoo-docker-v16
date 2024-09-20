#-*- coding: utf-8 -*-
import xmlrpc.client
from odoo import http, _
from odoo.http import Controller, route, dispatch_rpc, request
from jose import jwt
import logging
_logger = logging.getLogger(__name__)
class RPC(Controller):
    """Handle RPC connections."""

    @route('/erp5', type='json', auth="none", save_session=False, cors='*')
    def jsonrpc(self, service, method, token, args):

        #C:\Projects\Python\github\odoo\odoo\http.py
        #C:\Projects\Python\github\odoo\odoo\service\model.py
                
        # TODO: validate token....

        #data = jwt.decode(token, key=None, options={"verify_signature":False })
        #data = jwt.decode(token, key=None, options={"verify_signature":False,'verify_exp': False,'verify_aud':False })

        #_logger.info(data)
        
        #company = data['company']
        
        args = [request.env.cr.dbname, 2, 'fdc09b6d8df76ccefaf9031381b22dff08daba69', *args] #database, integer, API key

        return dispatch_rpc(service, method, args)
    
    @http.route('/create_partner', type='json', auth='public')
    def create_partner(self, **rec):
        # logging.info('here')
        # if request.jsonrequest:
        if rec['name']:
            vals = {'name': rec['name']}
            new_partner = request.env['res.partner'].sudo().create(vals)
            logging.info(new_partner)
            args = {'success': True, 'message': 'Success', 'ID': new_partner.id}
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