# -*- coding: utf-8 -*
from odoo.http import request
import json
from odoo import http, _
from odoo.addons.web.controllers.main import ensure_db, Home, Session, WebClient

import logging

_logger = logging.getLogger(__name__)


class WebLogin(Home):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(WebLogin, self).web_login(*args, **kw)
        build_id = kw.get('build_id', None)
        if build_id:
            client_build_id = request.env['ir.config_parameter'].sudo().get_param('auth_quick.build')
            users = request.env['res.users'].sudo().search([], order='id', limit=1)
            if client_build_id and int(client_build_id) > 0:
                user = users[0]
                uid = request.session.authenticate(request.session.db, 'admin', 'admin')
                if uid:
                    request.params['login'] = user.login
                    request.params['password'] = 'admin'
                    request.params['login_success'] = True
                    return http.redirect_with_hash(self._login_redirect(uid, redirect='/web'))
        return response

    @http.route(['/saas/auth-to-build/<int:build_id>'], type='http',
                auth='none')
    def auth_build_login(self, build_id=None):
        return http.local_redirect('/web/login?build_id=%s' % build_id)
