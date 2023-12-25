from odoo import fields, models

class ResUsers(models.Model):
        _inherit = 'res.users'

        property_ids = fields.One2many('real.estate.karl', 'sales_person', domain=[('active', '=', True)])