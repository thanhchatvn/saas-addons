# -*- coding: utf-8 -*
from odoo.http import request
import json
from odoo import http, _
from odoo.addons.web.controllers.main import ensure_db, Home, Session, WebClient

import logging

_logger = logging.getLogger(__name__)


class WebLogin(Home):

    @http.route(['/saas/auth-to-build/<int:build_id>'], type='http',
                auth='none')
    def auth_build_login(self, build_id=None):
        return http.local_redirect('/web/login?build_id=%s' % build_id)
