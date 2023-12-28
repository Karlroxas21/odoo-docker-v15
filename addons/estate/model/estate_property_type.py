from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "real.estate.type"
    _description = "Real State Types"
    # Set Order-Descending Name
    _order = "sequence, name"

    name = fields.Char(require=True)
    property_ids = fields.One2many(
        "real.estate.karl", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("real.estate.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", store=True)

    # SQL Constraints
    _sql_constraints = [("unique_name", "UNIQUE(name)", "Property name must be unique")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
