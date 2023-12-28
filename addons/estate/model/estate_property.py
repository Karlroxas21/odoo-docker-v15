from odoo import fields, models, api, exceptions
from odoo.tools import float_utils
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = "real.estate.karl"
    _description = "Real State by Karl"
    # Set Order-Descending ID
    _order = "id desc"

    name = fields.Char(require=True)
    tag_ids = fields.Many2many("real.estate.tag", string="Tag")
    property_type_id = fields.Many2one("real.estate.type", string="Property Type")
    buyer = fields.Char(copy=False)
    sales_person = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("real.estate.offer", "property_id", string="Offer")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        months=3,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(require=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_offer = fields.Integer(compute="_compute_highest_offer")
    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        require=True,
        copy=False,
        default="new",
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Garden facing orientation",
    )

    # SQL Constrataints
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price >= 0)",
            "Expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be strictly positive",
        ),
    ]

    # Compute total area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Get the highest offer
    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        for record in self:
            best_offer = record.offer_ids.mapped("price")
            record.best_offer = max(best_offer) if best_offer else 0

    # Set values for garden and garden orientation on change
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = "north"

    # Mark as SOLD
    def sold_action(self):
        for record in self:
            if self.state == "canceled":
                raise exceptions.UserError("Canceled properties cannot be sold")

            self.state = "sold"

    # Cancel property
    def cancel_action(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold property cannot be canceled.")

            record.state = "canceled"

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price
                and record.selling_price < 0.9 * record.expected_price
            ):
                raise exceptions.ValidationError(
                    "Selling price cannot be lower than 90% of the expected price."
                )

    #        Prevent deletion of property that is not new and canceled
    @api.ondelete(at_uninstall=False)
    def _unlink_except_not_new_and_canceled(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(
                    "You cannot delete a property which is in %s state."
                    % (record.state,)
                )

        return super(EstateProperty, self)
