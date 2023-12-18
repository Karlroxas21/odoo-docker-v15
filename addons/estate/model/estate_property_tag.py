from odoo import fields, models

class EstatePropertyTag(models.Model):
        _name = "real.estate.tag"
        _description = "Real State Tags"

        name = fields.Char(require=True)
        