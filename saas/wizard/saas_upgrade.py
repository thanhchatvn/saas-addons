# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaasUpgrade(models.TransientModel):
    _name = "saas.upgrade"
    _description = "Upgrade addons"

    module_ids = fields.Many2many(
        'ir.module.module',
        string='Modules Upgrade',
        required=1)

    def do_upgrade(self):
        self.ensure_one()
        self.env['saas.db'].browse(self.env.context.get('active_ids', [])).upgrade([module.name for module in self.module_ids])
        return True
