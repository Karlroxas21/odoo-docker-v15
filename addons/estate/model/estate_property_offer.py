from odoo import fields, models, api, exceptions
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

        # Set offer status
        def accept_action(self):
                for record in self:
                        accepted_offers = self.env['real.estate.offer'].search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])

                        if accepted_offers:
                                raise exceptions.UserError("Only one offer can be accepted for a given property.")
                        
                        record.property_id.state = 'sold'
                        record.property_id.buyer = record.partner_id.display_name
                        record.property_id.selling_price = record.price
                        
                        self.status = 'accepted'
  
        def refuse_action(self):
                self.status = 'refused'