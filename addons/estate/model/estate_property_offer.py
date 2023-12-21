from odoo import fields, models, api, exceptions
from odoo.tools import float_utils
from odoo.exceptions import ValidationError

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

        #SQL Constrataints
        _sql_constraints = [
                ('check_price', 'CHECK(price >= 0)', "Offer must be strictly positive")
        ]
        
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
                        
                        # if not float_utils.float_is_zero(record.price, precision_digits=2) and float_utils.float_compare(record.price, 0.9 * record.property_id.expected_price, precision_digits=2):
                        #         raise exceptions.UserError("Selling price cannot be lower than 90% of the expected price")       
                        # if not float_utils.float_is_zero(record.price, precision_digits=2) and float_utils.float_compare(record.price, 0.9 * record.property_id.expected_price, precision_digits=2):
                        #         raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price NEW")     

                        record.property_id.state = 'sold'
                        record.property_id.buyer = record.partner_id.display_name
                        record.property_id.selling_price = record.price
                                
                        self.status = 'accepted'
        
        def refuse_action(self):
                for record in self:
                        accepted_offers = self.env['real.estate.offer'].search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])

                        if accepted_offers:
                                self.status = 'refused'
                        else:
                                self.property_id.selling_price = 0
                                record.property_id.buyer = ''
                                record.property_id.state = 'new'

        #Constrain for selling price and expected price
        # @api.constrains('property_id.selling_price', 'property_id.expected_price')
        # def _check_selling_and_expected_price(self):
        #         for record in self:
        #                 if record.property_id.selling_price < 0.9 * record.property_id.expected_price:
        #                         raise exceptions.ValidationError("Selling price must at least 90% of expected price")