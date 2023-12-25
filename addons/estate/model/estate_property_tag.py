from odoo import fields, models

class EstatePropertyTag(models.Model):
        _name = "real.estate.tag"
        _description = "Real State Tags"
        # Set Order-Descending Name
        _order = 'name'
        
        name = fields.Char(require=True)
        color = fields.Integer()

        # SQL Constraints
        _sql_constraints = [
                ('unique_name', 'UNIQUE(name)', 'Tag must be unique')
        ]