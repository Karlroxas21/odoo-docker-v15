from odoo import fields, models

class EstatePropertyType(models.Model):
        _name = "real.estate.type"
        _description = "Real State Types"

        name = fields.Char(require=True)
        
        # SQL Constraints
        _sql_constraints = [
                ('unique_name', 'UNIQUE(name)', 'Property name must be unique')
        ]