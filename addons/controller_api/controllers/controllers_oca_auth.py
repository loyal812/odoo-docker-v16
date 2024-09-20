#-*- coding: utf-8 -*-
from urllib import request
from odoo.addons.auth_oauth.controllers.main import OAuthController
from odoo import http
from odoo.http import Controller, route, dispatch_rpc, request, Response
import xmlrpc.client

class OauthControllerAPI(OAuthController):

    @http.route(type='json', csrf=False, save_session=False)
    def signin(self, **kw):
        
        
        
        #request.update_env(user=1)
        return super().signin(**kw)