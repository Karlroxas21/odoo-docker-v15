from odoo import fields, models

class EstatePropertyType(models.Model):
        _name = "real.estate.type"
        _description = "Real State Types"

        name = fields.Char(require=True)
        