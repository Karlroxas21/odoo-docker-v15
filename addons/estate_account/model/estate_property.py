from odoo import models


class EstateProperty(models.Model):
    _inherit = "real.estate.karl"

    def sold_action(self):
        partner_id = self.offer_ids.partner_id

        # 6% of the selling price
        selling_price_percentage = 0.06 * self.selling_price

        move_vals = {
            "partner_id": partner_id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "Selling Price Percentage",
                        "quantity": "1",
                        "price_unit": selling_price_percentage,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    },
                ),
            ],
        }

        self.env["account.move"].create(move_vals)
        return super(EstateProperty, self).sold_action()
