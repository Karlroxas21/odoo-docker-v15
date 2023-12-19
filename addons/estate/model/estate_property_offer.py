from odoo import fields, models, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
        _name = "real.estate.offer"
        _description = "Real State Offer"

        price = fields.Float()
        status = fields.Selection([('accepted', 'Accepted'), 
                                   ('refused', 'Refused')], copy=False)
        validity = fields.Integer(default=7)
        date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
        partner_id = fields.Many2one('res.partner', require=True)
        property_id = fields.Many2one('real.estate.karl',require=True)
        
        @api.depends('create_date', 'validity')
        def _compute_date_deadline(self):
                for record in self:
                        if record.create_date:
                                record.date_deadline = record.create_date + timedelta(days=record.validity)

        def _inverse_date_deadline(self):
                for record in self:
                        if record.create_date and record.date_deadline:
                                record.validity = (record.date_deadline - record.create_date).days