from odoo import fields, models

class EstatePropertyOffer(models.Model):
        _name = "real.estate.offer"
        _description = "Real State Offer"

        price = fields.Float()
        status = fields.Selection([('accepted', 'Accepted'), 
                                   ('refused', 'Refused')], copy=False)
        partner_id = fields.Many2one('res.partner', require=True)
        property_id = fields.Many2one('real.estate.karl',require=True)
        
        