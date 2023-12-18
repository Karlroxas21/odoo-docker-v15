from odoo import fields, models

class EstateProperty(models.Model):
        _name = "real.estate.karl"
        _description = "Real State by Karl"

        name = fields.Char(require=True)
        tag_ids = fields.Many2many('real.estate.tag', string="Tag")
        property_type_id = fields.Many2one('real.estate.type', string="Property Type")
        buyer = fields.Char(copy=False)
        sales_person = fields.Char('res.users', default=lambda self: self.env.user.name)
        offer_ids = fields.One2many('real.estate.offer', 'property_id', string="Offer")
        description = fields.Text()
        postcode = fields.Char()
        date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3 ))
        expected_price = fields.Float(require=True)
        selling_price = fields.Float(readonly=True, copy=False)
        active = fields.Boolean(default=False)
        state = fields.Selection(
                [('new', 'New'),
                ('offer', 'Offer'),
                ('received', 'Received'),
                ('offer accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')],
                require=True,
                copy=False,
                default='new')
        bedrooms = fields.Integer(default=2)
        living_area = fields.Integer()
        facades = fields.Integer()
        garage = fields.Boolean()
        garden = fields.Boolean()
        garden_area = fields.Integer()
        garden_orientation = fields.Selection(
                [('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
                string="Garden facing orientation")