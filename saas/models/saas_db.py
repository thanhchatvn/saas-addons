# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2019 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, tools, SUPERUSER_ID, sql_db, registry
from odoo.addons.queue_job.job import job
from odoo.http import _request_stack
import threading

class saas_db(models.Model):
    _name = 'saas.db'
    _description = 'Build'

    name = fields.Char('Name', help='Technical Database name')
    operator_id = fields.Many2one('saas.operator', required=True)
    type = fields.Selection([
        ('template', 'Template DB'),
        ('build', 'Normal Build'),
    ], string='DB Type', default='build')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Ready'),
    ], default='draft')

    def unlink(self):
        self.drop_db()
        return super(saas_db, self).unlink()

    @job
    def create_db(self, template_db, demo, lang='en_US', callback_obj=None, callback_method=None):
        self.ensure_one()
        db_name = self.name
        self.operator_id._create_db(template_db, db_name, demo, lang)
        self.state = 'done'
        self.env['saas.log'].log_db_created(self)
        if callback_obj and callback_method:
            getattr(callback_obj, callback_method)()

    @job
    def drop_db(self):
        for r in self:
            r.operator_id._drop_db(r.name)
            r.state = 'draft'
            self.env['saas.log'].log_db_dropped(r)

    def get_url(self):
        # TODO: need possibility to use custom domain
        self.ensure_one()
        return self.operator_id.get_db_url(self)

    def action_get_build_access(self):
        self.ensure_one()
        auth_url = 'http://' + self.name + '/saas/auth-to-build/' + str(self.id)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': auth_url,
        }

    def upgrade(self, db_names, models_name):
        for db_name in db_names:
            threaded_synchronization = threading.Thread(target=self._auto_upgrade, args=(
                db_name, models_name))
            threaded_synchronization.start()

    def _auto_upgrade(self, db_name, models_name=[]):
        with api.Environment.manage():
            new_cr = registry(self._cr.dbname).cursor()
            env = api.Environment(new_cr, SUPERUSER_ID, {})
            env['ir.module.module'].sudo().search([('name', 'in', models_name)]).button_immediate_upgrade()
            new_cr.commit()
            new_cr.close()
        return True
