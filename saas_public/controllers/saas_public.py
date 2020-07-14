# Copyright 2019 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.http import route, request, Controller
import logging

_logger = logging.getLogger(__name__)

class SaaSPublicController(Controller):
    @route('/saas/public/<int:template_id>', type='http', auth='public')
    #https://fast_build_053.apps.it-projects.info/auth_quick/check-token?token=c1cffd20-5b03-4af8-81a2-1ab28da4063a
    def create_fast_build(self, template_id, **kwargs):
        if not kwargs:
            kwargs = {}
        template = request.env['saas.template'].browse(template_id).sudo()
        return self._redirect_to_build(template, kwargs)

    def _redirect_to_build(self, template, kwargs):
        if template and template.public_access:
            template_operator_id = template.operator_ids.random_ready_operator()
            build = template_operator_id.create_db(kwargs, with_delay=False)
            build_url = build.get_url()
            _logger.info('new build url: %s' % build_url)
            return request.env['auth_quick_master.token'].sudo().redirect_with_token(build_url, build.id,
                                                                                     build_login='admin')
        else:
            return request.not_found()
