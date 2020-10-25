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
        context = self.env.context
        dbs = None
        if context.get('source_mode', None) == 'saas.db':
            dbs = self.env['saas.db'].browse(self.env.context.get('active_ids', []))
        else:
            dbs = self.env['saas.template.operator'].browse(self.env.context.get('active_ids', []))
        if dbs:
            dbnames = [db.name for db in dbs]
            self.env['saas.db'].upgrade(dbnames, [module.name for module in self.module_ids])
        return True
