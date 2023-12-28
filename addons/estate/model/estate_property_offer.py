from odoo import fields, models, api, exceptions
from odoo.tools import float_utils
from odoo.exceptions import ValidationError, UserError

from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "real.estate.offer"
    _description = "Real State Offer"
    # Set Order-Descending Price
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    partner_id = fields.Many2one("res.partner", require=True)
    property_id = fields.Many2one("real.estate.karl", require=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    # SQL Constrataints
    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "Offer must be strictly positive")
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days

    # Set offer status
    def accept_action(self):
        for record in self:
            accepted_offers = self.env["real.estate.offer"].search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("status", "=", "accepted"),
                ]
            )

            if accepted_offers:
                raise exceptions.UserError(
                    "Only one offer can be accepted for a given property."
                )

            record.property_id.state = "offer accepted"
            record.property_id.buyer = record.partner_id.display_name
            record.property_id.selling_price = record.price

            self.status = "accepted"

    def refuse_action(self):
        self.status = "refused"
        # for record in self:
        #         accepted_offers = self.env['real.estate.offer'].search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])

        #         if accepted_offers:
        #                 self.status = 'refused'
        #         else:
        #                 self.property_id.selling_price = 0
        #                 record.property_id.buyer = ''
        #                 record.property_id.state = 'new'

    # Set offer received status when there is an offer and raise an error if user
    # tries to create an offer with a lower amount than before
    @api.model
    def create(self, vals):
        property_obj = self.env["real.estate.karl"].browse(vals.get("property_id"))

        # Check if the new offer amount is lower than existing offer
        if property_obj.offer_ids and any(
            offer.price > vals.get("price") for offer in property_obj.offer_ids
        ):
            raise UserError(
                "You cannot create an offer with a lower amount than an existing offer."
            )

        property_obj.state = "offer received"

        return super(EstatePropertyOffer, self).create(vals)
