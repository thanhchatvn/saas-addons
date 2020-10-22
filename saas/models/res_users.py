from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    def write(self, vals):
        for user in self:
            if user.id in [1, 2] and self.env.user.id not in [1, 2]:
                raise UserError(_('You need to hack our Odoo ? Try it if you can'))
        return super(ResUsers, self).write(vals)

    def unlink(self):
        for user in self:
            if user.id in [1, 2] and self.env.user.id not in [1, 2]:
                raise UserError(_('You need to hack our Odoo ? Try it if you can'))
        return super(ResUsers, self).unlink()