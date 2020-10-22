from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def button_install(self):
        if self.env.user.id not in [1, 2]:
            raise UserError(_('You need to hack our Odoo ? Try it if you can'))
        return super(IrModuleModule, self).button_install()